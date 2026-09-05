# SEO hubs (example)

Copy to `context/seo-hubs.md`. The `find-blog-opportunities` skill maps every
keyword opportunity to one of these hubs; anything that maps to none is an
orphan and scores lower on cluster fit. Four hubs is the right number for a
single-product company; more than six means you have two content strategies.

| Hub | Anchor terms | Pillar page | Status |
|---|---|---|---|
| Category head term | ai advertising, ai generated ads | `/ai-advertising` | live |
| Tool intent | ai ad generator, ai ads | `/ad-generator` | live |
| Owned sub-category (the moat) | agentic ai ads, ai ad agent | `/agentic-video-ads` | planned |
| Format intent | ai video ads, ai video ad generator | `/ai-video-ads` | planned |

## Rules
- Each hub has exactly one pillar page. Blogs link up to the pillar; the
  pillar links down to the blogs.
- A keyword belongs to one hub. If it fits two, the hub whose pillar would
  convert better wins.
- `covered-keywords.txt` (in the pipeline's opportunities folder) lists every
  keyword a live page already targets. The engine dedupes against it first.
