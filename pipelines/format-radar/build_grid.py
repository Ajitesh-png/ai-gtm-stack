#!/usr/bin/env python3
"""
Max Format Radar — template B: the 3-up "yapping" grid.

Reads episode-yapping.json, renders the chrome layer once with headless
Chrome, and hstacks the three clips underneath it.

    python build_grid.py
    python build_grid.py other-episode.json
    python build_grid.py --still

Cheap by design: ONE Chrome render, ONE ffmpeg pass. There are no per-scene
overlays here because all three panels play simultaneously.

Requires: Chrome, ffmpeg on PATH.
"""

import json
import re
import subprocess
import sys
from pathlib import Path

from build import CHROME_CANDIDATES, find_chrome, run  # shared helpers

ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".work-grid"
TEMPLATE = ROOT / "post-template-yapping.html"

PANEL_W, PANEL_H = 608, 1080          # true 9:16
CANVAS_W, CANVAS_H = PANEL_W * 3, PANEL_H
FPS = 30

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}


def make_html(cfg: dict, mode: str, dest: Path) -> None:
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("--preview:.5", "--preview:1")
    html, n = re.subn(r"^<body>", f'<body data-mode="{mode}">', html, count=1, flags=re.M)
    if n != 1:
        sys.exit("Could not find the <body> tag at line start in post-template-yapping.html.")
    html = html.replace("<head>", f'<head>\n<base href="{ROOT.as_uri()}/">', 1)
    dest.write_text(
        re.sub(
            r'(<script id="episode" type="application/json">).*?(</script>)',
            lambda m: m.group(1) + "\n" + json.dumps(cfg, ensure_ascii=False, indent=2) + "\n" + m.group(2),
            html,
            flags=re.S,
        ),
        encoding="utf-8",
    )


def shoot(chrome: str, html: Path, png: Path, transparent: bool) -> None:
    cmd = [
        chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
        "--force-device-scale-factor=1",
        f"--window-size={CANVAS_W},{CANVAS_H}",
        "--virtual-time-budget=5000",
    ]
    if transparent:
        cmd.append("--default-background-color=00000000")
    cmd += [f"--screenshot={png}", str(html)]
    run(cmd)
    if not png.exists():
        sys.exit(f"Chrome wrote no screenshot for {html.name}.")


def probe_duration(path: Path) -> float:
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(path)])
    return float(r.stdout.strip())


def main() -> None:
    args = [a for a in sys.argv[1:]]
    still_only = "--still" in args
    args = [a for a in args if not a.startswith("--")]
    cfg_path = ROOT / (args[0] if args else "episode-yapping.json")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    panels = cfg.get("panels", [])
    if len(panels) != 3:
        sys.exit(f"This template needs exactly 3 panels, got {len(panels)}.")
    clips = [ROOT / p["clip"] for p in panels]
    for c in clips:
        if not c.exists():
            sys.exit(f"Missing clip: {c.relative_to(ROOT)}")

    chrome = find_chrome()
    WORK.mkdir(exist_ok=True)
    slug = cfg.get("slug", cfg_path.stem)

    # A grid of stills is the same layout with <img> panels — Chrome renders the
    # whole thing in one shot and there is nothing for ffmpeg to do.
    static_grid = all(c.suffix.lower() in IMAGE_EXTS for c in clips)

    name = f"post-static-{slug}.png" if static_grid else f"post-still-{slug}.png"
    still_html, still_png = WORK / "still.html", ROOT / name
    make_html(cfg, "still", still_html)
    shoot(chrome, still_html, still_png, transparent=False)
    print(f"  {'static' if static_grid else 'still '} -> {still_png.name}")
    if still_only or static_grid:
        return

    if any(c.suffix.lower() in IMAGE_EXTS for c in clips):
        sys.exit("Mixed image and video panels aren't supported — make all three one or the other.")

    # --- chrome layer: transparent, panels hidden ---
    chrome_html, chrome_png = WORK / "chrome.html", WORK / "chrome.png"
    make_html(cfg, "chrome", chrome_html)
    shoot(chrome, chrome_html, chrome_png, transparent=True)

    # Shortest clip wins unless the config pins a duration, so no panel
    # freezes on its last frame while the others keep talking.
    dur = cfg.get("duration") or round(min(probe_duration(c) for c in clips), 2)

    # Audio from one panel only — three voices at once is noise. Set
    # audio_from to null/0/false for a silent build: X autoplays muted, so a
    # grid whose panels carry no dialogue often reads better with no track at
    # all than with one panel's room tone standing in for three.
    raw_audio = cfg.get("audio_from", 1)
    silent = not raw_audio
    a_idx = 0 if silent else int(raw_audio) - 1
    if not silent and not 0 <= a_idx < 3:
        sys.exit("audio_from must be 1, 2, 3 — or null/false for a silent build.")

    scale = (f"scale={PANEL_W}:{PANEL_H}:force_original_aspect_ratio=increase,"
             f"crop={PANEL_W}:{PANEL_H},setsar=1,setpts=PTS-STARTPTS")
    fc = (
        f"[0:v]{scale}[p0];[1:v]{scale}[p1];[2:v]{scale}[p2];"
        f"[p0][p1][p2]hstack=inputs=3[grid];"
        f"[grid][3:v]overlay=0:0,format=yuv420p[v]"
    )
    if not silent:
        fc += (
            f";[{a_idx}:a]afade=t=out:st={max(dur - 0.35, 0):.2f}:d=0.35,"
            f"aresample=48000,asetpts=PTS-STARTPTS[a]"
        )

    final = ROOT / f"format-radar-{slug}.mp4"
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-t", str(dur), "-i", str(clips[0]),
        "-t", str(dur), "-i", str(clips[1]),
        "-t", str(dur), "-i", str(clips[2]),
        "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(chrome_png),
        "-filter_complex", fc,
        "-map", "[v]",
    ]
    if silent:
        cmd += ["-an"]
    else:
        cmd += ["-map", "[a]", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
    cmd += [
        "-c:v", "libx264", "-crf", "19", "-preset", "medium", "-r", str(FPS),
        "-movflags", "+faststart", str(final),
    ]
    run(cmd)
    tail = "silent" if silent else f"audio from panel {a_idx + 1}"
    print(f"  built  -> {final.name}  ({CANVAS_W}x{CANVAS_H}, {dur}s, {tail})")


if __name__ == "__main__":
    main()
