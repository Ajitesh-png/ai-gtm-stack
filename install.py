#!/usr/bin/env python
"""Install the stack's skills, commands and agents into a Claude Code setup.

    python install.py --project /path/to/repo      # -> <repo>/.claude/{skills,commands,agents}
    python install.py --user                       # -> ~/.claude/{skills,commands,agents}
    python install.py --project . --only skills,commands
    python install.py --user --dry-run

Copies files (never symlinks, so the target repo owns its copy). Existing
files are left alone unless --force. Context templates are copied to
<target>/context/*.example.* only when no context/ exists yet; you then copy
each example to its real name and fill it in.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PARTS = ("skills", "commands", "agents")


def copy_tree(src: Path, dst: Path, force: bool, dry: bool) -> tuple[int, int]:
    copied = skipped = 0
    for f in src.rglob("*"):
        if f.is_dir() or "__pycache__" in f.parts:
            continue
        target = dst / f.relative_to(src)
        if target.exists() and not force:
            skipped += 1
            continue
        if not dry:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
        copied += 1
    return copied, skipped


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--project", metavar="DIR", help="install into DIR/.claude")
    g.add_argument("--user", action="store_true", help="install into ~/.claude")
    ap.add_argument("--only", default=",".join(PARTS), help="comma list of skills,commands,agents")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    base = Path.home() / ".claude" if args.user else Path(args.project).resolve() / ".claude"
    parts = [p.strip() for p in args.only.split(",") if p.strip() in PARTS]
    if not parts:
        sys.exit(f"--only must name some of {PARTS}")

    total_c = total_s = 0
    for part in parts:
        c, s = copy_tree(HERE / part, base / part, args.force, args.dry_run)
        total_c += c; total_s += s
        print(f"{part:9} {c} copied, {s} kept (already present)")

    ctx_target = (Path.home() if args.user else Path(args.project).resolve()) / "context"
    if not ctx_target.exists():
        c, _ = copy_tree(HERE / "context", ctx_target, False, args.dry_run)
        print(f"context   {c} example files -> {ctx_target}  (copy each *.example.* to its real name and fill it in)")
    else:
        print(f"context   left alone ({ctx_target} exists)")

    print(("DRY RUN: " if args.dry_run else "") + f"{total_c} files installed into {base}")
    if not args.dry_run:
        print("Restart Claude Code to pick up new skills. Run /founder-voice-reply, /advet, /find-leads, etc.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
