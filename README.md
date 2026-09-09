# ai-gtm-stack

**The operating stack I use to run go-to-market for an AI startup with agents instead of a team.** Claude Code skills, slash commands, subagents, deterministic pipelines and an MCP server, sharing one context layer. Built in production for [Notch](https://www.usenotch.ai), an agentic video-ad product for performance marketers, and kept as deployed: the prompts name the real product because generic prompts are worthless. Swap `context/` to re-point every one of them.

[![check](https://github.com/Ajitesh-png/ai-gtm-stack/actions/workflows/check.yml/badge.svg)](https://github.com/Ajitesh-png/ai-gtm-stack/actions/workflows/check.yml)

```
context/    what is true about the product, the buyer, the voice     (you fill in)
skills/     multi-step procedures Claude Code runs on a trigger phrase
commands/   slash commands: /founder-voice-reply /advet /find-leads /content-routine /content-saturation-simulator
agents/     subagents for research, scouting, scripting, lead-finding
pipelines/  the deterministic parts: SEO opportunity engine, format-radar builder, lead enrichment
mcp/        competitor-radar (separate repo)
playbooks/  the ad-craft documents the agents are grounded in
docs/       architecture, case studies
```

## What is in here

### Intelligence: what the market is telling our buyers
| artifact | does |
|---|---|
| [competitor-radar MCP](https://github.com/Ajitesh-png/competitor-radar-mcp) | scrapes competitor X accounts, rates every post per day by replies → bookmarks → retweets → likes, scores ICP relevance |
| [Scrapling MCP + skill](mcp/README.md) (third-party) | the scraping layer for everything that is not X: stealth fetches through Cloudflare, JavaScript rendering, CSS-narrowed markdown. The scouts, the analyst and the lead finder fall back to it when a plain fetch fails |
| `agents/format-scout` | reverse-engineers the *format* mechanics of winning posts in the category, scores them for our ICP, maps each to an ownable angle |
| `agents/content-scout` | finds fresh high-engagement posts, deconstructs hook + structure + trigger, adapts the mechanism (never the copy) to our product |
| `agents/content-engagement-analyst` | strict freshness + engagement-rate filters across X, LinkedIn, Reddit; six-dimension deconstruction; QA gate before anything is stored |
| `agents/content-saturation-simulator` + `/content-saturation-simulator` | models the buyer's feed, scores saturation on 12 dimensions, finds the break vectors; rates a hook DEAD → VIRGIN |

### Content production
| artifact | does |
|---|---|
| `skills/x-content-playbook` | performance-grounded rules from a full-population teardown of a founder account: pick the target metric first, four hook families, the CTA decision table, the outlier rule ([case study](docs/case-studies/x-post-performance-teardown.md)) |
| `skills/launch-post` | the locked launch-post structure (S1 specificity + gap, S2 widens, S3 takes), a hook-mechanics library with shipped examples, a 3–10 round iteration protocol, and the creator amplification brief |
| `skills/format-radar` + `pipelines/format-radar` | one episode of a recurring series: find a trending ad format, deconstruct it, decide where it is burned and where it is open, rebuild it for our ICP, generate the scenes, build the 1080×1920 post video, write the thread |
| `agents/ad-breakdown` | weekly "breaks down an ad" pillar: source → why it works → blueprint → recreate the asset via Higgsfield → package |
| `/content-routine` | research sweep → 3–5 post packages channelling a named desire from the desire map → a 20-angle bank, in the house format |
| `/founder-voice-reply` | replies in the founder's voice from `context/voice-profile.md`; finds the angle only they could see; refuses to run without a real profile |

### Demand
| artifact | does |
|---|---|
| `skills/find-blog-opportunities` + `pipelines/seo-opportunity-engine` | niche → keyword universe → cluster → score (relevance, intent, winnability, citation potential, cluster fit) → tiered backlog. Cannibalization guard against the live sitemap first. AI-Overview citation potential scored as its own axis |
| `agents/lead-finder` + `/find-leads` + `pipelines/lead-finder` | natural-language request → ICP segment + sourcing strategy → enrich via provider waterfall → QA against the competitor skip list → canonical CSV with an intent signal on every row |
| `agents/outreach-specialist` | ICP definition, tiered qualification rubric, prospect sourcing plan, list QA |

### Paid-media craft
| artifact | does |
|---|---|
| `/advet` | a 10-year media buyer across Meta, TikTok, Instagram: tactical, spend-aware, platform-specific; saves every tactic it teaches to `knowledge/` |
| `agents/ugc-script-architect` | trending UGC format breakdowns with real brand examples and production-ready 90-second scripts |
| `playbooks/winning-ad-production-system.md` | the anatomy of a converting ad: hook types by audience, body structures, close mechanics |
| `playbooks/segment-level-ad-format-research.md` | which formats win at cold, warm and hot, and why |

## Install

```bash
git clone https://github.com/Ajitesh-png/ai-gtm-stack
cd ai-gtm-stack
python install.py --project /path/to/your/repo      # or --user
```

Then fill the context layer. Each file has a `.example` next to it:

```
context/product.md               what you sell, in your words
context/icp.json                 who buys, per segment
context/voice-profile.md         the founder, specifically
context/competitor-skip-list.md  who never gets a cold email
context/watchlist.md             whose posts to study
context/proof-points.md          the only numbers allowed in copy
context/desire-map.md            the desires and fears posts may channel
context/post-structure.md        the loop law
context/post-format.md           the house format
context/seo-hubs.md              the four topical hubs
```

Two third-party pieces the intelligence layer expects, both optional: the
[competitor-radar MCP](https://github.com/Ajitesh-png/competitor-radar-mcp) and
[Scrapling](mcp/README.md) (its MCP server plus the author's `scrapling-official`
skill: `npx skills add D4Vinci/Scrapling --skill scrapling-official`). Without
them the scouts still run on WebFetch; they just fail more often on protected sites.

Restart Claude Code. `/advet how should I structure a $30k/mo Meta account for a skincare DTC brand` is a good first run; `/content-routine` is a good second.

## Principles the stack is built on

- **Pick the metric before the line.** Reach, replies and saves have different levers and are nearly independent. A post that does not know which it wants gets none.
- **No invented numbers.** Every figure traces to `context/proof-points.md`, a demo, or the user. Otherwise it is a `[slot]`.
- **Lead with mechanism, never the category label.** "AI growth marketer" arrives as the explanation, not the opener.
- **The model picks, the script scores.** Scoring, deduping, enrichment and rating are deterministic and inspectable. Judgment stays in the prompt.
- **Fresh only, verified or flagged.** Intelligence agents work on 7–14 day windows and mark anything they could not confirm `UNVERIFIED`.
- **Skip more than you post.** Every engine is designed to refuse. Quiet is a valid output.
- **Rules carry their evidence.** The X playbook cites the posts each rule came from and expires quarterly. Format-radar guardrails name the episode that taught them.
- **Confidential stays out of the repo.** Voice, ICP, competitor intel and customer numbers live in `context/` and `knowledge/`, both gitignored. `scripts/check.py` fails CI on any local path or secret-shaped string.

## Results

The product this stack runs growth for, as of 2026:

| | |
|---|---|
| **4,000+** | marketers running paid social through the product across Meta and TikTok |
| **40,000+** | ads generated on the platform |

Those are platform numbers; the stack is the growth machinery behind them, operated by one person. What the machinery itself produced in 2026:

- An autonomous competitor radar that rates every competitor post, every day, and separates engagement from buyer relevance.
- A 1,300-keyword SEO universe collapsed into 18 clusters, a 29-row content plan, a per-keyword impact model and a citation-priority list for AI Overviews; four waves of blogs published with generated imagery.
- A measured X playbook, built from a full-population teardown, that changed how every post is written: target metric first, gated CTAs, dated rules that expire quarterly.
- A weekly ad-format series that finds, deconstructs, rebuilds and renders the post video without an editor.
- A lead pipeline that writes CSVs with an intent signal on every row and has never emailed a competitor.

Per-customer performance numbers are deliberately absent. The methods are all here; the two figures above are the only ones approved for public use, per the same rule the stack enforces on itself.

Not in this repo, by design: the autonomous X reply engine (it carries the founder's voice profile and the ICP config and is not yet separable), the email sequences, and anything with customer data.

## Layout

See [docs/architecture.md](docs/architecture.md) for the diagram and the conventions every artifact follows. MIT licensed.
