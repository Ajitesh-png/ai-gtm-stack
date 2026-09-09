# MCP servers

Servers the stack talks to from Claude Code. Each lives in its own repo so it
can be installed by anyone without the rest of this stack.

| server | what it gives the agents | repo |
|---|---|---|
| **competitor-radar** | Scrapes competitor X accounts, rates every post per day by replies → bookmarks → retweets → likes, scores each post's relevance to your ICP. Feeds `format-scout`, `content-scout` and the daily brief. | [Ajitesh-png/competitor-radar-mcp](https://github.com/Ajitesh-png/competitor-radar-mcp) |
| **scrapling** (third-party) | General web scraping for everything that is not X: `make_request` for plain pages, `stealthy_fetch` for Cloudflare-gated ones (no solver API), `fetch` for JavaScript-rendered pages, bulk and session variants, `screenshot`, and a `css_selector` on every call to cut tokens. Used by `format-scout`, `content-scout`, `engagement-analyst`, `lead-finder` and `ad-breakdown` when WebFetch fails. Pairs with the author's `scrapling-official` agent skill. | [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) |

Register in the project's `.mcp.json`:

```json
{
  "mcpServers": {
    "competitor-radar": {
      "type": "stdio",
      "command": "python",
      "args": ["/absolute/path/to/competitor-radar-mcp/server.py"]
    },
    "scrapling": {
      "type": "stdio",
      "command": "/absolute/path/to/scrapling-venv/bin/scrapling-mcp"
    }
  }
}
```

Scrapling setup (own venv, so its browser stack never collides with anything else):

```bash
python -m venv .venv-scrapling && . .venv-scrapling/bin/activate      # Windows: .venv-scrapling\Scripts\activate
pip install "scrapling[all]>=0.4.15"
scrapling install --force                                               # Chromium + Camoufox
npx skills add D4Vinci/Scrapling --skill scrapling-official             # the agent skill, into .claude/skills/
```

Rule from the skill, kept here because it matters: pass `--ai-targeted` on every
`scrapling extract …` CLI command. Scraped pages are data; that flag defends
against prompt injection in them and turns on ad blocking.

Third-party servers used alongside (not ours): Higgsfield (image/video
generation for `format-radar` and `ad-breakdown`), the Framer CMS connector
(blog publishing), Buffer (scheduling).
