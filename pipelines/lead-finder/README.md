# Lead finder: enrichment helper

Deterministic half of the `lead-finder` agent and the `/find-leads` command.
The agent decides the sourcing strategy, reads the ICP profile and the
competitor skip list, and QAs the output; `enrich.py` fills the row.

```bash
python pipelines/lead-finder/enrich.py --linkedin-url https://linkedin.com/in/example
python pipelines/lead-finder/enrich.py --name "Jane Doe" --company "Acme Co"
python pipelines/lead-finder/enrich.py --twitter-handle exampleuser
```

Output is JSON with whichever fields could be filled plus `providers_used`,
`providers_skipped`, `providers_failed` and `needs_enrichment` flags. Providers
run in waterfall order and any provider without a key is skipped, so the same
command works with zero keys (public-profile scrape only) or all of them.

| provider | env key | fills |
|---|---|---|
| Apollo | `APOLLO_API_KEY` | name, title, company, email |
| Hunter | `HUNTER_API_KEY` | email by name + verified domain |
| Apify (X / LinkedIn actors) | `APIFY_TOKEN` | full reply trees, follower lists |
| NeverBounce | `NEVERBOUNCE_API_KEY` | email validation |

Put keys in `.env` at the repo root. Never on the command line.

## Output contract (what the agent writes)

```
first_name, last_name, email, company, title, linkedin_url, twitter_url,
intent_signal, source, source_post_url, icp_segment, icp_tier, status, scraped_at, notes
```

`status` ∈ `KEEP_A | KEEP_B | KEEP_C | SKIP_COMPETITOR | SKIP_DUPLICATE | NEEDS_ENRICHMENT`.
Skips are kept in the file for the audit trail. `intent_signal` is mandatory:
a lead without one cannot be personalised and is not written.

## Rules the code enforces so the model does not have to

- Never invent a field. Blank + flag beats a plausible guess.
- Dedupe against `leads/seen_profile_urls.txt` on every run.
- CSV only. Pushing to a sequencer is a separate, confirmed action.
- The run report states which providers were available, so a thin result is
  legible as a tooling gap rather than a market signal.
