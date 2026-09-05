# SEO opportunity engine

Turns a niche into a scored, clustered blog backlog with modeled traffic and
AI-Overview citation potential. Driven by the `find-blog-opportunities` skill;
these scripts are the deterministic parts so the model never has to invent a
number.

```
seed niche ─▶ discover.py ─▶ keyword_metrics.py ─▶ classify_universe.py ─▶ render_backlog.py
               (multi-seed      (volume, KD,          (cluster → hub,          (score, tier,
                expansion +      intent, SERP          main vs secondary)       CSV + markdown)
                sitemap dedupe)  features)
                                        │
                                        ├─▶ citation_score.py      Citation Potential Score 0-100
                                        ├─▶ per_keyword_impact.py  modeled clicks/mo by KD band
                                        └─▶ build_master_table.py  one-page plan for the founder
```

| script | does |
|---|---|
| `discover.py` | expands N seeds via the keyword API, dedupes against your live sitemap and `covered-keywords.txt` so you never propose a page you already have |
| `keyword_metrics.py` | provider waterfall (DataForSEO → Semrush → Ahrefs → WebSearch estimate). Modes `expand` and `metrics`. Degrades to estimates when no key is present and says so in the output |
| `classify_universe.py` | assigns every keyword to a topical hub and marks it main or secondary |
| `render_backlog.py` | deterministic scoring: product relevance, intent fit, winnability, citation potential, cluster fit → opportunity score + tier. Writes CSV + markdown |
| `citation_score.py` | Citation Potential Score = SERP AI-surface presence (AI Overview, People Also Ask, from live SERP features) + format extractability + intent + first-party flags. Config in `config/citation_config.json` |
| `per_keyword_impact.py` | modeled clicks/mo = volume × capture rate by KD band (0-14 → 25%, 15-29 → 12%, 30-44 → 5%, 45+ → 2%). Modeled, not forecast; don't sum synonym variants |
| `build_master_table.py` | one table, one row per page: wave, pillar, funnel, primary keyword, volume, KD, status, why |

## Run

```bash
pip install requests
echo "DATAFORSEO_LOGIN=...\nDATAFORSEO_PASSWORD=..." > pipelines/seo-opportunity-engine/.env   # optional
python pipelines/seo-opportunity-engine/scripts/discover.py --seeds "ai video ads,ai ad generator" --out pipelines/seo-opportunity-engine/opportunities/_candidates.json
python pipelines/seo-opportunity-engine/scripts/render_backlog.py --help
```

Outputs land in `pipelines/seo-opportunity-engine/opportunities/` (gitignored).

## Why it is built this way

- **The model picks, the script scores.** Every number in the backlog comes
  from an API response or a stated formula, so the backlog can be argued
  with.
- **Cannibalization guard first.** Dedupe against the live sitemap before
  scoring; the most common SEO mistake is writing the page you already have.
- **Citation is a separate axis from ranking.** A KD-0 brand-commercial
  keyword that triggers an AI Overview can be worth more than a KD-40 head
  term. The engine surfaces both and lets the human choose.
- **Degrade loudly.** No API key means estimates, labelled as estimates, not
  silence.

In production this produced a 1,300-keyword universe, 18 clusters, a 29-row
master plan and a citation-priority list for one AI-advertising product. The
hubs, pillar pages and covered keywords are configuration, not code.
