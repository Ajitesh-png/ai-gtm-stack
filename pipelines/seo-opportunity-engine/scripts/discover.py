"""
Multi-seed discovery driver for find-blog-opportunities.

Expands several seeds at once (via keyword_metrics waterfall), pulls the LIVE
sitemap, and flags each candidate as already-published vs a gap + whether it's
in the cannibalization guard. Emits one consolidated candidates JSON for scoring.

Usage:
    python discover.py \
      --seeds "agentic video ads,ai advertising,ai ad generator,ai video ads,creative fatigue,ugc ads,ai avatar ads" \
      --limit 60 \
      --sitemap https://www.usenotch.ai/sitemap.xml \
      --out pipelines/seo-opportunity-engine/opportunities/_candidates.json

Output JSON: { "live_urls": [...], "candidates": [ {keyword, search_volume,
keyword_difficulty, cpc, search_intent, serp_features, source_seed,
is_published, published_match, covered} ] }
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
import keyword_metrics as km  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
COVERED = ROOT / "pipelines" / "seo-opportunity-engine" / "opportunities" / "covered-keywords.txt"


def fetch_sitemap(url: str) -> list[str]:
    """Fetch a sitemap (handles sitemap-index recursion). Returns all <loc> URLs."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; NotchSEO/1.0)"}
    try:
        r = requests.get(url, headers=headers, timeout=30)
        r.raise_for_status()
    except requests.RequestException as exc:
        print(f"sitemap fetch error: {exc}", file=sys.stderr)
        return []
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", r.text)
    # If this is a sitemap index, recurse into child sitemaps.
    if "<sitemapindex" in r.text:
        urls: list[str] = []
        for child in locs:
            urls.extend(fetch_sitemap(child))
        return urls
    return locs


def url_slug(u: str) -> str:
    path = re.sub(r"https?://[^/]+", "", u).strip("/")
    return path.lower()


def tokens(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def load_covered() -> list[str]:
    if not COVERED.exists():
        return []
    out = []
    for line in COVERED.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(tokens(line))
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--seeds", required=True, help="Comma-separated seeds")
    p.add_argument("--limit", type=int, default=60, help="Ideas per seed")
    p.add_argument("--sitemap", default="https://www.usenotch.ai/sitemap.xml")
    p.add_argument("--location", default="united states")
    p.add_argument("--out", required=True, help="Output candidates JSON path")
    args = p.parse_args()

    loc = km.location_code(args.location)
    seeds = [s.strip() for s in args.seeds.split(",") if s.strip()]

    # --- Live sitemap ---
    live_urls = fetch_sitemap(args.sitemap)
    live_slugs = {url_slug(u) for u in live_urls}
    live_token_blobs = [tokens(s.replace("-", " ").replace("/", " ")) for s in live_slugs]
    print(f"sitemap: {len(live_urls)} live URLs", file=sys.stderr)

    covered = load_covered()

    # --- Expand seeds ---
    by_kw: dict[str, dict] = {}
    provider_used = None
    for seed in seeds:
        res = km.run_waterfall("expand", loc, seed=seed, limit=args.limit)
        provider_used = res.get("provider_used") or provider_used
        for rec in res.get("results", []):
            kw = (rec.get("keyword") or "").strip()
            if not kw:
                continue
            key = kw.lower()
            if key in by_kw:
                continue
            rec["source_seed"] = seed
            by_kw[key] = rec
        print(f"  seed '{seed}': +{len(res.get('results', []))} (total {len(by_kw)})", file=sys.stderr)

    # --- Flag coverage ---
    candidates = []
    for key, rec in by_kw.items():
        kw_tok = tokens(key)
        # Published if a live slug's token blob contains all the keyword tokens
        # (e.g. slug "what-are-agentic-video-ads" covers "agentic video ads").
        published_match = None
        kw_words = set(kw_tok.split())
        for slug, blob in zip(live_slugs, live_token_blobs):
            blob_words = set(blob.split())
            if kw_words and kw_words.issubset(blob_words):
                published_match = slug
                break
        rec["is_published"] = published_match is not None
        rec["published_match"] = published_match
        rec["covered"] = any(
            set(kw_tok.split()) and set(kw_tok.split()).issubset(set(c.split()))
            or set(c.split()) and set(c.split()).issubset(set(kw_tok.split()))
            for c in covered
        )
        candidates.append(rec)

    # Sort by volume desc for readability
    candidates.sort(key=lambda r: (r.get("search_volume") or 0), reverse=True)

    out = {
        "provider_used": provider_used,
        "seeds": seeds,
        "sitemap": args.sitemap,
        "live_url_count": len(live_urls),
        "live_urls": sorted(live_slugs),
        "candidate_count": len(candidates),
        "published_count": sum(1 for c in candidates if c["is_published"]),
        "candidates": candidates,
    }
    Path(args.out).write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(
        json.dumps(
            {
                "provider_used": provider_used,
                "live_urls": len(live_urls),
                "candidates": len(candidates),
                "already_published": out["published_count"],
                "out": args.out,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
