"""One-off: classify the discovered keyword universe into clusters and rank.

Reads _universe.json, filters junk, buckets keywords into product clusters,
and prints per-cluster: count, total volume, and top keywords (main vs
secondary candidates) with volume/KD, separating live-covered from gaps.
"""
import json, re, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
d = json.load(open("pipelines/seo-opportunity-engine/opportunities/_universe.json", encoding="utf-8"))
C = d["candidates"]

# --- junk filters ---
BRANDS = ["canva","capcut","adobe","veed","invideo","pictory","synthesia","heygen",
 "creatify","arcads","predis","pencil","runway","kling","sora","fliki","lumen5","powtoon",
 "vyond","animoto","clipchamp","crello","descript","elai","colossyan","hourone","deepbrain",
 "steve ai","simplified","hubspot","semrush","jasper","copy.ai","copy ai","opus clip","vidiq",
 "midjourney","dall","chatgpt","gemini","grok","wondershare","filmora","premiere","davinci",
 "renderforest","biteable","flexclip","kapwing","veo","luma","hailuo","pika","pollo","viggle",
 "framer","wix","shopify app"]
OFFPRODUCT = ["free download","mod apk","apk","online free","for youtube","youtube video",
 "for pc","reddit","anime","song","music video"," intro","logo","meme","cartoon","gaming",
 "movie","deepfake","porn","nsfw","girlfriend"," girl","face swap","photo","image generator",
 "text to speech","tts","voice changer","voice clone","singing","rap","lip sync","dance",
 "headshot","profile picture","selfie","baby","pet","resume","essay","story generator",
 "art generator","wallpaper","sticker","emoji","game","minecraft","roblox","course","tutorial pdf"]

def junk(k):
    return any(b in k for b in BRANDS) or any(o in k for o in OFFPRODUCT)

# --- cluster assignment (priority order: first match wins) ---
def cluster(k):
    if "agentic" in k or "ai ad agent" in k: return "Agentic Video Ads"
    if "ugc" in k: return "UGC Ads"
    if "creative fatigue" in k or "ad fatigue" in k or "creative testing" in k: return "Creative Ops (pains)"
    if ("facebook" in k or " fb " in k or k.startswith("fb ")) and "ad" in k: return "Platform: Facebook/Meta"
    if "meta ad" in k or "meta ai" in k: return "Platform: Facebook/Meta"
    if "tiktok" in k: return "Platform: TikTok"
    if "instagram" in k or " ig " in k: return "Platform: Instagram"
    if "advertising" in k: return "AI Advertising"
    if ("video ad" in k) or ("video ads" in k): return "AI Video Ads"
    if "ad generator" in k or ("ad maker" in k): return "AI Ad Generator"
    if "ad creative" in k or "ad copy" in k or "ad script" in k: return "Ad Creative/Copy"
    if "avatar" in k: return "AI Avatar (capability)"
    if "voiceover" in k or "voice over" in k or "voiceover" in k: return "AI Voiceover (capability)"
    if "product video" in k: return "Product Video (capability)"
    if "video edit" in k: return "Video Editing (capability)"
    if "dropship" in k or "ecommerce" in k or "e-commerce" in k or "shopify" in k: return "Ecommerce/Dropshipping"
    if "ai ads" in k or "ai ad " in k or k=="ai ads" or k=="ai ad": return "AI Ad Generator"
    if "ai marketing" in k: return "AI Marketing"
    if "commercial" in k or "brand video" in k: return "AI Commercial/Brand Video"
    return "Other"

buckets = {}
for x in C:
    k = (x["keyword"] or "").lower()
    if not k or junk(k):
        continue
    cl = cluster(k)
    buckets.setdefault(cl, []).append(x)

order = ["AI Advertising","AI Ad Generator","AI Video Ads","Agentic Video Ads","UGC Ads",
 "Creative Ops (pains)","Platform: Facebook/Meta","Platform: TikTok","Platform: Instagram",
 "Ad Creative/Copy","AI Avatar (capability)","AI Voiceover (capability)","Product Video (capability)",
 "Video Editing (capability)","Ecommerce/Dropshipping","AI Marketing","AI Commercial/Brand Video","Other"]

total_kept = sum(len(v) for v in buckets.values())
print(f"KEPT {total_kept} product-relevant keywords (of {len(C)} raw)\n")
print(f"{'CLUSTER':<32}{'#KW':>5}{'SUM VOL':>10}{'MAIN (highest-vol head)':>10}")
print("-"*92)
for cl in order:
    v = buckets.get(cl, [])
    if not v: continue
    v.sort(key=lambda r:(r.get("search_volume") or 0), reverse=True)
    sv = sum((r.get("search_volume") or 0) for r in v)
    main = v[0]
    print(f"{cl:<32}{len(v):>5}{sv:>10}   {main['keyword']} ({main.get('search_volume')}/{main.get('keyword_difficulty')})")

# Detailed top keywords per major cluster (gaps only)
print("\n\n===== TOP UNPUBLISHED KEYWORDS PER CLUSTER (vol>=40) =====")
for cl in order:
    v = [x for x in buckets.get(cl, []) if not x["is_published"] and (x.get("search_volume") or 0)>=40]
    if not v: continue
    v.sort(key=lambda r:(r.get("search_volume") or 0), reverse=True)
    print(f"\n### {cl}  ({len(v)} gap kws)")
    for x in v[:14]:
        print(f"   {x['keyword'][:44]:<45} {x.get('search_volume'):>5}/{str(x.get('keyword_difficulty')):<3} {x.get('search_intent')}")
