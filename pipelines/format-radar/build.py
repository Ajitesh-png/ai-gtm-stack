#!/usr/bin/env python3
"""
Max Format Radar — episode builder.

Reads episode.json, renders the post plates with headless Chrome, and
composites a multi-scene 1080x1920 MP4 with per-scene burned subtitles.

    python build.py                    # build episode.json
    python build.py other-episode.json
    python build.py --still            # just the still PNG (for thread posts 3-4)

Layering per scene:
    plate.png (everything but the video pixels and the burned text)
      + the clip segment, scaled/cropped to 614x1092 at (392, 452)
      + scene-N.png (transparent: question card + that scene's subtitle)

Requires: Chrome, ffmpeg on PATH.
"""

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".work"
TEMPLATE = ROOT / "post-template.html"

# Output frame geometry — must match .output in post-template.html
FRAME_X, FRAME_Y, FRAME_W, FRAME_H = 392, 452, 614, 1092
CANVAS_W, CANVAS_H = 1080, 1920
FPS = 30

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
]


def find_chrome() -> str:
    for c in CHROME_CANDIDATES:
        if Path(c).exists() or shutil.which(c):
            return c
    sys.exit("Chrome not found. Add your binary to CHROME_CANDIDATES.")


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(str(c) for c in cmd[:3])}...\n{r.stderr[-1500:]}")
    return r


def make_html(cfg: dict, mode: str, dest: Path) -> None:
    """Write a render-ready copy of the template with the config injected.

    mode 'plate' hides the video pixels and burned text; mode 'scene' renders
    a transparent overlay carrying only the question card and subtitle. Both
    are driven by body[data-mode] rules already in the template.
    """
    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("--preview:.42", "--preview:1")
    # Anchor to line start: a loose "<body>" replace also matches the string
    # inside the stylesheet comments.
    html, n = re.subn(r"^<body>", f'<body data-mode="{mode}">', html, count=1, flags=re.M)
    if n != 1:
        sys.exit("Could not find the <body> tag at line start in post-template.html.")
    # Render copies live in .work/, so relative asset paths would resolve one
    # level too deep. Pin them back to the project root.
    html = html.replace("<head>", f'<head>\n<base href="{ROOT.as_uri()}/">', 1)
    html = re.sub(
        r'(<script id="episode" type="application/json">).*?(</script>)',
        lambda m: m.group(1) + "\n" + json.dumps(cfg, ensure_ascii=False, indent=2) + "\n" + m.group(2),
        html,
        flags=re.S,
    )
    dest.write_text(html, encoding="utf-8")


def shoot(chrome: str, html: Path, png: Path, transparent: bool = False) -> None:
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
        sys.exit(f"Chrome wrote no screenshot for {html.name} (check write permissions on {png.parent}).")


def has_audio(clip: Path) -> bool:
    """True if the clip carries an audio stream.

    Clips generated with `sound: "off"` have none, and the audio filter chain
    below then fails with 'Stream specifier :a matches no streams'. A silent
    demonstration ad (no dialogue) is a legitimate episode shape, so detect
    rather than assume.
    """
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", str(clip)],
        capture_output=True, text=True,
    )
    return bool(out.stdout.strip())


def build_segment(plate: Path, scene_png: Path, clip: Path, t_in: float, t_out: float, out: Path) -> None:
    """One scene: plate + clip segment in the frame + scene overlay."""
    dur = round(t_out - t_in, 3)
    if dur <= 0:
        sys.exit(f"Scene has non-positive duration ({t_in} -> {t_out}) for {clip.name}.")
    # setpts is load-bearing: -ss input seeking leaves the clip's PTS at its
    # source offset, so without this the overlay never lands inside the
    # segment's time window and the frame renders empty.
    fc = (
        f"[1:v]scale={FRAME_W}:{FRAME_H}:force_original_aspect_ratio=increase,"
        f"crop={FRAME_W}:{FRAME_H},setsar=1,setpts=PTS-STARTPTS[vid];"
        f"[0:v][vid]overlay={FRAME_X}:{FRAME_Y}[bg];"
        f"[bg][2:v]overlay=0:0,format=yuv420p[v]"
    )
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(plate),
        "-ss", str(t_in), "-t", str(dur), "-i", str(clip),
        "-loop", "1", "-framerate", str(FPS), "-t", str(dur), "-i", str(scene_png),
    ]
    if has_audio(clip):
        fc += (
            f";[1:a]afade=t=in:st=0:d=0.06,afade=t=out:st={max(dur - 0.10, 0):.3f}:d=0.10,"
            f"aresample=48000,asetpts=PTS-STARTPTS[a]"
        )
        cmd += ["-filter_complex", fc, "-map", "[v]", "-map", "[a]"]
        tail = ["-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]
    else:
        # Silent source: emit a silent AAC track anyway so every segment has the
        # same stream layout — the concat demuxer refuses a mix of with/without.
        cmd += [
            "-f", "lavfi", "-t", str(dur), "-i", "anullsrc=r=48000:cl=stereo",
            "-filter_complex", fc, "-map", "[v]", "-map", "3:a",
        ]
        tail = ["-c:a", "aac", "-b:a", "96k", "-ar", "48000", "-ac", "2"]
    cmd += ["-c:v", "libx264", "-crf", "18", "-preset", "medium", "-r", str(FPS)]
    cmd += tail + [str(out)]
    run(cmd)


def main() -> None:
    args = [a for a in sys.argv[1:]]
    still_only = "--still" in args
    args = [a for a in args if not a.startswith("--")]
    cfg_path = ROOT / (args[0] if args else "episode.json")
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))

    scenes = cfg.get("scenes", [])
    if not scenes:
        sys.exit("episode.json has no scenes.")

    for s in scenes:
        if not (ROOT / s["clip"]).exists():
            sys.exit(f"Missing clip: {s['clip']}")

    chrome = find_chrome()
    WORK.mkdir(exist_ok=True)
    slug = cfg.get("slug", cfg_path.stem)

    # --- the still: scene 1's copy, full opaque page. Used for thread posts. ---
    still_cfg = dict(cfg, preview_clip=scenes[0]["clip"], preview_subtitle=scenes[0]["subtitle"])
    still_html = WORK / "still.html"
    still_png = ROOT / f"post-still-{slug}.png"
    make_html(still_cfg, "still", still_html)
    shoot(chrome, still_html, still_png)
    print(f"  still   -> {still_png.name}")
    if still_only:
        return

    # --- background plate: rendered once, reused by every scene ---
    plate_html, plate_png = WORK / "plate.html", WORK / "plate.png"
    make_html(cfg, "plate", plate_html)
    shoot(chrome, plate_html, plate_png)

    # --- one overlay + one segment per scene ---
    segments = []
    for i, s in enumerate(scenes, start=1):
        scene_cfg = dict(cfg, preview_subtitle=s["subtitle"])
        scene_html, scene_png = WORK / f"scene{i}.html", WORK / f"scene{i}.png"
        make_html(scene_cfg, "scene", scene_html)
        shoot(chrome, scene_html, scene_png, transparent=True)

        seg = WORK / f"seg{i}.mp4"
        build_segment(plate_png, scene_png, ROOT / s["clip"], float(s["in"]), float(s["out"]), seg)
        segments.append(seg)
        print(f"  scene {i} -> {round(float(s['out']) - float(s['in']), 2)}s  {s['subtitle'][:44]}")

    # --- concat ---
    listing = WORK / "concat.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in segments), encoding="utf-8")
    final = ROOT / f"format-radar-{slug}.mp4"
    run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
        "-c:v", "libx264", "-crf", "18", "-preset", "medium",
        "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(final),
    ])

    total = sum(float(s["out"]) - float(s["in"]) for s in scenes)
    print(f"\n  built   -> {final.name}  ({len(scenes)} scenes, {total:.1f}s)")


if __name__ == "__main__":
    main()
