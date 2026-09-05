"""Per-keyword impact plan.

For a curated keyword set (mapped to pages), pulls real vol/KD/intent from the
discovered universe and models the impact of ranking:

  modeled monthly clicks = search_volume x capture_rate(KD)

capture_rate models the achievable click share for a *growing* domain once a
page matures (~6-9 mo), baking in achievable SERP position by difficulty:
  KD 0-14  -> 0.25   (can reach top 3)
  KD 15-29 -> 0.12   (page 1, mid)
  KD 30-44 -> 0.05   (page 1 bottom / page 2)
  KD 45+   -> 0.02   (long shot near-term)
  unknown  -> 0.08

Citation / conversion impact + "unlocks" are editorial (set per row). Emits
CSV + Markdown to pipelines/seo-opportunity-engine/opportunities/.
"""
import csv, json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

OUT = Path("pipelines/seo-opportunity-engine/opportunities")
UNI = json.load(open(OUT / "_universe.json", encoding="utf-8"))
LOOK = {(c.get("keyword") or "").lower(): c for c in UNI["candidates"]}

def cap(kd):
    if kd is None: return 0.08
    if kd <= 14: return 0.25
    if kd <= 29: return 0.12
    if kd <= 44: return 0.05
    return 0.02

# curated plan: keyword, page, role, citation, conversion, unlocks
# vol/kd/intent are pulled from the universe (fallback to provided if missing)
P = [
 # keyword, page, role, cite, conv, unlocks, fallback_vol, fallback_kd
 ("ai advertising","/ai-advertising","primary","Med","Med","Anchors the whole AI Advertising cluster; becomes the entity page LLMs cite for 'what is AI advertising'",6600,28),
 ("ai in advertising","/ai-advertising","secondary","Med","Med","Same SERP, KD 12 - easiest path into the 6,600 territory",6600,12),
 ("ai generated advertising","/ai-advertising > AI-Generated Advertising","primary","Med","Med","Mid-funnel guide; generative->agentic narrative bridge",1000,27),
 ("ai advertising campaign","/ai-advertising > AI Ad Campaign","primary","Med","Med","Featured-snippet + how-to; routes to product as campaign engine",170,9),
 ("ai advertising examples","/ai-advertising > 30 Examples","primary","High","Med","Newsjackable listicle; backlink + citation magnet; showcases output",140,0),
 ("ai programmatic advertising","/ai-advertising > Programmatic Explained","primary","Med","Low","KD-0 authority chunk; positions us on creative-supply side",140,0),
 ("generative ai advertising","/ai-advertising > Generative vs Agentic","primary","Med","Med","Sets up the category contrast; feeds the moat",110,17),
 ("ai advertising generator","/ai-advertising > Best AI Advertising Tools","primary","Low","High","BOFU tool intent; 2.4k vol; direct product comparison",2400,49),
 # --- AI Ad Generator ---
 ("ai ads","/ad-generator","primary","Med","High","Head commercial term at KD 18; the BOFU hub",6600,18),
 ("coca-cola ai ads","/ad-generator > Big-Brand AI Ads","primary","High","Med","Newsjack engine: refresh as brands ship AI ads; PR + backlinks",4400,26),
 ("skechers ai ads","/ad-generator > Big-Brand AI Ads","secondary","High","Med","KD 3 at 2,400 vol - near-free ranking",2400,3),
 ("kalshi ai ads","/ad-generator > Big-Brand AI Ads","secondary","High","Med","Trending brand term, 2,400 vol",2400,22),
 ("super bowl ai ads","/ad-generator > Big-Brand AI Ads","secondary","High","Low","Seasonal traffic spike + evergreen refresh",720,6),
 ("ai ads maker","/ad-generator > Best AI Ad Generators","secondary","Low","High","880 vol BOFU; feeds the refresh listicle",880,29),
 ("ai ad generator free","/ad-generator > Best Free AI Ad Generators","primary","Low","High","720 vol KD 14 buy intent; free-tier wedge",720,14),
 ("ai ad copy generator","/ad-generator > AI Ad Copy Generator","primary","Low","Med","Capability page; cross-links to video pillar",110,26),
 # --- AI Video Ads ---
 ("ai video ad generator","/ai-video-ad-generator","primary","Med","High","Core-product category page; the conversion hub for video",320,36),
 ("ai video ads","/ai-video-ad-generator","secondary","Med","High","390 vol; product head term",390,28),
 ("video ad maker","/ai-video-ad-generator > Best AI Video Ad Makers","primary","Low","High","720 vol BOFU; biggest video-intent term",720,26),
 ("ai powered video ads","/ai-video-ad-generator > AI-Powered Video Ads","primary","Med","High","TOP PICK: KD 10, core product, mechanism explainer",320,10),
 ("create video ads with ai","/ai-video-ad-generator > Create Video Ads Step-by-Step","primary","Med","High","Workflow rung; high purchase-readiness",70,23),
 # --- Agentic moat ---
 ("agentic video ads","/agentic-video-ads","primary","High","High","Owns the category definition for LLMs; the entire moat hinges here",0,None),
 ("ai ad agent","/agentic-video-ads","secondary","High","High","480 vol; the only term with demand in the category",480,43),
 ("creative fatigue","/agentic-video-ads > Creative Fatigue","primary","High","Med","the founder POV -> LinkedIn flywheel; AI Overview + PAA already on SERP",140,4),
 # --- AI Ad Creative ---
 ("ad creative ai","/ad-generator > AI Ad Creative","primary","Med","High","3.6k vol at KD 18 - opens the ad-creative sub-cluster (briefs, ideas, strategy)",3600,18),
 ("ad creative brief","/ad-generator > Ad Creative Brief Template","primary","Med","Med","KD 4; downloadable template = link magnet + email capture",140,4),
 ("ad creative ideas","/ad-generator > AI Ad Creative","secondary","Low","Med","Idea-stage demand feeding the creative cluster",140,32),
 # --- UGC ---
 ("ugc ads","/ad-generator > UGC cluster","primary","Med","Med","1,300 vol head; anchors UGC sub-cluster",1300,29),
 ("what are ugc ads","/ad-generator > What Are UGC Ads","primary","Med","Med","Definition gap (live post is how-to only)",210,30),
 ("ugc-style ads","/ad-generator > UGC-Style Ads with AI","primary","Med","Med","KD 0; direct product use case (AI avatars)",90,0),
 # --- AI Commercials (citation play) ---
 ("ai commercial","/ai-advertising > Famous AI Commercials","primary","High","Low","2.4k vol; brand-news listicle = traffic + citation flywheel",2400,16),
 ("progressive ai commercial","/ai-advertising > Famous AI Commercials","secondary","High","Low","KD 0 at 1,600 vol - near-free",1600,0),
 ("liquid death ai commercial","/ai-advertising > Famous AI Commercials","secondary","High","Low","KD 0; viral-brand association",590,0),
 # --- Platform / ICP ---
 ("facebook ads for dropshipping","/dropshipping > FB Ads for Dropshipping","primary","Low","High","KD 0 at 390 vol; ICP wedge into the live dropshipping LP",390,0),
 ("ai facebook advertising","Refresh: How to Create FB Ads with AI","secondary","Low","Med","Refresh boosts an existing ranking page",320,35),
]

rows = []
for kw, page, role, cite, conv, unlocks, fv, fk in P:
    rec = LOOK.get(kw.lower(), {})
    vol = rec.get("search_volume", fv); vol = fv if vol is None else vol
    kd = rec.get("keyword_difficulty", fk); kd = fk if kd is None else kd
    intent = rec.get("search_intent") or "-"
    clicks = round((vol or 0) * cap(kd))
    rows.append({
        "keyword": kw, "vol": vol, "kd": kd, "intent": intent,
        "page": page, "role": role,
        "modeled_clicks_mo": clicks,
        "citation_impact": cite, "conversion_impact": conv,
        "unlocks": unlocks,
    })

# sort by modeled clicks desc (impact)
rows.sort(key=lambda r: r["modeled_clicks_mo"], reverse=True)

# CSV
cols = ["keyword","vol","kd","intent","page","role","modeled_clicks_mo","citation_impact","conversion_impact","unlocks"]
csv_path = OUT / "2026-06-03-per-keyword-impact.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)

# MD table
md = ["| Keyword | Vol | KD | Page it feeds | Role | Modeled clicks/mo | Citation | Conversion | What it unlocks |",
      "|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['keyword']} | {r['vol']} | {r['kd'] if r['kd'] is not None else '-'} | {r['page']} | {r['role']} | {r['modeled_clicks_mo']} | {r['citation_impact']} | {r['conversion_impact']} | {r['unlocks']} |")
(OUT / "_per_keyword_impact.md").write_text("\n".join(md), encoding="utf-8")

total_clicks = sum(r["modeled_clicks_mo"] for r in rows)
print(f"keywords={len(rows)}  total modeled clicks/mo={total_clicks}")
print("csv:", csv_path)
