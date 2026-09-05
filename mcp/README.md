# MCP servers

Servers the stack talks to from Claude Code. Each lives in its own repo so it
can be installed by anyone without the rest of this stack.

| server | what it gives the agents | repo |
|---|---|---|
| **competitor-radar** | Scrapes competitor X accounts, rates every post per day by replies → bookmarks → retweets → likes, scores each post's relevance to your ICP. Feeds `format-scout`, `content-scout` and the daily brief. | [Ajitesh-png/competitor-radar-mcp](https://github.com/Ajitesh-png/competitor-radar-mcp) |

Register in the project's `.mcp.json`:

```json
{
  "mcpServers": {
    "competitor-radar": {
      "type": "stdio",
      "command": "python",
      "args": ["/absolute/path/to/competitor-radar-mcp/server.py"]
    }
  }
}
```

Third-party servers used alongside (not ours): Higgsfield (image/video
generation for `format-radar` and `ad-breakdown`), the Framer CMS connector
(blog publishing), Buffer (scheduling).
