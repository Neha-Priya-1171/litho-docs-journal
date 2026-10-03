#!/usr/bin/env python3
"""Check every journal entry follows the standard template. Exit 1 on errors.

    python tools/lint_journal.py
"""
import os
import sys

from common import (ENTRY_RE, GENERATED_NAMES, IMG_RE, JOURNAL, ROOT, as_list,
                    iter_entry_paths, load_team, parse_entry, promote_value,
                    scan_files, sections)

REQUIRED_KEYS = ["title", "date", "author", "subsystem", "status", "promote_to_docs"]
REQUIRED_SECTIONS = [
    ("goal", "Goal of this session"),
    ("what i did", "What I did"),
    ("results", "Results and numbers"),
    ("decisions", "Decisions and why"),
    ("problems", "Problems and what didn't work"),
    ("next steps", "Next steps"),
]


def lint(path, team):
    errs, warns = [], []
    y, mo, d, file_author, _slug = ENTRY_RE.match(path.name).groups()
    if path.parent.name != mo or path.parent.parent.name != y:
        errs.append(f"file should live in journal/{y}/{mo}/")
    try:
        e = parse_entry(path)
    except ValueError as ex:
        return [str(ex)], []
    meta, body = e["meta"], e["body"]

    for k in REQUIRED_KEYS:
        if meta.get(k) in (None, "", []):
            errs.append(f"front matter is missing '{k}'")
    if str(meta.get("date")) != f"{y}-{mo}-{d}":
        errs.append(f"front matter date ({meta.get('date')}) does not match file name ({y}-{mo}-{d})")

    people = team["people"]
    author = str(meta.get("author", ""))
    if author != file_author:
        errs.append(f"author '{author}' does not match file name author '{file_author}'")
    if author and author not in people:
        errs.append(f"author '{author}' is not in team.yml")
    for p in as_list(meta.get("people")):
        if p not in people:
            errs.append(f"person '{p}' is not in team.yml")

    subs = as_list(meta.get("subsystem"))
    for s in subs:
        if s not in team["subsystems"]:
            errs.append(f"subsystem '{s}' is not in team.yml ({', '.join(team['subsystems'])})")
    if meta.get("status") not in (None, "") and meta["status"] not in team["statuses"]:
        errs.append(f"status '{meta['status']}' must be one of {team['statuses']}")
    if promote_value(meta) not in ("no", "yes", "done"):
        errs.append("promote_to_docs must be \"no\", \"yes\" or \"done\"")
    if "hours" in meta and not isinstance(meta["hours"], (int, float)):
        errs.append("hours must be a number")
    if promote_value(meta) == "done" and not meta.get("promoted_in"):
        warns.append("promote_to_docs is 'done' but there is no 'promoted_in:' path")

    secs = sections(body)
    for key, label in REQUIRED_SECTIONS:
        hits = [h for h in secs if key in h]
        if not hits:
            errs.append(f"missing section '## {label}'")
        elif not any(secs[h] for h in hits):
            errs.append(f"section '## {label}' is empty (write 'None.' if there is nothing to say)")

    for link in IMG_RE.findall(body):
        if link.startswith(("http://", "https://", "data:")):
            continue
        if not (path.parent / link.split("#")[0]).exists():
            errs.append(f"image/link target not found: {link}")

    scans = scan_files(path)
    if not scans and not IMG_RE.search(body):
        warns.append("no handwritten notes attached (fine if there were none)")
    for f in scans:
        if f.stat().st_size > 1_500_000:
            warns.append(f"{f.name} is {f.stat().st_size // 1024} KB – run tools/prep_scans.py to shrink it")
    return errs, warns


def main():
    team = load_team()
    gha = os.environ.get("GITHUB_ACTIONS") == "true"
    n_err = 0

    for p in sorted(JOURNAL.rglob("*.md")) if JOURNAL.is_dir() else []:
        generated = p.name in GENERATED_NAMES or {"by-person", "by-subsystem"} & set(p.parts)
        if not generated and not ENTRY_RE.match(p.name):
            n_err += 1
            msg = "bad file name. Use YYYY-MM-DD_author_short-slug.md (lowercase, no spaces) – create entries with tools/new_entry.py"
            print(f"ERROR {p.relative_to(ROOT)}: {msg}")
            if gha:
                print(f"::error file={p.relative_to(ROOT)}::{msg}")

    paths = iter_entry_paths()
    for p in paths:
        errs, warns = lint(p, team)
        rel = p.relative_to(ROOT)
        for m in errs:
            n_err += 1
            print(f"ERROR   {rel}: {m}")
            if gha:
                print(f"::error file={rel}::{m}")
        for m in warns:
            print(f"warning {rel}: {m}")
            if gha:
                print(f"::warning file={rel}::{m}")

    print(f"\nchecked {len(paths)} entr{'y' if len(paths) == 1 else 'ies'}, {n_err} error(s)")
    sys.exit(1 if n_err else 0)


if __name__ == "__main__":
    main()
