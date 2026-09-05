"""Emit the one-page master content plan as CSV (for Sheets) + Markdown table."""
import csv, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")

OUT = Path("pipelines/seo-opportunity-engine/opportunities")
OUT.mkdir(parents=True, exist_ok=True)

# wave, pillar, title, type, funnel, primary_kw, vol, kd, secondary, status, cite, why
ROWS = [
 # ---- WAVE 1: PILLAR PAGES (build the hubs) ----
 ["1","AI Advertising","/ai-advertising","Pillar LP","TOFU","ai advertising","6600","28","ai in advertising (6600/12), ai for advertising (390)","Build","Med","Biggest open territory on the web; no page exists"],
 ["1","AI Ad Generator","/ad-generator","Pillar LP","TOFU/BOFU","ai ads","6600","18","ai ad generator (head)","Optimize","Med","Live page; add definition+FAQ, link to cluster"],
 ["1","AI Video Ads","/ai-video-ad-generator","Pillar LP","TOFU","ai video ad generator","320","36","ai video ads (390/28), video ad maker (720/26)","Build","Med","Core product category, no page"],
 ["1","Agentic Video Ads","/agentic-video-ads","Category Pillar","Category","agentic video ads","0","-","ai ad agent (480/43)","Build","High","Category we're creating; win LLM citations, not traffic"],
 # ---- WAVE 2: INDEXING FIX ----
 ["2","Alternatives","/alternative/* (6 pages)","Fix indexing","BOFU","creatify/arcads/heygen alternative","-","-","built but not in sitemap","Fix","-","Free buy-intent traffic already built; add to sitemap+schema"],
 # ---- WAVE 3: KD-0-14 QUICK WINS (rank fast + cited) ----
 ["3","AI Ad Generator","Every Big-Brand AI Ad (Coca-Cola, Skechers, Super Bowl)","Blog (listicle)","MOFU","coca-cola ai ads","4400","26","skechers ai ads (2400/3), kalshi (2400/22), super bowl ai ads (720/6)","Build","High","Citation goldmine: huge vol at KD 3-26; ends 'make your own'"],
 ["3","AI Commercials","Famous AI Commercials (2026)","Blog (listicle)","MOFU","ai commercial","2400","16","progressive (1600/0), liquid death (590/0), trivago (480/0), super bowl ai commercial (590)","Build","High","Brand-news terms at KD 0; traffic + citation magnet"],
 ["3","AI Video Ads","AI-Powered Video Ads: How They Actually Work","Blog (how-to)","MOFU","ai powered video ads","320","10","ai video advertising (390/12)","LIVE","Med","TOP PICK: core product, KD 10 | published 2026-06-03"],
 ["3","Agentic Video Ads","Creative Fatigue: Why Your Meta Ads Stop Working","Blog (POV)","MOFU","creative fatigue","140","4","ad creative testing (70/0)","LIVE","High","the founder 9yr-Meta POV; SERP has AI Overview + PAA | published 2026-06-03"],
 ["3","AI Advertising","30 Real AI Advertising Examples (2026)","Blog (listicle)","MOFU","ai advertising examples","140","0","ai in advertising examples (110/0)","LIVE","High","KD 0, citation magnet, showcases output | published 2026-06-03"],
 ["3","AI Advertising","What Is an AI Ad Campaign? (+ How to Run One)","Blog (definition)","MOFU","ai advertising campaign","170","9","ai advertising campaigns (170/1)","Build","Med","KD 9; wins featured snippet"],
 ["3","AI Advertising","AI Programmatic Advertising, Explained","Blog (definition)","MOFU","ai programmatic advertising","140","0","programmatic advertising ai (140/3)","Build","Med","KD 0 quick win"],
 ["3","UGC Ads","UGC-Style Ads: Faking Authentic with AI","Blog (how-to)","MOFU","ugc-style ads","90","0","ugc style ads (90/0), ugc ads examples (50/0)","Build","Med","KD 0, direct product use case"],
 ["3","AI Ad Creative","Ad Creative Brief Template (+ AI generator)","Blog (template)","MOFU","ad creative brief","140","4","ad creative brief template (70/3)","Build","Med","KD 4, template = linkable asset"],
 ["3","Ecommerce/DTC","Facebook Ads for Dropshipping (with AI)","Blog (how-to)","MOFU/BOFU","facebook ads for dropshipping","390","0","dropshipping ads (210/14)","Build","Low","KD 0, ICP-perfect (live dropshipping page)"],
 # ---- WAVE 4: MID-FUNNEL VOLUME ----
 ["4","AI Ad Creative","AI Ad Creative: How to Generate Winning Creative","Blog (how-to)","MOFU","ad creative ai","3600","18","ai ad creative (170/18), ad creative ideas (140/32)","Build","Med","3.6k vol at KD 18 = strong mid-funnel"],
 ["4","AI Advertising","AI-Generated Advertising: How Brands Use It (2026)","Blog (guide)","MOFU","ai generated advertising","1000","27","ai-generated advertising (1000/32)","Build","Med","1k vol, generative->agentic bridge"],
 ["4","UGC Ads","What Are UGC Ads? (+ How to Make Them with AI)","Blog (definition)","MOFU","what are ugc ads","210","30","ugc ads meaning (170/32), ugc ads (1300/29 head)","LIVE","Med","Definition gap (live post is how-to only) | published 2026-06-03"],
 ["4","AI Ad Generator","AI Ad Copy Generator: How It Works","Blog (how-to)","MOFU","ai ad copy generator","110","26","-","Build","Low","Capability -> product bridge"],
 ["4","AI Video Ads","How to Create Video Ads with AI, Step by Step","Blog (how-to)","MOFU","create video ads with ai","70","23","ai generated video ads (70/22)","Build","Med","Workflow rung of video ladder"],
 ["4","AI Advertising","Generative AI vs Agentic Advertising","Blog (compare)","MOFU","generative ai advertising","110","17","ai driven advertising (90/16)","Build","Med","Bridges to the moat"],
 # ---- WAVE 5: BOFU + REFRESH ----
 ["5","AI Ad Generator","Best Free AI Ad Generators (2026)","Blog (listicle)","BOFU","ai ad generator free","720","14","free ai ad generator (480/16)","Build","Low","720 vol, KD 14, buy intent"],
 ["5","AI Video Ads","Best AI Video Ad Makers (2026)","Blog (listicle)","BOFU","video ad maker","720","26","ai video ads maker (140/33)","Build","Low","720 vol, BOFU"],
 ["5","AI Ad Generator","Best AI Ad Generators (2026)","Refresh","BOFU","best ai ad generator","260","37","ai ads maker (880/29)","Refresh","Low","Refresh live 2025 top-5 post; kill '2025'"],
 ["5","AI Advertising","Best AI Advertising Tools (2026)","Blog (listicle)","BOFU","ai advertising generator","2400","49","best ai advertising generator (260/37)","Build","Low","2.4k vol BOFU"],
 ["5","Platform: FB/Meta","AI for Facebook Ads","Refresh","MOFU","ai facebook advertising","320","35","ai for facebook ads (320/30), meta ai ads (480/58)","Refresh","Low","Refresh live FB how-to post"],
 # ---- WAVE 6: MOAT / CITATION (uncopyable) ----
 ["6","Agentic Video Ads","We Analyzed 1,000 Agentic Video Ads","Blog (data report)","MOFU","(first-party data)","0","-","-","Build","High","#1 citation magnet; original data"],
 ["6","Agentic Video Ads","How to Create 30 Video Ads in One Go","Blog (product-led)","BOFU","(no search volume)","0","-","-","Build","High","Demand we create, not capture; product demo + citation"],
 ["6","Agentic Video Ads","Claude Code, But for Video Ads","Blog (analogy)","MOFU","(adjacent agentic demand)","0","-","-","Build","Med","Captures agentic/builder audience"],
]

HEADERS = ["Wave","Pillar/Cluster","Page / Blog","Type","Funnel","Primary keyword","Vol","KD","Secondary keywords","Status","Cite","Why / priority"]

# CSV
csv_path = OUT / "2026-06-03-master-content-plan.csv"
with csv_path.open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(HEADERS)
    w.writerows(ROWS)

# Markdown table
md = ["| " + " | ".join(HEADERS) + " |", "|" + "|".join(["---"]*len(HEADERS)) + "|"]
for r in ROWS:
    md.append("| " + " | ".join(r) + " |")
md_path = OUT / "_master_table.md"
md_path.write_text("\n".join(md), encoding="utf-8")

# Stats
from collections import Counter
waves = Counter(r[0] for r in ROWS)
build = sum(1 for r in ROWS if r[9]=="Build")
print(f"rows={len(ROWS)} build={build} refresh={sum(1 for r in ROWS if r[9]=='Refresh')}")
print("by wave:", dict(sorted(waves.items())))
print("csv:", csv_path)
print("md :", md_path)
