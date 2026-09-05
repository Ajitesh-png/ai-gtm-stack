# The Question Ladder — keyword → question series → blog set

**What this is:** the decomposition method for turning a keyword (or a whole cluster) into a *series of question-shaped blogs* that mirror how a real user comes to understand — and then adopt — a topic. Apply this in Phase 2.5 of the skill, after expansion and before scoring.

**Why it works on two levels:**
1. **For humans** — people don't consume one blog; they climb a learning curve (what → why → how → do → scale → decide). A connected series guides them down the funnel.
2. **For AEO/GEO** — people now *prompt* AI engines in full questions. Question-shaped titles + H2s are natively extractable, so each rung earns citations in AI Overviews / Perplexity / ChatGPT.

---

## Core principle

> A user never searches a single keyword in isolation. They move through a **sequence of questions** as their understanding deepens. Map a keyword onto that sequence, and each question becomes a blog (if it has its own demand) or an H2 (if it's sub-intent of a parent).

So the job isn't "pick keywords" — it's **"reconstruct the journey, then assign keywords to each step."**

---

## The 7 rungs

| # | Rung | User mindset | Question templates | Funnel | Blog format | Product bridge |
|---|---|---|---|---|---|---|
| 1 | **Define** | "I just heard this term" | What is {X}? · What does {X} mean? · {X} explained | TOFU→MOFU | definition | light (mention) |
| 2 | **Why / Problem** | "Why should I care?" | Why does {X} matter? · What problem does {X} solve? · Why now? | MOFU | thought-leadership | the problem we solve |
| 3 | **Mechanism** | "How does it actually work?" | How is {X} made? · How does {X} work? | MOFU | explainer | how Notch does it |
| 4 | **Workflow** | "Walk me through doing it" | What's the workflow for {X}? · How do you make {X} step by step? | MOFU | how-to | Notch *is* the workflow |
| 5 | **Compare** | "How is this different / better?" | {X} vs {Y}? · Is {X} better than {old way}? | MOFU→BOFU | comparison | why agentic wins |
| 6 | **Apply / Scale** | "How do I get {specific outcome}?" | How do I use {X} to {outcome}? · How can I {scale outcome}? | MOFU→BOFU | use-case / how-to | direct product demo |
| 7 | **Decide** | "What should I use / buy?" | Best {X} tools? · How to choose {X}? · {X} pricing / alternatives | BOFU | listicle / alternative | pick Notch |

> The user's example — *"how can I create 30 ads in one go"* — is **Rung 6 (Apply/Scale)**. *"what is it"* = Rung 1, *"how it's made"* = Rung 3, *"what is the workflow"* = Rung 4.

---

## The decomposition procedure (apply per cluster)

1. **Take the cluster head keyword** (e.g. "agentic video ads", "ai advertising").
2. **Generate rung questions** using the templates above — one or more per rung.
3. **Attach metrics** to each question's keyword form:
   ```bash
   python pipelines/seo-opportunity-engine/scripts/keyword_metrics.py metrics --keywords "what are X,how does X work,X workflow,..."
   ```
4. **Apply the blog-vs-H2 rule** (below) to decide what becomes its own page.
5. **Order the survivors as a journey** (rung order). This is the *narrative* order + the internal-link path. (Publishing order can differ — ship KD-0 rungs first for fast ranking; see ordering note.)
6. **Recurse one level:** a blog *is* one rung; its **H2s are the mini-ladder within that rung** (the next-level sub-questions). Write H2s as prompts.
7. **Internal-link the series in rung order** ("what is" → "how it's made" → "workflow" → "30 at once"), all linking *up* to the pillar. This builds the guided path Google and LLMs both reward.

### Blog-vs-H2 decision rule

| Condition | Becomes |
|---|---|
| Distinct search volume (≈ **≥ 50/mo**) **or** clearly distinct intent | **its own blog** |
| Logically part of a parent topic, little/no standalone volume | an **H2** inside the parent/pillar |
| Zero-volume **category** term (e.g. "agentic video ads") | **H2s in the pillar** + a citation play — the journey still matters for LLMs even with no Google volume |
| Already covered by a live page (cannibalization check) | an **H2/refresh** of that page, not a new blog |

### Ordering note
- **Narrative/link order** = rung order (1→7). This is how you interlink and how the reader journeys.
- **Publish order** = winnability-first. Ship the KD-0–14 rungs first so something ranks while higher-KD rungs mature. (e.g. publish the KD-0 "examples" rung before the KD-28 pillar.)

---

## Worked example A — "agentic video ads" (the user's example)

Cluster head: **agentic video ads** (0 vol — category we're creating → the *series* is for humans + LLM citation, not Google volume).

| Rung | Question (blog title) | Keyword + data | Status | Becomes |
|---|---|---|---|---|
| 1 Define | What are agentic video ads? | agentic video ads (0) | ✅ LIVE | blog (`what-are-agentic-video-ads`) |
| 2 Why | Why aren't AI ad generators enough? | — | ✅ LIVE | blog (`why-ai-ad-generators-arent-enough`) |
| 3 Mechanism | How are agentic video ads made? | ai powered video ads (320/KD10) | ❌ GAP | **blog** → "AI-Powered Video Ads: How They Actually Work" |
| 4 Workflow | What's the workflow to make one? | create video ads with ai (70/23) | ❌ GAP | **blog** → "How to Create Video Ads with AI, Step by Step" |
| 5 Compare | Agentic vs AI ad generators? | — | ✅ LIVE | blog (`agentic-ads-vs-ai-ad-generators`) |
| 6 Apply/Scale | **How do I create 30 video ads in one go?** | mass ad variations / batch creative | ❌ GAP | **blog** → product-led how-to ← *the user's example* |
| 7 Decide | Best AI ad tools (2026)? | best ai ad generator (260/37) | 🔁 refresh | refresh live top-5 listicle |

**The series reads as one journey:** *what it is → why the old way fails → how it's made → the workflow → 30 at once → what to use.* Internal links chain them in that order, all pointing up to `/agentic-video-ads`.

### Rung 6 blog, decomposed into prompt-based H2s
"How do I create 30 video ads in one go?"
- `Why do performance marketers need 30+ ad variations?`
- `What does it take to make 30 ad variations manually?`
- `How does an agentic workflow generate 30 ads at once?`
- `How do you keep 30 ads on-brand automatically?`
- `How do you test 30 creatives without overwhelming the algorithm?`
- `How do I generate my first batch of 30 ads?` (CTA → Notch)

---

## Worked example B — "ai advertising" (high-volume cluster)

Cluster head: **ai advertising** (6,600 vol / KD 28 → pillar page).

| Rung | Question | Keyword + data | Becomes |
|---|---|---|---|
| 1 Define | What is AI advertising? | ai advertising 6,600/28 · ai in advertising 6,600/12 | **pillar page** `/ai-advertising` (def block + H2s) |
| 2 Why | Why is AI changing advertising now? | — | H2 in pillar / the founder POV blog |
| 3 Mechanism | How does AI-generated advertising work? | ai generated advertising 1,000/27 | **blog** |
| 4 Workflow | How do you run an AI ad campaign? | ai advertising campaign 170/9 | **blog** |
| 5 Compare | Generative vs agentic advertising? | generative ai advertising 110/17 | **blog** |
| 6 Apply | Real examples of AI advertising | ai advertising examples 140/0 · coca-cola 4,400/29 | **blog** (listicle) |
| 7 Decide | Best AI advertising tools / generators | ai advertising generator 2,400/49 | **blog** (BOFU) / link to `/ad-generator` |

---

## Output: the Content Journey Map

When the skill runs a cluster through this ladder, it adds a **Journey Map** to the markdown report: the ordered series (rung → title → keyword/data → blog-or-H2 → live/gap), so the user sees not just *which* keywords but *the path* and *what to publish in what order*. The CSV still carries one row per resulting blog opportunity (with its primary keyword + scores).
