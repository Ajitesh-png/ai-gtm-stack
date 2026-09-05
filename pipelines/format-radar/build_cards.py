#!/usr/bin/env python3
"""
Max Format Radar — render the in-thread explainer cards.

    python build_cards.py            # all cards
    python build_cards.py 3          # just card 3

Each card is a <div class="cardN" id="cardN"> in thread-cards.html with its own
canvas size. The renderer hides every other card, so adding a card means adding
a div plus one row in CARDS.
"""

import re
import sys
from pathlib import Path

from build import find_chrome, run  # shared helpers

ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".work-cards"

# card id -> (template, width, height, output filename)
# Cards sharing a template are isolated by hiding the other #cardN divs.
CARDS = {
    "3":    ("thread-cards.html", 1600, 900, "thread-card-3-the-gap.png"),
    "4":    ("thread-cards.html", 1216, 1080, "thread-card-4-presented-vs-owned.png"),
    "note": ("max-note.html", 1200, 1500, "max-note-killed-your-best-ad.png"),
    "note2": ("max-note-ep02.html", 1200, 1500, "max-note-pressed-the-winner.png"),
    "five": ("thread-cards.html", 1400, 668, "thread-card-five-executions.png"),
    "teardown": ("ad-teardown.html", 1200, 1552, "ad-teardown-three-years.png"),
    "adhero": ("ad-hero.html", 1200, 1290, "ad-hero-oakwash-review.png"),
    "variants": ("ad-variants.html", 1500, 1000, "ad-variants-three-buyers.png"),
    "bracken": ("max-note-bracken.html", 1200, 1500, "max-note-bracken-refused.png"),
    "bracken3": ("ad-variants-bracken.html", 1500, 1000, "ad-variants-bracken-three.png"),
    # halden: build hc1/hc2/hc3 FIRST — the note and ad cards embed their PNGs.
    "hc1": ("creative-halden.html", 1080, 1080, "halden-creative-shelf.png"),
    "hc2": ("creative-halden.html", 1080, 1080, "halden-creative-bag.png"),
    "hc3": ("creative-halden.html", 1080, 1080, "halden-creative-wash.png"),
    "hero-halden": ("ad-hero-halden.html", 1200, 1500, "ad-hero-halden-shelf.png"),
    "note-halden": ("max-note-halden.html", 1200, 1500, "max-note-halden-beforeafter.png"),
    "scan-halden": ("competitor-scan-halden.html", 1400, 1180, "competitor-scan-halden.png"),
    "found-merino": ("found-ad-merino.html", 1200, 700, "found-ad-merino.png"),
    "two-jobs": ("same-number-two-jobs.html", 1600, 800, "same-number-two-jobs.png"),
    "redfern-static": ("redfern-static.html", 1080, 1350, "redfern-static-ad-designed.png"),
    "receipt": ("max-note-receipt.html", 1200, 1500, "max-note-receipt.png"),
    "word": ("max-note-word.html", 1200, 1500, "max-note-word.png"),
    "word2": ("word-growth.html", 1600, 900, "word-growth.png"),
    "word3": ("word-options.html", 1600, 1000, "word-options.png"),
    "word4": ("word-conclusion.html", 1600, 900, "word-conclusion.png"),
}


def main() -> None:
    wanted = [a for a in sys.argv[1:] if a in CARDS] or list(CARDS)
    chrome = find_chrome()
    WORK.mkdir(exist_ok=True)

    for cid in wanted:
        tpl, w, h, out = CARDS[cid]
        html = (ROOT / tpl).read_text(encoding="utf-8")
        html = re.sub(r"--preview:\.\d+", "--preview:1", html)
        html = html.replace("<head>", f'<head>\n<base href="{ROOT.as_uri()}/">', 1)
        siblings = [o for o, spec in CARDS.items() if spec[0] == tpl and o != cid]
        hide = "".join(f"#card{o}{{display:none!important}}" for o in siblings)
        page = re.sub(r"</head>", f"<style>{hide}</style></head>", html, count=1)
        src = WORK / f"card{cid}.html"
        src.write_text(page, encoding="utf-8")
        dest = ROOT / out
        run([
            chrome, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1", f"--window-size={w},{h}",
            "--virtual-time-budget=5000", f"--screenshot={dest}", str(src),
        ])
        if not dest.exists():
            sys.exit(f"Chrome wrote no screenshot for card {cid}.")
        print(f"  card {cid} -> {out}  ({w}x{h})")


if __name__ == "__main__":
    main()
