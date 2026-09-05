---
name: launch-post
description: >
  Write a Notch launch/feature post for X (Twitter) from a video script,
  product concept, or founder draft — then produce the matching creator
  amplification brief, quote packs, and comment packs. Encodes the locked
  Notch post structure (3-line hook: specificity + open curiosity → widen →
  take), the hook-mechanics library, the iteration protocol (variants → ranked
  table → pick), the hard voice rules (no invented numbers, no em dashes,
  hire language for Max), and the creator-brief format (vault MD + Notch-yellow
  artifact page + guardrails). Use when the user says "create a post around
  this script", "write the launch post", "give me hook variations", "make a
  creator brief", "post for the video going out tonight", or pastes a draft
  post for tightening. NOT for SEO blogs (your blog pipeline), Max Format Radar
  episodes (format-radar), or founder tweet replies (/founder-voice-reply).
---

# Notch Launch Post + Creator Brief

You produce launch-day content for Notch products (Max, Notch MCP, and future
agents in the family): the main X post, the creator amplification brief, and
optionally quote/comment packs. The methodology below was locked across the
Max launch, the Notch MCP series (ChatGPT / any-LLM / Claude / Shopify-stack),
and the Level 4/5 autonomy arc — follow it, don't re-derive it.

## Read these vault files first (every time)

Root: `context/`

| File | What it gives you |
|---|---|
| `Post Format — Notch Workflow Breakdown (IMP).md` | The canonical 3-line hook rules + body sequence + tone rules |
| `Post structure (IMP).md` | The Zeigarnik loop law: S1 opens, S2 widens, S3 kills the easy explanation |
| `Hooks.md` | 15 hook types + the stacking rule (always stack 2-3) |
| `Hook Research Competitors.md` | creator patterns (just-did-X, BREAKING, equation, declarative, fear, insider) |
| `Hook Research - Workflow.md` | Number-forward workflow hooks + dense-hook mechanics table (impossible pair, mundane specificity, ending-first, emotional asymmetry) |

Product truth lives in `context/product.md`.
If a demo video is attached, extract frames (`ffmpeg -vf fps=1/2`) and read
them — the post may only claim what's on screen.

## The post skeleton (locked)

```
[optional headline equation — only if it earns its line]

S1  hook: specificity + open curiosity
S2  tease: widen the loop, don't resolve
S3  take: kill the easy explanation / reframe

[bridge line, ends with " -"]

→ bullet 1
→ bullet 2
→ bullet 3
→ bullet 4        (3-5 bullets, one action each, mechanism in demo order)

[closer take — the quotable line]

[CTA: Comment "KEYWORD" + what they get]
```

- 4 bullets is the default; each is verb-first, demo-ordered, no repeated "same X" phrasing.
- The closer often quotes the video's own end card verbatim so post and video lock together.
- CTA keywords are ONE word, caps, stable per launch ("MAX", "MCP"). Offer variants: comment + brand URL for onboarding mechanics.
- Casing: **sentence case** for brand-account launch posts (locked since the Max launch). **all lowercase** for founder-voice / insight-series posts (e.g. the skincare percentage post). Ask which surface if unclear — or infer: brand = sentence case.

## Hook engineering

S1 must contain a hard metric or specific object AND a gap the brain can't
close. The mechanics that repeatedly won this cycle, with shipped examples:

| Mechanic | Shipped example |
|---|---|
| Impossible pair | "$66K in new monthly revenue from decisions no human made." |
| Effect-before-cause | "The first sign our winning ad was dying was the three replacements already waiting for approval." |
| Ending-first | "Three replacement ads were waiting for approval this morning. Nobody asked for them." |
| Ritual contrast | "Every media buyer wakes up to the same question: what broke overnight? One brand woke up to it already fixed." |
| Two-lives contrast | "Level 1: it's 11pm and you're still uploading the clip it made you. Level 5: a 7am Slack message." |
| Audit count | "9 ads are selling vases on Meta right now. Total human input: six words." |
| Machine's own words | "'Still working, but the trend is turning.' No analyst wrote that." |
| Equation  | "1 chat thread + 1 connector = research to live ads on Meta." |
| Assumption-kill | "Claude could always tell you why your ads win. It could never do anything about it." |
| Announcement-flat | "Notch MCP just launched for Claude." (Higgsfield style — the flatness is the flex) |

Rules learned the hard way:

- **Passive voice hides the actor** when the reveal should wait ("the turn got caught, the variants got built") — but if the user says it's confusing, clarity beats mystery: name Max in S2.
- **Count what's countable.** "I like these 3" + "Launch them" = six words → that count became the hook. Look for the audit number hiding in the story.
- **S2 must widen, not resolve.** Revealing the mechanism in S2 kills the scroll. Add scale, stakes, or a mundane-specificity anchor ("before the coffee cooled", "positioning debates at 1am").
- **S3 is a take, not a description.** Best takes re-diagnose something the reader already believes ("most 'creative fatigue' is operator fatigue", "intelligence was never the gap. shipping was.").
- One metaphor per post. If the hook is a race, the body can't be a vending machine.

## Iteration protocol

The user iterates hooks 3-10 rounds. Work with it, don't fight it:

1. First delivery: full post + 2-3 alt hooks.
2. "Give me variations" → 6-8 variants, each tagged with its mechanic, ranked
   in a table (strongest line + why + best audience), one clear pick with
   reasoning, runner-up named.
3. Line-level feedback in parentheses → apply exactly, explain each change in
   a short table (was → now → why). Never restate their instruction back as prose.
4. "Shorter / crisp / too long" → cut structurally (merge bullets, kill the
   second list, drop repeated ideas), not by squeezing words. Report the cuts.
5. "Doesn't land / try again" → diagnose WHY before redrafting (usually:
   too many frames stacked, hook resolves too early, or take reads as marketing
   instead of observation). Name the diagnosis in one line, then rebuild.
6. Lock = user pastes the post back or says lock. After lock, only touch what
   they flag.

## Hard rules (violations the user has corrected — never repeat)

- **Never invent numbers.** No made-up ROAS, brand counts, salaries, "10x",
  "$30" vs "$199". Only numbers from the script/demo/user. If a number would
  help, ask for the real one or leave a [slot].
- **Demo-as-demo.** The post may claim what the video shows. Creators must
  frame it as "in the demo it..." — never extend into guarantees.
- **No em dashes.** Periods or commas. (A trailing hyphen on the bridge line
  is house style, keep it.)
- **Max is a hire, "he".** Never "tool", "agent-speak" verbs ("deploys
  workflows"), or "it" once the hire frame is set. Notch MCP is "it" (a connector).
- **Lead with mechanism, not category label.** "AI growth marketer" arrives as
  the explanation, never the opener (house rule).
- **Saturated words banned in hooks:** introducing (unless deliberate),
  unlimited, revolutionary, game-changing, 10x, "the future of".
- **No narrowing** ("ecom", "DTC") unless the user names the ICP for that post.
- **Partnership claims:** never "now on ChatGPT / GPT store / official
  OpenAI-Anthropic-Shopify partnership". It's "connects to" / a custom connector.
- **Autonomy claims:** match the current ladder position. "You make the calls" /
  "the approval button stays yours" unless the user explicitly moves Max up a level.
- Repetition audit before delivering: if a word ("already", "same") appears
  3+ times in the hook block, rewrite until each line advances.

## Creator amplification brief (the companion deliverable)

When the user says "creator brief" / "brief for influencers", produce all three:

1. **Vault MD**: `02 — Content Library/Twitter & LinkedIn Posts/Drafts/<Launch> — Creator Brief (<date>).md`
2. **Artifact page** (Notch-yellow design system: #F5C518 accent, light+dark
   themes, tweet card for the main post, yellow block for the ONE idea, lane
   cards with copy-to-clipboard buttons, → bullets for facts, red ✕ for
   guardrails, numbered mechanics). One artifact per launch; republish same
   file path for revisions.
3. **SendUserFile** the MD.

Brief sections (fixed order):

1. **What's Launching** — product truth in plain words + "the main idea to communicate" + audience line.
2. **The Main Post** — verbatim, in a tweet card, + note that the demo video carries product detail ("your quote frames the idea").
3. **The ONE Idea We're Amplifying** — one sentence, plus the payoff line creators may borrow.
4. **Quote Angles — Pick One Lane** — exactly 6 lanes, each: name, "For: audience", 2-4 line sample in lowercase influencer voice. Lanes must not overlap; instruct "pick ONE and rewrite in YOUR voice".
5. **Voice & Format Guide** — works/skip two-column. Always includes: short lines, name the pain first, personal observation beats hot take, react like it's news, keep it idea-level.
6. **Facts You Can Use (all verified)** — only script/demo-backed claims.
7. **Do NOT Say** — every launch gets: no invented numbers; no partnership/store-listing claims; no overclaiming beyond the demo; no competitor naming as the loser; plus launch-specific bans.
8. **Mechanics** — quote-tweet main post, same-day window, shared CTA keyword, first-hour replies, disclosure. Placeholders: post link + launch window.

Reference influencer voice (from the creator reply screenshots): pain
or discovery first → what the product did, specifically → reaction closer
("genuinely insane", "finally", "what."). 3-5 short lines. Never a feature list.

## Quote packs & comment packs (on request)

- **Quote pack**: 8-12 quotes across archetypes (founder, media buyer,
  contrarian, beta insider, agency-adjacent, one-liner accounts) with a
  distribution table (quote → who posts it) and a top-3.
- **Comment pack**: mix pain-recognition, warming skeptics, operator questions
  (these give the founder layup replies), feature-specific reactions, and
  CTA-followers. Never 100% praise — that reads botted. Spread over 2-3 hours.
- Observations outperform hot takes. "i noticed X" > "X is dead."

## Ship checklist

- [ ] Every number traces to script/demo/user
- [ ] Hook: S1 metric+gap, S2 widens, S3 takes — no early reveal
- [ ] No em dashes, no banned words, casing matches surface
- [ ] Closer echoes the video end card (when there is one)
- [ ] CTA keyword consistent with the series
- [ ] Brief: 6 non-overlapping lanes, guardrails cover this launch's specific risks
- [ ] Flag any post-vs-graphic contradiction (e.g. ladder level badges) before it ships
