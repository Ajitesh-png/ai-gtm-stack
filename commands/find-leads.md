---
description: Find and enrich high-intent leads for Notch outreach. Invokes the lead-finder agent with parsed parameters.
---

# /find-leads

Find and enrich leads for Notch outreach. Wraps the `lead-finder` subagent for common patterns.

## Usage

Free-form (most common):
```
/find-leads find me 100 DTC founders posting about creative fatigue this week
```

Parameterized (for repeatable runs):
```
/find-leads icp=dropshipper_dtc count=100 source=topic:"creative fatigue" platform=linkedin
/find-leads icp=ai_saas_b2c count=50 source=apollo
/find-leads source=post:https://linkedin.com/posts/... count=all
/find-leads source=csv:path/to/file.csv mode=enrich
```

## Parameters (when using key=value form)

| Param | Values | Default |
|---|---|---|
| `icp` | `ai_saas_b2c` \| `mobile_gaming_ua` \| `affiliate_cpa` \| `dropshipper_dtc` \| `custom` | inferred from request |
| `count` | integer \| `all` | 50 |
| `source` | `post:URL` \| `apollo` \| `linkedin_search` \| `twitter_search` \| `topic:"..."` \| `followers_of:@handle` \| `csv:PATH` | inferred |
| `platform` | `linkedin` \| `x` \| `both` | `both` |
| `mode` | `find` \| `enrich` (skip phase 2 sourcing) | `find` |
| `dedup_against` | path to prior CSV | `leads/seen_profile_urls.txt` |
| `label` | custom slug for output filename | auto-generated |

## What this does

Invokes the `lead-finder` subagent with your request. The agent runs a 5-phase pipeline:

1. **Parse** the request → map to ICP segment + sourcing strategy
2. **Source** raw leads via scraper (Apify if installed) or WebFetch/WebSearch fallback
3. **Enrich** with first_name, last_name, email, company, title, intent signal
4. **QA** against the competitor skip list + dedup file
5. **Output** canonical CSV to `leads/YYYY-MM-DD-{label}.csv` + run report

Default output is **CSV only**. The agent will NOT push to HeyReach or Instantly without an explicit second confirmation.

## Agent reference

Full agent prompt: `agents/lead-finder.md`

Knows the product (Notch Agentic Video Ads), the 4 ICP profiles (`context/icp.json`), and the competitor skip list (`context/competitor-skip-list.md`).

## Output CSV schema

```
first_name, last_name, email, company, title, linkedin_url, twitter_url,
intent_signal, source, source_post_url, icp_segment, icp_tier, status, scraped_at, notes
```

Status values: `KEEP_A`, `KEEP_B`, `KEEP_C`, `SKIP_COMPETITOR`, `SKIP_DUPLICATE`, `NEEDS_ENRICHMENT`.

## Common patterns

```
# Extract commenters from a specific post
/find-leads source=post:https://www.linkedin.com/posts/calebkrusemedia_xxx count=all

# Find DTC operators posting about creative fatigue
/find-leads icp=dropshipper_dtc count=100 source=topic:"creative fatigue"

# Apollo search for AI SaaS Head of Growth
/find-leads icp=ai_saas_b2c count=50 source=apollo

# Re-enrich an existing CSV (no new sourcing)
/find-leads source=csv:leads/<prior-run>.csv mode=enrich
```

## Notes

- Always confirms the parse before sourcing unless the run is an unambiguous re-run.
- Surfaces tool gaps in the run report (e.g., "Apify not installed, fell back to WebFetch — title coverage limited").
- Always cross-checks the competitor skip list before output. Marks competitor employees/founders as `SKIP_COMPETITOR`.
- Always updates `leads/seen_profile_urls.txt` after run to prevent re-touching the same leads.
- Never invents data. Missing fields are flagged for downstream Clay/manual enrichment, not filled with guesses.
