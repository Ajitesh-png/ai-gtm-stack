"""
Render a scored blog-opportunity backlog to CSV + Markdown.

The find-blog-opportunities skill does the judgment (it assigns the five
sub-scores per keyword using product context the API can't know). This script
does the deterministic part: sum the sub-scores, assign a tier, sort, and
write both artifacts so output is reproducible and correctly escaped.

Usage:
    python render_backlog.py --input opportunities.json --label agentic-video-gaps

Input JSON: a list of opportunity objects. Required keys per object:
    keyword                (str)
    search_volume          (int | null)
    keyword_difficulty     (float | null)   # 0-100, lower = easier
    search_intent          (str | null)     # informational | commercial | transactional | navigational
    cluster                (str)            # which pillar/hub it strengthens
    suggested_title        (str)
    suggested_angle        (str)
    content_format         (str)            # e.g. listicle, data report, how-to, definition, comparison
    existing_overlap       (str | null)     # URL/slug we already cover, or null
    recommended_pillar_link(str | null)
    data_source            (str)            # dataforseo | semrush | ahrefs | estimated
    notes                  (str | null)
    scores: {
        product_relevance   (0-30),
        intent_fit          (0-20),
        winnability         (0-20),
        citation_potential  (0-15),
        cluster_fit         (0-15)
    }

Output (under pipelines/seo-opportunity-engine/opportunities/):
    {YYYY-MM-DD}-{label}.csv
    {YYYY-MM-DD}-{label}.md
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT_DIR = ROOT / "pipelines" / "seo-opportunity-engine" / "opportunities"

# Sub-score maxima — keep in sync with the SKILL.md scoring rubric.
WEIGHTS = {
    "product_relevance": 30,
    "intent_fit": 20,
    "winnability": 20,
    "citation_potential": 15,
    "cluster_fit": 15,
}

CSV_COLUMNS = [
    "rank",
    "keyword",
    "search_volume",
    "keyword_difficulty",
    "search_intent",
    "product_relevance",
    "intent_fit",
    "winnability",
    "citation_potential",
    "cluster_fit",
    "opportunity_score",
    "tier",
    "cluster",
    "suggested_title",
    "suggested_angle",
    "content_format",
    "existing_overlap",
    "recommended_pillar_link",
    "data_source",
    "notes",
]


def tier_for(score: float) -> str:
    if score >= 75:
        return "A"
    if score >= 55:
        return "B"
    return "C"


def clamp(v, lo, hi):
    try:
        v = float(v)
    except (TypeError, ValueError):
        return 0.0
    return max(lo, min(hi, v))


def score_opportunity(opp: dict) -> dict:
    scores = opp.get("scores") or {}
    total = 0.0
    clamped = {}
    for key, cap in WEIGHTS.items():
        val = clamp(scores.get(key, 0), 0, cap)
        clamped[key] = round(val, 1)
        total += val
    opp["_subscores"] = clamped
    opp["opportunity_score"] = round(total, 1)
    opp["tier"] = tier_for(total)
    return opp


def to_row(opp: dict, rank: int) -> dict:
    sub = opp["_subscores"]
    return {
        "rank": rank,
        "keyword": opp.get("keyword", ""),
        "search_volume": opp.get("search_volume"),
        "keyword_difficulty": opp.get("keyword_difficulty"),
        "search_intent": opp.get("search_intent"),
        "product_relevance": sub["product_relevance"],
        "intent_fit": sub["intent_fit"],
        "winnability": sub["winnability"],
        "citation_potential": sub["citation_potential"],
        "cluster_fit": sub["cluster_fit"],
        "opportunity_score": opp["opportunity_score"],
        "tier": opp["tier"],
        "cluster": opp.get("cluster", ""),
        "suggested_title": opp.get("suggested_title", ""),
        "suggested_angle": opp.get("suggested_angle", ""),
        "content_format": opp.get("content_format", ""),
        "existing_overlap": opp.get("existing_overlap") or "",
        "recommended_pillar_link": opp.get("recommended_pillar_link") or "",
        "data_source": opp.get("data_source", ""),
        "notes": opp.get("notes") or "",
    }


def render_markdown(rows: list[dict], label: str, date: str, meta: dict) -> str:
    a = [r for r in rows if r["tier"] == "A"]
    b = [r for r in rows if r["tier"] == "B"]
    c = [r for r in rows if r["tier"] == "C"]
    estimated = sum(1 for r in rows if r["data_source"] == "estimated")

    lines = [
        f"# Blog Opportunity Backlog — {label}",
        "",
        f"**Generated:** {date}  ",
        f"**Total opportunities:** {len(rows)} "
        f"(Tier A: {len(a)} · Tier B: {len(b)} · Tier C: {len(c)})  ",
        f"**Data source:** {meta.get('provider', 'mixed')} "
        f"({estimated} estimated via WebSearch)  ",
        f"**Seeds:** {meta.get('seeds', '—')}",
        "",
        "> Scored backlog only. Pick rows to write, then feed the chosen "
        "`suggested_title` + `keyword` + `cluster` into Step 2 of the blog "
        "pipeline (image manifest) in `framer-seo/your blog pipeline`.",
        "",
        "**Scoring (0–100):** product relevance (30) · intent fit (20) · "
        "winnability (20) · citation/GEO potential (15) · cluster fit (15). "
        "Tier A ≥75, B 55–74, C <55.",
        "",
    ]

    def section(title: str, group: list[dict]) -> None:
        lines.append(f"## {title}")
        lines.append("")
        if not group:
            lines.append("_None this run._")
            lines.append("")
            return
        lines.append("| # | Keyword | Vol | KD | Intent | Score | Cluster | Suggested title | Format |")
        lines.append("|---|---|---|---|---|---|---|---|---|")
        for r in group:
            lines.append(
                f"| {r['rank']} | {r['keyword']} | "
                f"{r['search_volume'] if r['search_volume'] is not None else '—'} | "
                f"{r['keyword_difficulty'] if r['keyword_difficulty'] is not None else '—'} | "
                f"{r['search_intent'] or '—'} | **{r['opportunity_score']}** | "
                f"{r['cluster']} | {r['suggested_title']} | {r['content_format']} |"
            )
        lines.append("")
        # Angles + overlap notes underneath the table for the writer.
        for r in group:
            note = ""
            if r["existing_overlap"]:
                note = f" ⚠️ overlaps `{r['existing_overlap']}` — refresh/differentiate, don't duplicate."
            lines.append(f"- **{r['keyword']}** — {r['suggested_angle']}{note}")
        lines.append("")

    section("Tier A — write these first", a)
    section("Tier B — strong, queue next", b)
    section("Tier C — backlog / low priority", c)

    lines.append("---")
    lines.append("")
    lines.append(f"_CSV: `pipelines/seo-opportunity-engine/opportunities/{date}-{label}.csv`_")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to opportunities JSON")
    parser.add_argument("--label", required=True, help="Slug for output filenames")
    parser.add_argument("--date", required=True, help="YYYY-MM-DD (pass today's date)")
    parser.add_argument("--provider", default="mixed", help="Provider used this run")
    parser.add_argument("--seeds", default="—", help="Seeds used (for the report header)")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    opps = payload if isinstance(payload, list) else payload.get("opportunities", [])
    if not opps:
        print("No opportunities in input.", file=sys.stderr)
        return 1

    scored = [score_opportunity(dict(o)) for o in opps]
    scored.sort(key=lambda o: o["opportunity_score"], reverse=True)
    rows = [to_row(o, i + 1) for i, o in enumerate(scored)]

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = OUT_DIR / f"{args.date}-{args.label}.csv"
    md_path = OUT_DIR / f"{args.date}-{args.label}.md"

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    meta = {"provider": args.provider, "seeds": args.seeds}
    md_path.write_text(render_markdown(rows, args.label, args.date, meta), encoding="utf-8")

    print(
        json.dumps(
            {
                "csv": str(csv_path),
                "markdown": str(md_path),
                "total": len(rows),
                "tier_a": sum(1 for r in rows if r["tier"] == "A"),
                "tier_b": sum(1 for r in rows if r["tier"] == "B"),
                "tier_c": sum(1 for r in rows if r["tier"] == "C"),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
