#!/usr/bin/env python3
"""Liste les skills installés pour Claude Code et Codex, avec leur description.

  list_skills.py [--dirs DIR ...] [--width N] [--json]

Par défaut lit ~/.claude/skills/*/SKILL.md et ~/.codex/skills/*/SKILL.md,
résout les liens symboliques et fusionne les doublons (même skill installé des
deux côtés). Sortie : tableau Markdown trié par nom.
Colonnes : skill | outils (claude, codex) | source (dossier réel) | description.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

DEFAULT_DIRS = {"claude": "~/.claude/skills", "codex": "~/.codex/skills"}


def frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(errors="replace")
    except OSError:
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return {}
    out: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val in (">", ">-", "|", "|-"):
                val = ""
            out[key] = val.strip("'\"")
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def source_label(real: Path) -> str:
    parts = real.parts
    for marker in ("tstack", "agents-config"):
        if marker in parts:
            return marker
    if ".system" in parts:
        return "système"
    home = str(Path.home())
    s = str(real)
    return "~" + s[len(home):] if s.startswith(home) else s


def collect(dirs: dict[str, str]) -> list[dict]:
    skills: dict[str, dict] = {}
    for tool, d in dirs.items():
        base = Path(os.path.expanduser(d))
        if not base.is_dir():
            continue
        for entry in sorted(base.iterdir()):
            skill_md = entry / "SKILL.md"
            if not skill_md.is_file():
                continue
            real = skill_md.resolve().parent
            fm = frontmatter(skill_md)
            name = fm.get("name") or entry.name
            key = str(real)
            item = skills.setdefault(key, {
                "name": name,
                "tools": [],
                "source": source_label(real),
                "path": key,
                "description": fm.get("description", ""),
            })
            if tool not in item["tools"]:
                item["tools"].append(tool)
    return sorted(skills.values(), key=lambda s: (s["name"].lower(), s["source"]))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dirs", nargs="*", help="dossiers tool=chemin, ex. claude=~/.claude/skills")
    ap.add_argument("--width", type=int, default=110, help="longueur max de la description")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    dirs = DEFAULT_DIRS
    if args.dirs:
        dirs = dict(d.split("=", 1) for d in args.dirs)
    items = collect(dirs)
    if args.json:
        print(json.dumps(items, ensure_ascii=False, indent=1))
        return
    print("| Skill | Outils | Source | Quand |")
    print("|---|---|---|---|")
    for s in items:
        desc = s["description"].replace("|", "/")
        if len(desc) > args.width:
            desc = desc[: args.width - 1].rstrip() + "…"
        print(f"| `{s['name']}` | {', '.join(s['tools'])} | {s['source']} | {desc} |")


if __name__ == "__main__":
    main()
