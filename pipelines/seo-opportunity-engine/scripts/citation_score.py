"""Citation Potential Scorer (GEO).

Ranks planned pages by how likely AI engines (Perplexity / ChatGPT /
Google AI Overviews) will cite them. CPS 0-100 combines:

  - SERP AI surface   (auto, from DataForSEO serp_features of the primary kw):
                       ai_overview / people_also_ask / featured_snippet present
                       => the query is already AI-answered, sources get pulled
  - Format            (editorial): data report / examples / definition extract best
  - Intent            (auto): informational gets cited more than transactional
  - First-party data  (flag): original research = #1 citation magnet
  - Named expert      (flag): the founder attribution; LLMs favor named sources
  - Brand entity      (flag): brand-name queries pulled into "brands using X" answers

Config + per-page flags: pipelines/seo-opportunity-engine/config/citation_config.json
Data: pipelines/seo-opportunity-engine/opportunities/_universe.json (serp_features + intent)

Output: ranked CSV + Markdown in pipelines/seo-opportunity-engine/opportunities/.
"""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "pipelines" / "seo-opportunity-engine" / "opportunities"
CFG = json.load(open(ROOT / "pipelines" / "seo-opportunity-engine" / "config" / "citation_config.json", encoding="utf-8"))
UNI = json.load(open(OUT / "_universe.json", encoding="utf-8"))
LOOK = {(c.get("keyword") or "").lower(): c for c in UNI["candidates"]}
W = CFG["weights"]


def capped(val, cap):
    return min(val, cap)


def score_page(p):
    kw = (p.get("primary_kw") or "").lower()
    rec = LOOK.get(kw, {}) if kw else {}
    feats = rec.get("serp_features") or []
    intent = rec.get("search_intent") or ("informational" if not kw else "-")

    # 1. SERP AI surface
    sa = W["serp_ai_surface"]
    surface = 0
    detail = []
    for f in ("ai_overview", "people_also_ask", "featured_snippet", "discussions_and_forums"):
        if f in feats:
            surface += sa.get(f, 0)
            detail.append(f)
    surface = capped(surface, sa["_cap"])

    # 2. Format
    fmt = capped(W["format_extractability"].get(p["format"], 0), W["format_extractability"]["_cap"])

    # 3. Intent
    intent_score = capped(W["intent"].get(intent, 0), W["intent"]["_cap"])

    # 4-6. Flags
    fp = W["first_party_data"] if p.get("first_party_data") else 0
    ne = W["named_expert"] if p.get("named_expert") else 0
    be = W["brand_entity"] if p.get("brand_entity") else 0

    cps = surface + fmt + intent_score + fp + ne + be
    return {
        "page": p["page"], "cluster": p.get("cluster", ""),
        "primary_kw": p.get("primary_kw") or "(no search demand)",
        "vol": rec.get("search_volume"), "kd": rec.get("keyword_difficulty"),
        "format": p["format"], "intent": intent,
        "serp_ai_surface": surface, "ai_signals": ",".join(detail) or "-",
        "format_score": fmt, "intent_score": intent_score,
        "first_party": fp, "expert": ne, "brand": be,
        "CPS": cps,
    }


def tier(cps):
    if cps >= CFG["tiers"]["A"]:
        return "A"
    if cps >= CFG["tiers"]["B"]:
        return "B"
    return "C"


rows = [score_page(p) for p in CFG["pages"]]
for r in rows:
    r["tier"] = tier(r["CPS"])
rows.sort(key=lambda r: r["CPS"], reverse=True)

cols = ["rank", "page", "cluster", "CPS", "tier", "primary_kw", "vol", "kd", "format",
        "intent", "serp_ai_surface", "ai_signals", "format_score", "intent_score",
        "first_party", "expert", "brand"]
csv_path = OUT / "2026-06-03-citation-priority.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols)
    w.writeheader()
    for i, r in enumerate(rows, 1):
        w.writerow({"rank": i, **{k: r.get(k) for k in cols if k != "rank"}})

# Markdown
md = ["| # | Page | CPS | Tier | Primary kw (vol/KD) | Format | AI surface signals | Why citable |",
      "|---|---|---|---|---|---|---|---|"]
def why(r):
    bits = []
    if r["ai_signals"] != "-": bits.append(r["ai_signals"].replace(",", " + "))
    if r["first_party"]: bits.append("first-party data")
    if r["expert"]: bits.append("the founder expert")
    if r["brand"]: bits.append("brand-entity query")
    return "; ".join(bits) or r["format"]
for i, r in enumerate(rows, 1):
    vk = f"{r['vol']}/{r['kd']}" if r["vol"] is not None else "—"
    md.append(f"| {i} | {r['page']} | **{r['CPS']}** | {r['tier']} | {r['primary_kw']} ({vk}) | {r['format']} | {r['ai_signals']} | {why(r)} |")
(OUT / "_citation_priority.md").write_text("\n".join(md), encoding="utf-8")

a = sum(1 for r in rows if r["tier"] == "A")
b = sum(1 for r in rows if r["tier"] == "B")
print(f"pages={len(rows)}  Tier A={a}  Tier B={b}  Tier C={len(rows)-a-b}")
print(f"top 5: " + " | ".join(f"{r['page'][:28]} ({r['CPS']})" for r in rows[:5]))
print("csv:", csv_path)
