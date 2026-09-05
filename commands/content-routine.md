You are running the Notch Content Angle Research Routine. This is a structured workflow that produces ready-to-publish Twitter/X post angles for Notch Agentic Video Ads.

# Workflow Steps

## Step 1: Load Context

Read these files to load the full context before doing anything else:

1. **Product Knowledge:** `context/product.md`
2. **Schwartz Desire Map:** `context/desire-map.md`
3. **Post Structure:** `context/post-structure.md`
4. **Existing Content Research:** Scan `content-research/` to avoid duplicating angles already covered.

## Step 2: Run the Content Engagement Analyst

Use the Agent tool to invoke the `content-engagement-analyst` agent with this prompt:

> Search Twitter/X for high-performing posts in these spaces in the last 48-72 hours:
> - AI video ad tools (Creatify, HeyGen, Runway, Higgsfield, Arcads, Sora, Kling)
> - Performance marketing creative workflows
> - AI-generated UGC / AI ad production
> - Media buyers discussing creative velocity, ad fatigue, creative testing
> - Solo founders / operators building ad infrastructure with AI
> - "Stack" posts combining AI tools for ad production
>
> Focus specifically on Twitter/X. Find 5-10 posts that pass your engagement and freshness filters. Provide full deconstructions.

## Step 3: Synthesize Into Post Angles

Using the agent's research output, the Schwartz Desire Map, and the Post Structure, produce **3-5 post angle packages**. Each package must follow this exact format:

---

### Concept
A one-line concept name that captures the angle (e.g., "The Agency Tax Is Dead", "Your Brand Already Knows Itself").

### Performance Research
- **Source post(s):** Link to the high-performing post(s) that inspired this angle, with engagement metrics
- **Why it worked:** 1-2 sentences on the structural/psychological reason the source post performed
- **Format pattern:** Name the format (Equation Stack, "I just built", Double Negation, Listicle, etc.)

### Post Angle
- **Schwartz desire channeled:** Name the specific desire or fear from the Desire Map being activated (e.g., "The dream of leverage without headcount", "The fear of the dying window")
- **ICP target:** Which ICP segment this hits (DTC founders, AI SaaS UA, Affiliate/CPA, or Universal)
- **Hook type:** Specificity + open curiosity, bold claim, contrarian rehook, surprising stat, etc.
- **Emotional trigger:** The primary emotion (terror of being passed, thrill of being early, shame of dependency, etc.)

### Post
The full ready-to-publish Twitter/X post. **MUST follow the Notch Workflow Breakdown format exactly.** Read `context/post-format.md` before writing ANY post. The format is reproduced below for reference.

**THE POST FORMAT — follow this exactly:**

**HOOK — 3 lines. Each line does one job.**

Line 1: Dollar figure or concrete metric + wild promise. Specific enough to feel real, large enough to stop the scroll.
- "$39,128 from stolen ad structure. legally."
- "$110k+/month from a grandma that doesn't exist."
- "$23k/day from a 47-second video about a breakup."

Line 2: Visual/situational tease. What it looks like. What happened. Do NOT explain the mechanism.
- "one skincare brand's doctor recommendation ad. dissected. rebuilt. 30 times."
- "same face. same kitchen. same calm voice. every video."
- "ai agent. one product URL. no brief."

Line 3: Controversial take that reframes what the reader just absorbed. An opinion, not a fact.
- "original creative is a luxury tax. this is what's actually printing."
- "the best ai ads will never be identified as ai. and that's exactly the point."

**BODY — follows this sequence:**

1. **Setup** (1-2 lines): Bridge from hook to story. Often "here's how." or short context.

2. **The Steps / What Happened**: Numbered steps or short staccato lines. Each step = one action, one line. Call out what happened BETWEEN steps — "but what happened between step 2 and 3 is why this printed."

3. **The Agent's Work**: Use → arrows for each bullet. Each bullet = one specific action. Include the questions the agent asked (shows intelligence).
   - "→ what skin concern is your cold audience searching right now?"
   - "→ what proof does your warm audience need. clinical authority or social proof?"

4. **The Output**: Specific breakdown by segment/type. Use labels:
   - "10 cold. [description]."
   - "10 warm. [description]."
   - "10 hot. [description]."

5. **Results**: Dollar figures per segment. One per line. Summary: "3 segments. 30 ads. 30 data points for the algorithm instead of 3."

6. **The Pattern**: → arrow bullets showing the repeatable system. 4-5 steps max. Actionable and specific.

7. **Controversial Take**: "controversial take:" label. The insight most people won't act on. Reframes the entire post.

8. **CTA**: "comment [KEYWORD] for the workflow." or "rt + comment [KEYWORD] and i'll send the full setup." Next line: "(follow for dm)". Keyword = ONE word, all caps.

**TONE RULES — non-negotiable:**
- All lowercase throughout
- Staccato sentences. short. punchy.
- No em dashes (use periods or commas)
- No emojis. No exclamation marks.
- → arrows for workflow/system bullets
- Numbers are specific ($12,847 not ~$13k)
- Observational tone. reacting to what's happening, not selling.
- No filler words ("basically", "essentially", "actually")
- No first person unless telling a specific story

**ZEIGARNIK PRINCIPLE — applied WITHIN this format:**
The 3-line hook already opens the main loop. The body reveals in stages — each section should leave something unresolved that the next section partially answers while opening a new question. The CTA closes the loop conditionally. Do NOT resolve the main hook's curiosity before the CTA. The reader should reach the CTA knowing the SHAPE of the answer but needing the specific workflow/detail.

**SELF-CHECK GATE — after writing each post:**
- [ ] Does Line 1 have a specific dollar figure or hard metric? If NO → rewrite.
- [ ] Is the entire post lowercase with no em dashes or emojis? If NO → fix.
- [ ] Does the body use → arrows for agent work and pattern bullets? If NO → fix.
- [ ] Is there a labeled "controversial take:" section? If NO → add.
- [ ] Does the CTA use "comment [KEYWORD]" + "(follow for dm)"? If NO → fix.
- [ ] Can the reader get the full workflow without commenting? If YES → pull detail behind CTA.

---

## Step 3B: Generate 20 Angle Bank

After the 3-5 full post packages, generate a bank of **20 hook-ready angles** for Notch in context to AI ads. These are NOT full posts. They are one-line angle concepts with a hook sketch and format tag. Think of these as the raw material for future posts.

Use the agent's sweep findings, the Schwartz Desire Map, the competitive landscape, and trending conversations to generate angles that are fresh and timely.

Reference format (from `Twitter Stack Posts Sweep — May 2026.md`):

```
**Angle 1 — Equation Stack:**
> Notch + Claude Code = 40 video ads per week. No studio. No UGC creators. No editing queue. Just fresh creatives — every Monday morning.

**Angle 2 — "I built" Playbook:**
> I just built a workflow that generates 50 video ad concepts every Sunday night. Feed it your best hooks + product brief + target customer pain points. Notch renders 50 ready-to-test videos by Monday morning. While you sleep.
```

**Each angle must include:**
1. **Angle number + format tag** (Equation Stack, Founder Math, Trend Sniper, Myth Killer, Clone/Competitor, Split Test, Stack Reveal, Before/After, DM Screenshot, "$0 Playbook", etc.)
2. **The hook sketch** — 1-3 lines in the exact tone (lowercase, staccato, specific numbers). This is the Line 1 + Line 2 of a future post. Not a description of the angle. The actual hook words.
3. **Schwartz tag** — which desire/fear it channels, in parentheses

**Rules for the 20 angles:**
- At least 4 angles must reference specific data points or events from the agent's sweep (timely, not evergreen)
- At least 4 angles must be pure Notch product angles (what the system does, not market commentary)
- At least 4 angles must be competitive contrast angles (Notch vs the 3-tool stack, Notch vs agencies, Notch vs Meta's AI)
- Remaining angles can be market commentary, trend sniper, or format experiments
- No duplicating angles from existing Content Research files
- Each angle should be different enough that it could become a standalone post

---

## Step 4: Save to knowledge folder Vault

Save the complete output as a new file in:
`content-research/`

**Filename format:** `Content Angles — Twitter — YYYY-MM-DD.md`

**File structure:**
```
# Content Angles — Twitter — [Date]

**Date:** [today's date]
**Source:** Content engagement analyst sweep + Schwartz Desire Map synthesis
**Platform:** Twitter/X
**Product:** Notch Agentic Video Ads

---

[All 3-5 post angle packages here, separated by ---]

---

## 20 Angle Bank
[All 20 hook-ready angles here, numbered]

---

## Research Notes
[Brief summary of trends observed, format gaps identified, and any emerging patterns worth tracking]
```

## Rules
- Every post MUST channel a specific desire/fear from the Schwartz Desire Map — no generic "AI is cool" angles
- Every post MUST follow the Post Structure (Zeigarnik loops, not flat copy)
- Never repeat an angle that already exists in the Content Research folder
- Posts should sound like a founder/operator talking, not a brand account
- No hashtags. No emojis unless structurally necessary. No "thread incoming" bait.
- If the content-engagement-analyst finds fewer than 3 qualifying posts, note the gap and generate angles from the Desire Map directly using proven formats from past sweeps

$ARGUMENTS