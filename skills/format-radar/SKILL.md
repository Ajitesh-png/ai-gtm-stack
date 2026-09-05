---
name: format-radar
description: >
  Run one episode of the recurring "Max Format Radar" Twitter/X series end to
  end: research a trending ad format, deconstruct why it converts, decide which
  category it's already burned in, mutate it into a Max-ownable version,
  generate the scenes on Higgsfield, build the 1080x1920 multi-scene post
  video, and write the 5-post thread. Use when the user drops a new ad format
  ("do a format radar on X", "new format: street polls", "make a post about
  this ad format"), names a category to go find one in, or asks for the next
  episode of the series. NOT for general blog work (see your blog pipeline) or
  one-off Higgsfield generations (see higgsfield-generate).
---

# Max Format Radar — episode runner

You produce one episode of **Max Format Radar**. Every episode is **the
provenance of one ad**, told in four beats:

1. Max **read competitors' live ads** and found a format before it saturates.
2. Max **read the account's own ad history** and picked the pain that already
   converts there.
3. Max **wrote the script around that pain** — not around the product.
4. Max **built it and queued it to launch.** The founder approved the spend.

That chain maps 1:1 onto the product loop (analyze → decide → create → launch),
and it is the narrative of *everything* in the episode: the four input chips,
the numbered trace card, and the thread's three value posts.

Pipeline: **Find → Deconstruct → Isolate → Call → Generate → Verify → Build →
Thread → Package.**

**The chain that must not break:** every mechanism named in the deconstruction
has to survive isolation, get a row in the transfer table, own a beat in the
rebuilt ad, and be *pointable at* in the finished frames. A mechanism that
can't be pointed at was never real, and the post's central claim — that the
analysis produced the ad — is only true if that chain holds end to end.

Project root: `pipelines/format-radar/`
Series spec + Ep.01: vault `Growth Marketer/Content/Max Format Radar — Series Spec + Ep.01 (Street Poll).md`
Template B + Ep.02: vault `Growth Marketer/Content/Max Format Radar — Template B (Yapping 3-Up) + Ep.02.md`

## Pick the template first

| | **A — provenance** | **B — hook test** |
|---|---|---|
| Files | `post-template.html` · `episode.json` · `build.py` | `post-template-yapping.html` · `episode-yapping.json` · `build_grid.py` |
| Canvas | 1080×1920 vertical | 1824×1080 landscape (3 × true 9:16 panels) |
| Shape | equation rail + 3-step reasoning trace, one ad cut across 3–5 scenes | 3-up grid playing simultaneously + why/call band |
| Says | *here is how this one ad came to exist* | *this format is cheap enough to test, so here are three hooks* |
| Use when | the format's story is the **selection** — where it came from, which pain it's pointed at | the format is **cheap to produce**, so shipping one asset would be the mistake |

Default to **A**. Reach for **B** when the episode's honest conclusion is "don't make one of these, make three and let the data pick" — that's a different argument and it needs the grid to make it.

## The one rule that defines the series

The post visual is an equation borrowed from Arcads, with **two research
inputs** because the story has two discovery beats:

```
the format it found      (from competitors' live ads)
+ the pain it pulled     (from the account's own ad history)
+ your product
+ your growth marketer
→ a live ad, and the trace of how it got there
```

Theirs resolves to *"100% automated"* — an asset. **Ours resolves to a
reasoning trace**, carried in the numbered `HOW IT GOT HERE` card under the
output frame.

**Never collapse the two research chips into one.** That the *format* came from
outside the account and the *pain* came from inside it is the entire argument
for why this is a hire and not a generator: a generation tool can borrow a
format, but only something reading your account can say which pain to point it
at. If you can't write a step 2 that names something **only account access
could reveal**, the episode isn't worth shipping — go find a different one.

## Always-loaded context
- `context/product.md` and the Growth Marketer vault folder, especially:
  - `Product Knowledge/Notch Growth Marketer — Product Knowledge.md` (the loop: analyze → decide → create → launch → optimize → learn)
  - `Brand Positioning/Max — Revenue Engine Positioning (Single Hire).md` — locked: **"Max. Your superhuman growth marketer." / "You sleep. Max ships."**
  - `Content/Format Radar — 2026-08-07 (Competitor Scan).md` — what's saturated, what's open
  - `Content/AI Growth Marketer — Watch Max Work (Organic Thread Series).md` — the 30 loop use-cases
- ICP: scaling DTC operator who *is* the media buyer. **Rotate category each episode: apparel → home goods → skincare.** No supplements/health.

---

## Step 1 — Find the format

If the user drops a format, take it. Otherwise go find one: WebSearch → WebFetch
on ad-teardown sites and agency blogs, `mcp__Claude_Browser__*` on Meta Ad
Library, or run the `format-scout` agent.

You need three things before you continue:
1. A **named** format with observable mechanics (not "UGC" — too broad).
2. A category where it is **already spent**.
3. A category where it is **unspent** — this is where you rebuild it.

If you can't find #2 and #3, you don't have an episode. Keep looking.

> ⚠️ **Target ads whose mechanism lives in the COPY.** You can read ad copy and
> metadata. You cannot watch video. Pick a video ad and you will end up
> inventing what's on screen — Ep.05's first selection died exactly this way,
> with two of three "mechanisms" fabricated about 48 seconds of unwatched
> footage. Text-led ads, statics, review ads and long-copy are readable, so the
> deconstruction is observation rather than guesswork.
>
> ⚠️ **Run-time alone is not evidence.** *Active* ≠ performing — the Library
> shows a start date and a status, never spend. Before calling anything
> long-running, ask: long compared to *that advertiser's* median? compared to
> the *category's*? And beware confounds — a well-funded brand's ad may survive
> on budget or evergreen placement, not on its creative.
>
> ⚠️ **Never report a pattern you found under an unknown sort order.** The Ad
> Library's "Sort by" control defaults to something you didn't set. "Everything
> I found is recent" may be an artefact of your method rather than a fact about
> the market. Set the sort or don't make the claim.
>
> ⭐ **A controlled comparison beats a long run-time.** The strongest sourcing
> outcome is two advertisers using the *same fact* to different effect — same
> spec, same category, one making it an argument and one making it a bullet.
> That isolates the mechanism with no performance data and nothing to fake.
> Ep.05 is built on exactly this after its run-time thesis collapsed.
>
> ⚠️ **Text search surfaces the fabricated health-advertorial operation** on
> unrelated keywords (`bed sheets`, `backpack` both hit it). Invented personal
> stories naming real medications, aimed at elderly people with chronic
> conditions. Never teach these; see the Ad Teardown Ep.01 notes.

> **Numbers guardrail.** Format-vendor case studies (agencies who *sell* the
> format) publish spectacular CPA/ROAS deltas. Never put them in the thread —
> they're self-reported marketing. Also watch for outright SEO fabrication in
> this space (e.g. the claim that Meta scores creative via "on-device biometric
> inference" — not real, never repeat it). **The thread runs on mechanism.**
> Mechanism is defensible; borrowed metrics are not.

## Step 2 — Deconstruct (WHY it converts)

Write the teardown in Max's first-person operator voice. Cover: the hook, the
scroll-stop mechanic, the vessel/format, offer treatment, proof, pacing, the
exact ICP emotion, and — crucially — **what's borrowable vs what's saturated**.

### Mechanisms, not descriptions

A **description** says what is on screen. A **mechanism** explains why the
viewer behaves differently because of it. Only mechanisms transfer.

| Description ❌ | Mechanism ✅ |
|---|---|
| "it opens with a question" | "the question names an objection the viewer already holds, so *they* supply the tension and the ad never has to assert anything" |
| "it's shot on a phone" | "the framing is bad in the specific way a real person's is, so it's processed as a message before it's classified as an ad" |
| "the creator talks fast" | "it starts mid-sentence, so you arrive as an eavesdropper rather than an audience" |

**The test:** if the sentence doesn't contain a *because* that predicts viewer
behaviour, it's a description. Rewrite it or drop it.

Go deep into the niche, not just the ad. The same mechanic means different
things in skincare and in home goods, because the viewer arrives with different
defences.

## Step 2.5 — Isolate (mechanism vs packaging)

**The step that decides whether the rebuild is any good.** Skip it and you copy
the surface, which is what every swipe-file account already does.

For each element, run the **swap test**: replace it with a reasonable
alternative. Does the ad still work?

- **Still works → packaging.** Creator, room, lighting, wardrobe, music,
  offer wording, product colour. Do not transfer these. Copying packaging is
  how you get a clone that dies.
- **Breaks → mechanism.** Usually: the opening move, what is withheld, who is
  speaking and to whom, what is deliberately *not* shown, the order of reveals.

**Cap it at three.** Most ads have one or two real mechanisms. If your list has
six, you haven't isolated — you've inventoried. Rank them and cut to the ones
that break the ad when removed.

Write the surviving mechanisms as a numbered list. **Everything downstream —
the transfer table, the shot spec, the thread's value posts — is built from
this list and nothing else.**

## Step 3 — The visual anatomy

Turn it into a beat-by-beat recipe anyone could rebuild: timecode, what's on
screen, what's said. Plus the **non-negotiables** (aspect, grade, subtitles,
when the logo may appear). This is the save-bait post.

## Step 4 — The call (beat two + the mutation)

Three decisions, all stated explicitly:
- **Category:** where the format is burned vs where it's open, and why you picked yours.
- **The pain, from the ad history.** This is beat two and the heart of the
  narrative: which angle *already converts in this account*, ranked against the
  others — the last ~90 days of ads, every angle ever tested. Ep.01's read was
  *fit beat price on every angle*, against an operator defaulting to discount
  creative because discounting feels urgent. It must come from performance data,
  never a brainstorm. **If there's no clear read, pick a different episode.**
- **The mutation:** how Max points the format's mechanic at that pain. Ep.01:
  everyone asks a *curiosity* question; Max asks the **objection the account's
  own data says is blocking the sale**.

Then write the **3-step trace** — read the field → picked the pain from the
account → wrote the script around it. Write it *before* you generate anything;
it's the gate on the whole episode.

Rebuild target = a **fictional stand-in brand** (Ep.01 used NORTHFALL for
heavyweight tees). Never present it as a real customer.

**Rebuild in a different category from the one you found it in.** Same category
is a copy; a different category is proof you isolated the mechanism rather than
the packaging.

### The transfer table — write this before generating anything

One row per surviving mechanism. All three columns must be fillable.

| # | Mechanism (from 2.5) | How it manifests for this brand | The frame you point at |
|---|---|---|---|
| 1 | viewer supplies the tension, ad asserts nothing | opens on the objection the account's data says blocks the sale | 0–2s, before any product is visible |
| 2 | arrives as eavesdropper, not audience | already mid-sentence on frame one, eyeline off-lens | first frame |
| 3 | proof is behavioural, not stated | shows the thing they stopped doing, not a claim about results | 8–12s |

**If a mechanism has no third column, it is not real.** Either it was a
description wearing a mechanism's clothes, or the rebuild doesn't actually carry
it. Fix one or drop the row — never generate against an unfillable table.

This table is the contract. Step 5 generates it, Step 5.5 verifies it, and the
thread's value posts are its rows in prose.

## Step 5 — Generate on Higgsfield

Use `mcp__higgsfield__*` when connected; the `higgsfield` CLI is the fallback
(`higgsfield generate cost|create|wait`). If the CLI reports `Not authenticated`,
say so and stop — `higgsfield auth login` is interactive and can't be run here.

**Locked recipe** (validated Ep.01):

| | Model | Params | Credits |
|---|---|---|---|
| Scene clips (template A) | `kling3_0` | `9:16`, `duration 5`, `mode pro`, `sound on` | **12.5 ea** |
| Opening/hero clip | `kling3_0` | same but `duration 10` | **25** |
| Product still | `nano_banana_pro` | `1:1` | ~2 |

**Size the model to the rendered panel, not to the source.** Template A's frame
is 614px wide, template B's panels are 608px. 1080p is wasted at both. For
template B specifically, four levers cut cost with no visible loss:
`720p not 1080p` · `std not pro` · **`sound: off` on every panel whose audio the
template discards** (only `audio_from` needs it) · `5s not 10s`. Always
`generate cost` the candidates first and take the cheapest that holds lip-sync —
lip-sync is the one artefact viewers consciously notice on a talking head.

- Use `generate_video_batch` for the scene clips — they're independent, so they
  render in parallel. Then `jobs_wait`.
- `get_cost: true` preflights. Check `balance` first and **report the spend**.
- Veo 3.1 has better dialogue but caps at 8s. Seedance 1080p costs 90 cr and is
  wasted — the frame renders at 614px wide. Default to `kling3_0` pro.
- **Every prompt must end with:** `no on-screen text, no captions, no logos, no
  watermark` — otherwise Kling burns its own captions in and fights the overlay.
- Keep the scene prompts in the same shoot language (same street, light, mic,
  lens) and vary only the person + line, so the cuts read as one shoot.
- 3–5 scenes. Write an escalating objection stack, not four paraphrases of one line.

### The rebuild ad is 10–15s. One mechanism per beat.

The episode's rebuilt ad is **not** the multi-scene post video — it's a single
short ad, the length a real one would be.

| Beats | Runtime | Use when |
|---|---|---|
| 2 × 5s | **10s** | two mechanisms. Don't pad to 15. |
| 3 × 5s | **15s** | three mechanisms |

**One mechanism per beat, and it must be visible in that beat.** Two mechanisms
in one 5s beat means neither is legible — the viewer gets an impression instead
of an argument. Beat 1 always carries the opening move, because that's the
scroll-stop and it's the mechanism the thread leads on.

Longer is not better here. A 30s rebuild dilutes every mechanism and stops being
evidence of anything.

### Prompt the mechanism, not the aesthetic

**This is the fix for "the generated ads look generic."** A prompt describing a
vibe returns a vibe. A prompt describing the mechanism-carrying element returns
something you can point at.

❌ *"a woman talking to camera, authentic UGC style, natural lighting, holding
the product"* — every one of those words is packaging. The model returns a
stock-feeling clip because you asked for a genre.

✅ *"a woman already mid-sentence as the clip starts, eyes slightly off-lens as
if answering someone standing beside the camera, product held down at her side
and never lifted toward the lens"* — three mechanisms, each stated as a physical
fact the model can render: in-progress speech, off-lens eyeline, unlifted
product.

Write each prompt straight off its transfer-table row. If you cannot describe
the mechanism as a **physical, visible fact**, you have a description, not a
mechanism — go back to 2.5.

## Step 5.5 — Verify against the table (hard gate)

Pull one frame per beat and read it. For every row of the transfer table, name
the timestamp where that mechanism is visible.

- **Visible** → pass.
- **Not visible** → regenerate that beat with a more physical prompt. Do not
  ship and do not talk around it in the thread copy.

**A rebuild where the insight isn't visible is not a rebuild, it's a video.**
The whole post rests on the claim that the analysis produced the ad; if a reader
can't see mechanism 2 in the ad, the claim is false and the format's credibility
goes with it.

Log the pass/fail per row in the episode's vault entry.

## Step 6 — Build the post

**Never hand-edit `post-template.html` copy.** Everything episode-specific lives
in `episode.json`; the template reads it from an inline JSON block and
`build.py` rewrites that block per scene.

1. Download clips to `assets/`.
2. **Measure real speech boundaries — do not guess in/out points.** Ambient
   street noise defeats `silencedetect`, so use the RMS envelope:
   ```bash
   ffmpeg -v error -i clip.mp4 -af "asetnsamples=n=12000,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=-" -f null - 2>/dev/null \
     | grep RMS | awk -F'=' '{printf "%5.2fs %7.1f %s\n", (NR-1)*0.25, $2, ($2>-30?"SPEECH":"")}'
   ```
   Each row is 0.25s. Anything above about −30 dB is speech.
3. Fill `episode.json`: the four `chips` (format · pain · product · notch, each
   with its provenance caption), the question, the 3-step `trace`, and one
   scene per cut with `in`/`out`/`subtitle`. Chips and trace render from config
   — the template holds no hard-coded copy.
   - Cut **mid-conversation**: enter a beat before the line, leave on the last
     syllable, no trailing air.
   - If a clip has a gap over ~1s between sentences, **split it into two scenes**
     — a jump cut on the same speaker is native to street-interview editing and
     kills the dead air.
   - One subtitle per scene, and it must match what is actually audible.
4. `python build.py` → writes `format-radar-<slug>.mp4` and
   `post-still-<slug>.png`. `--still` renders only the PNG.

**Template B instead:** fill `episode-yapping.json` (three panels, each with
`clip` + `hook` name, plus `audio_from`) and run `python build_grid.py`. No
RMS/cut work — all three panels play at once for the shortest clip's duration.

**Default chrome is deliberately minimal: the notch mark and the three format
labels, nothing else.** The claim pill and the why/call band are opt-in
(`"claim": [...]`, `"band": {...}`). Turn the band ON for standalone reposts
where the video travels without its thread — otherwise the judgment layer
disappears and it's just three clips with a logo. Leave it OFF when the thread
carries the reasoning, which looks better and frees the full panel height.

Audio comes from exactly one panel (three voices at once is noise); generate the
other two with `sound off` and save 2.5 credits each.

**Static variant.** Panels accept images as well as clips — all three stills and
`build_grid.py` renders the PNG in one Chrome pass, no ffmpeg
(`episode-yapping-static.json`, ~**3 credits** vs ~25). Use it for LinkedIn,
quote-tweets, and as the media on the middle thread posts where re-running the
video is repetitive. Mixed image/video panels are rejected.
**Model: `flux_2` at 1 credit** — A/B'd against `z_image` at 0.15, which returns
beauty-lit smoothed skin, the one thing this format cannot be. And make the three
stills three *different* raw looks (flash-at-night / blown-out daylight /
high-ISO dark); sameness reads as a template, difference reads as three real
creators.

**Measured prices (5s, 9:16):** `kling3_0` std+sound-off **7.5** · std+sound-on
**10** · pro+sound-on **12.5** · `wan2_7` 720p 7.5 · `seedance_2_0_mini` 720p
12.5 (audio makes no difference) / 480p 5. A three-panel grid is **25 credits**
done right. Don't take the 480p option — upscaling a face into a 608px panel is
the first lever that actually costs quality.

⚠️ **`sound: false` is invalid and fails silently.** The API wants the string
`"off"`; a boolean is ignored and the model **defaults to sound ON** — a 5s std
clip you budgeted at 7.5 costs 10. The response reports it under `adjustments`,
which is easy to skim past. Same for any enum param: pass the string.

⚠️ **Preset hijack.** A batch item can be *refused outright* in favour of a
preset recommendation instead of being submitted, returning
`submission_failed` with a `preset_recommendation`. Retry that item with
`declined_preset_id: "<id>"`. **Always check `submitted_count` vs the number of
requests** — a batch can come back `submitted_count: 1, failed_count: 2` and
still look like a success at a glance.

⚠️ **Video models are unreliable with text.** If a beat depends on lettering
being *read* (a label, a stamp, a screen), `kling3_0` will often misspell it —
Ep.05 rendered `GENUINE LEATTER`. Generate that beat as a **`flux_2` still (1
credit, reliable text)** and push it with ffmpeg `zoompan` instead. A held macro
is usually the better shot anyway for a beat that asks the viewer to stop and
read.

⚠️ **CLI flags use underscores** (`--aspect_ratio`, not `--aspect-ratio`); the
dashed form fails with a misleading `Unknown params` error. `higgsfield model
get <model>` lists the real names. `kling3_0` has no `resolution` — quality is
`mode` (std/pro/4k). `higgsfield generate wait` takes **one** job id at a time.

**Two gotchas already fixed in `build.py` — don't reintroduce them:**
- The clip chain needs `setpts=PTS-STARTPTS`. `-ss` input seeking leaves the
  source PTS offset intact, so without it the overlay lands outside the
  segment's time window and the frame renders empty.
- The `data-mode` injection is anchored with `^<body>` (multiline). A loose
  `<body>` replace also matches the string inside the stylesheet comments.

**Always QA rendered frames** — pull one frame per scene with ffmpeg and read
them. Check: product image loaded (not alt text), subtitle matches the scene,
the video is actually visible in the frame, reason strip doesn't overflow.

## Step 7 — The thread

**Use the house post structure**, defined in
`03 — Frameworks & Playbooks/Content Pillars & Angles/Competitor Format Posts — Discovery + Dissection + Playbook.md`
(read it — it also contains ~11 worked examples in the exact voice):

> S1 hook (specificity + open curiosity) → S2 tease (situational detail, don't
> resolve) → S3 controversial rehook (kill an assumption) → body breadcrumb
> trail (partial reveals, each opening a sub-loop) → `controversial take:` →
> CTA closes the loop conditionally (comment = price of closure).

House conventions: **lowercase**, one idea per line, `→` bullets, `---` between
posts, "here's the mechanism / here's the psychology" section openers, and the
close `rt + comment "WORD" and i'll send the full X. (follow for dm)`.

**Shape: format first, reveal last.** The thread must stand entirely on its own
as a format teardown — someone who never learns what Notch is should still leave
with the read and the recipe. The agent doesn't appear until the second-to-last
beat, where it **recontextualises everything already read**: *none of that is my
read.* That satisfies the vault's 3:1 rule and the no-product-in-the-hook
guardrail without effort, and the reveal hits harder for having been earned.

**Five posts. Always end on the reveal.** The locked beat order:

1. **hook — name the format, then name three reasons and resolve none of them.**
   Each reason is one line, phrased as a paradox (*"the worse it looks, the
   better it sells"*) — three open loops in four lines. Close with the S3
   rehook that indicts the reader: *"every brand copying it is copying the look
   and missing all three."*
2–4. **one post per reason**, in the order promised. Each closes exactly one loop.
5. **the reveal + the build + CTA, in one post.** *"none of that is my read."*
   What it read, what it decided, what it built, then the human's sole role:
   *"i found out when i approved the spend."* Fold the controversial-take line in
   here (*"it didn't make me an ad. it ran me an experiment."*) rather than
   giving it a post.

Resist adding a sixth. Anything that feels like it deserves its own post —
the grading criteria, the shot list, the prompts — is **stronger as the
comment-to-unlock payload than as thread copy**. Pulling the most save-worthy
material *out* shortens the thread and gives the CTA something real to trade.

**Media placement performs the reveal.** Post 1 carries an artefact of the ad
you **found**, so the format reads as something spotted in the wild. The branded
asset goes on the reveal post — first sight of it lands exactly when the thread
admits who made it. Never put the branded asset on post 1; it spoils the ending
before the reader has earned it.

⚠️ **A raw clip of your own rebuild only works on post 1 when the rebuild is in
the SAME category as the source.** Ep.01 could use raw street-poll footage
because the rebuild was also a street poll. Ep.05 rebuilt merino into leather,
and the first pass put a raw wallet clip under copy entirely about a shirt —
the reader stumbles at the first image. **When the categories differ, build a
card of the found ad instead** (`found-ad-merino.html` is the pattern):
render it as a feed post, anonymise the advertiser to a fictional name, and
**write the copy original** — same mechanism, same register, never the real
brand's words. Leave the `… See more` truncation in; it's what makes it read as
a real long-copy ad rather than a designed card.

**Never put the comparison on post 1** if the episode has one — it's post 4's
payload, and post 4 is the strongest post in the thread.

⚠️ **The house format leans on revenue figures ($340K/month, $22K/day). Don't.**
Every number in our threads must be one we can stand behind — counts, seconds,
credits, hooks. No invented performance metrics; a real figure needs a real
account plus permission and the 2.5–4× range.

Each value post must also stand alone as a lesson, useful to someone who ignores
the product entirely.

- **1/ Hook** — the overnight trace, in the founder's first person. Ep.01:
  *"My growth marketer read 40 competitors' live ads last night, found a format
  none of them are running in my category, and had the ad built before I woke
  up. Here's the whole trace 👇"* **No "Notch" or "Max" in the hook line** — the
  label arrives in post 5. Attach the post video here.
- **2/ Beat one — it read the field.** How it searched, the format it found, why
  the format converts (mechanism, no numbers), and the saturation call.
  *Lesson: sort by run-length; longevity is the only free performance signal.*
- **3/ Beat two — it picked the pain from the account.** The ad-history read and
  what it overturned. *Lesson: you don't pick the angle, your ad history already
  picked it — most people never look.* **This is the strongest post in the
  thread; never cut or shorten it.**
- **4/ Beat three — it wrote the script around the pain.** The question, the
  escalating answer stack, when the product is allowed to appear, the
  non-negotiables. Save-bait. Attach the still.
- **5/ CTA** — *"I did none of that."* Then the loop in one paragraph ending on
  "I approved the spend. That's the entire job now.", then: *Max. Your
  superhuman growth marketer. You sleep. Max ships. → usenotch.ai*

**Voice check:** the value posts are written in Ajitesh's first person about
"my account". Keep the specifics illustrative of a real session *shape*. The
moment any of it is framed as a customer result it needs real numbers, written
permission and the 2.5–4× range.

## Step 8 — Package

Append the episode to the vault series doc (or a new `Ep.NN` section):
teardown, anatomy, the call, the script, the Higgsfield production log (models,
params, credits, job IDs), the thread copy, and anything that broke.

## Guardrails
- **Template A:** the trace card is mandatory, and step 2 must point at the
  account's own data. **Template B:** the band is mandatory, and its right-hand
  column must state a *call*, not a feature. Without them these are competitors'
  layouts with our logo on top.
- No borrowed vendor metrics in the thread. Mechanism only.
- Rebuild brands are fictional stand-ins; swiped ads are anonymised by category.
- Never reproduce competitor ad copy verbatim or impersonate a brand.
- No "Notch"/"Max" in the hook line.
- Subtitles must match audible speech — flag for a listen-check before posting,
  since you can't hear the generated audio.
- Any ROAS/CPA/customer figure needs permission + the 2.5–4× range.
- Confirm Higgsfield credit cost before video runs; report the spend after.
