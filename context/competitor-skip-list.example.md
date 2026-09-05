# Competitor skip list (example)

Copy to `context/competitor-skip-list.md` and fill in your market. The
`lead-finder` agent and the `/find-leads` command read this before writing any
CSV. Outreach to a competitor's staff is the single largest source of wasted
sends, and it is also embarrassing.

## Tiers

- **Tier 1, direct competitors.** Same buyer, same job-to-be-done. Their
  employees and founders are never prospects.
- **Tier 2, partial-overlap tools.** Solve one step of the workflow your
  product covers. Usually skip; occasionally partners.
- **Tier 3, adjacent tools.** Same audience, different job. Skip staff, keep
  their customers.
- **Tier 4, watch-list.** Could move into your category. Track, don't skip.

## Companies

| Company | Tier | Domain | Notes |
|---|---|---|---|
| Example Corp | 1 | example.com | direct competitor since 2025 |
| Adjacent Tool | 3 | adjacent.io | same audience, different job |

## People flagged in past runs

| Name | Company | Role | Reason | Date |
|---|---|---|---|---|
| J. Example | Example Corp | Co-founder | Tier 1 | 2026-01-15 |

## Decision rule

**SKIP if any of:**
1. Works at or founded a Tier 1 or Tier 2 company (verified via headline or bio).
2. Bio or posts say "I built" / "I'm building" a product in your category.
3. Their company website sells your category as a SKU.

**KEEP if any of:**
1. Practitioner at a company that buys tools like yours.
2. Founder or exec of a customer-shaped company.
3. Agency owner: they buy tools, they don't build them.

When in doubt, mark **Tier B with a note**, never SKIP. Manual judgment
downstream is cheap; a discarded real lead is expensive.
