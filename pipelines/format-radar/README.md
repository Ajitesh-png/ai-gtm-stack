# Format radar: episode builder

Production side of the `format-radar` skill. The skill decides *what* the
episode says (find a trending ad format, deconstruct why it converts, decide
where it is burned and where it is open, rebuild it for our ICP); these scripts
turn the decision into a post video without opening an editor.

| file | does |
|---|---|
| `post-template.html` | Template A, 1080×1920: equation rail (format found + pain pulled + product + agent → the ad) above a numbered "how it got here" reasoning trace, with a 614×1092 video frame cut out |
| `post-template-yapping.html` | Template B, 1824×1080: three true 9:16 panels playing simultaneously plus a why/call band, for formats cheap enough to test three hooks at once |
| `thread-cards.html` | static cards for thread posts 3–5 |
| `build.py` | reads an episode JSON, renders plates with headless Chrome, composites the clip segments and per-scene burned subtitles into an MP4 with ffmpeg |
| `build_grid.py` | same for Template B |
| `build_cards.py` | renders the thread cards to PNG |
| `episode.example.json` | a real episode spec (invented brand), showing the two research chips, the trace, the scenes and subtitle slots |

```bash
python pipelines/format-radar/build.py pipelines/format-radar/episode.example.json --still
```

Needs Chrome and ffmpeg on PATH. Generated scenes come from Higgsfield (or any
image/video model) and are referenced by path from the episode JSON; the
`assets/` folder is gitignored.

## The one rule the template encodes

The visual is an equation with **two** research inputs, never one: the format
came from *outside* the account (competitors' live ads), the pain came from
*inside* it (the account's own ad history). A generation tool can borrow a
format; only something reading your account can say which pain to point it
at. If the episode cannot name something only account access could reveal, the
skill says it is not worth shipping.

Guardrails the skill carries into production (learned from episodes that went
wrong): target ads whose mechanism lives in copy you can read, not video you
cannot watch; run-time in an ad library is not evidence of performance; never
report a pattern found under an unknown sort order; a controlled comparison of
two advertisers using the same fact beats any longevity claim.
