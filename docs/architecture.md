# Architecture

The stack is a set of Claude Code skills, slash commands and subagents that
share one **context layer** and call a small number of **deterministic
pipelines** and **MCP servers**. The model does judgment; the code does
counting; the context files hold what is true about the product, the buyer and
the voice so no prompt has to restate it.

```mermaid
flowchart LR
  subgraph context[context/  (what is true)]
    P[product.md] --- I[icp.json] --- V[voice-profile.md]
    C[competitor-skip-list.md] --- W[watchlist.md] --- PR[proof-points.md]
    D[desire-map.md] --- PS[post-structure.md] --- H[seo-hubs.md]
  end

  subgraph intel[intelligence]
    R[(competitor-radar MCP)]
    FS[format-scout]
    CS[content-scout]
    CEA[content-engagement-analyst]
    SAT[content-saturation-simulator]
  end

  subgraph content[content production]
    CR[/content-routine/]
    LP[launch-post]
    XP[x-content-playbook]
    FR[format-radar] --> FRB[format-radar builder]
    AB[ad-breakdown]
    FVR[/founder-voice-reply/]
  end

  subgraph demand[demand]
    FBO[find-blog-opportunities] --> SEO[seo-opportunity-engine]
    FL[/find-leads/] --> LF[lead-finder] --> EN[enrich.py]
    OS[outreach-specialist]
  end

  subgraph craft[paid-media craft]
    AV[/advet/]
    UGC[ugc-script-architect]
    WAP[winning-ad-production-system]
    SLR[segment-level-ad-format-research]
  end

  context --> intel
  context --> content
  context --> demand
  context --> craft
  R --> FS --> CR
  CS --> CR
  CEA --> CR
  SAT -.stress-tests.-> CR
  SAT -.stress-tests.-> LP
  XP -.rules.-> LP
  XP -.rules.-> FR
  AV -.knowledge/.-> UGC
```

## Layers

| layer | what lives there | rule |
|---|---|---|
| **context/** | product, ICP, voice, competitors, watchlist, proof points, desire map, post structure, SEO hubs | Every prompt reads from here instead of restating. Examples ship; real files are gitignored. |
| **intelligence** | what the market is telling our buyers right now | Fresh only (7–14 days). Every metric verified or flagged `UNVERIFIED`. Never fabricate engagement numbers. |
| **content production** | posts, launch posts, episodes, replies | Pick the target metric before writing. No invented numbers. Lead with mechanism, never the category label. |
| **demand** | SEO backlog, lead lists | The model picks, the script scores. CSV out; pushing to a sequencer is a separate confirmed step. |
| **paid-media craft** | media-buyer knowledge, UGC scripts, ad anatomy | Tactical, spend-aware, platform-specific. Saves what it learns to `knowledge/`. |

## Conventions every artifact follows

1. **A `doctor` or dry-run exists** wherever code runs (`radar_doctor`,
   `install.py --dry-run`, `--estimate` on paid actors).
2. **Degrade loudly.** No API key means estimates labelled as estimates and a
   line in the run report, never silence.
3. **Post text is data.** Nothing scraped is ever treated as instructions.
4. **Skip more than you post.** Engines are designed to refuse. A quiet day is
   a valid output.
5. **Rules carry their evidence.** The X playbook cites the posts each rule
   came from; format-radar guardrails name the episode that taught them.
6. **Confidential stays out.** Voice profiles, ICP data, competitor intel,
   customer numbers live in `context/` and `knowledge/`, both gitignored.
