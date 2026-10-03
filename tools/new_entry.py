#!/usr/bin/env python3
"""Create a new journal entry (and its scan folder) from the template.

    python tools/new_entry.py --author neha --subsystem optics,cad --title "Relay lens distance calc"
    python tools/new_entry.py            # asks you the questions

Tip: set LITHO_AUTHOR=neha in your shell profile so you never type --author.
"""
import argparse
import datetime
import os
import re
import sys

from common import JOURNAL, ROOT, load_team, scan_folder


def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:40].strip("-")
    return s or "entry"


def split(s):
    return [x.strip().lower() for x in (s or "").split(",") if x.strip()]


def main():
    team = load_team()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--author")
    ap.add_argument("--title")
    ap.add_argument("--subsystem", help="comma separated")
    ap.add_argument("--people", help="comma separated; defaults to just the author")
    ap.add_argument("--date", help="YYYY-MM-DD, default today")
    ap.add_argument("--hours", default="0")
    a = ap.parse_args()

    author = (a.author or os.environ.get("LITHO_AUTHOR") or input(f"Author {list(team['people'])}: ")).strip().lower()
    if author not in team["people"]:
        sys.exit(f"'{author}' is not in team.yml")
    title = (a.title or input("Short title: ")).strip()
    if not title:
        sys.exit("a title is required")
    subs = split(a.subsystem or input(f"Subsystem(s), comma separated {list(team['subsystems'])}: "))
    bad = [s for s in subs if s not in team["subsystems"]]
    if not subs or bad:
        sys.exit(f"unknown subsystem(s): {bad or 'none given'}. Allowed: {list(team['subsystems'])}")
    people = [author] + [p for p in split(a.people) if p != author]
    for p in people:
        if p not in team["people"]:
            sys.exit(f"'{p}' is not in team.yml")
    date = a.date or datetime.date.today().isoformat()
    try:
        datetime.date.fromisoformat(date)
    except ValueError:
        sys.exit("date must look like 2026-10-03")
    y, mo, _ = date.split("-")

    path = JOURNAL / y / mo / f"{date}_{author}_{slugify(title)}.md"
    if path.exists():
        sys.exit(f"{path.relative_to(ROOT)} already exists – use a different title or edit that file")

    tpl = (ROOT / "templates" / "journal_entry.md").read_text(encoding="utf-8")
    fill = {
        "title": title.replace('"', '\\"'),
        "date": date,
        "author": author,
        "people": "[" + ", ".join(people) + "]",
        "subsystem": "[" + ", ".join(subs) + "]",
        "hours": a.hours,
    }
    # the H1 title line should not have escaped quotes
    out = tpl.replace("# {{title}}", "# " + title)
    for k, v in fill.items():
        out = out.replace("{{" + k + "}}", v)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(out, encoding="utf-8")
    scan_folder(path).mkdir(exist_ok=True)

    rel = path.relative_to(ROOT)
    print(f"created {rel}\n")
    print("next:")
    print(f"  1. fill in {rel}")
    print(f"  2. python tools/prep_scans.py {rel} --from <folder with photos of your notebook pages>")
    print("  3. python tools/lint_journal.py")
    print(f"  4. git add journal && git commit -m \"journal: {author} – {title}\" && git push")


if __name__ == "__main__":
    main()
