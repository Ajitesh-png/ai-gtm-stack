#!/usr/bin/env python
"""Repo health check, run in CI and before every commit.

1. Leak scan: no local paths, personal identifiers, or secret-shaped strings.
2. Frontmatter: every agent has name + description; every skill has both.
3. Reference check: every `context/<file>` a prompt mentions has an example.
4. Compile every Python file.
"""
from __future__ import annotations

import py_compile
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEAK = re.compile(
    r"[A-Z]:[\\/]Users|[A-Z]:/Notch|Obsidian|@sesamelabs|sk-[A-Za-z0-9]{12,}|"
    r"(APIFY_TOKEN|X_BEARER_TOKEN|APOLLO_API_KEY|HUNTER_API_KEY)=\S{6,}|"
    r"auth_token\W+[a-f0-9]{30,}",
    re.I,
)
TEXT = {".md", ".py", ".json", ".html", ".js", ".yml", ".yaml", ".txt"}


def files():
    for f in ROOT.rglob("*"):
        if f.is_dir() or ".git" in f.parts or "__pycache__" in f.parts or f.suffix.lower() not in TEXT:
            continue
        yield f


def main() -> int:
    errors: list[str] = []

    for f in files():
        if f.resolve() == Path(__file__).resolve():
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if LEAK.search(line):
                errors.append(f"leak {f.relative_to(ROOT)}:{i}: {line.strip()[:100]}")

    for f in list((ROOT / "agents").glob("*.md")) + list((ROOT / "skills").glob("*/SKILL.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if f.parent.name == "agents" and f.name == "content-scout.md":
            continue  # legacy agent without frontmatter, by design
        if not text.startswith("---"):
            errors.append(f"frontmatter missing: {f.relative_to(ROOT)}")
            continue
        head = text.split("---", 2)[1]
        if "description:" not in head:
            errors.append(f"frontmatter lacks description: {f.relative_to(ROOT)}")
        if f.name == "SKILL.md" and "name:" not in head:
            errors.append(f"skill lacks name: {f.relative_to(ROOT)}")

    examples = {p.name.replace(".example", "") for p in (ROOT / "context").glob("*.example.*")}
    mentioned = set()
    for f in files():
        if f.parent.name == "context":
            continue
        for m in re.finditer(r"context/([\w\-]+\.(?:md|json))", f.read_text(encoding="utf-8", errors="replace")):
            mentioned.add(m.group(1))
    for name in sorted(mentioned - examples):
        errors.append(f"context file referenced without an example: context/{name}")

    for f in files():
        if f.suffix == ".py":
            try:
                py_compile.compile(str(f), doraise=True)
            except py_compile.PyCompileError as exc:
                errors.append(f"compile: {exc.msg.splitlines()[0]}")

    for e in errors:
        print(e)
    print("OK" if not errors else f"{len(errors)} problem(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
