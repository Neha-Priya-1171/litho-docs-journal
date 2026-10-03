# How we work

```
work → journal entry (+ scans) → push → verify → docs (via PR) → milestone
```

## The daily routine (every Litho session, about 5 minutes)

*Full step-by-step guide with examples, corrections and troubleshooting: [journal/README.md](journal/README.md).*

```bash
git pull
python tools/new_entry.py                      # asks: title, subsystem(s); creates the entry + scan folder
# ... fill in the entry ...
python tools/prep_scans.py journal/2026/10/<your-entry>.md --from ~/Downloads/notebook-photos
python tools/lint_journal.py                   # catches missing sections / typos in tags
git add journal && git commit -m "journal: <you> - <short title>" && git push
```

Rules for journal entries:

1. **One entry per person per session.** If two of you worked together, put both in `people:` and one of you writes it.
2. **A short entry beats a perfect missing one.** One honest line per required section is enough.
3. **Always fill "Problems and what didn't work".** Failed attempts are what we will want to find in six months.
4. **Never edit old entries** except to fix typos or add a correction at the bottom (`### Correction – date`).
5. **Handwritten pages:** write date + your name at the top of each page, number the pages, scan with a phone
   scanner app, run `prep_scans.py`. Keep the physical notebook. Retype any number you will need later
   into "Results and numbers" – scans are not searchable.
6. Large raw files (camera dumps, big CAD) don't go in the journal folder: see "Files" below.

## Verified = promoted into `docs/`

Something counts as **verified** when it has data or a calculation attached **and** a teammate other than the
author approves the pull request that puts it in `docs/`.

1. Set `promote_to_docs: "yes"` in the journal entry. It appears in `journal/PROMOTE_QUEUE.md`.
2. Branch (`docs/optics-relay-calc`), distil the result into the right `docs/` folder, open a PR.
   Link the journal entries and data as evidence.
3. A teammate reviews and merges. Set the entry to `"done"` and add `promoted_in: docs/...`.

Major choices (objective, wavelength, stage design, camera, ...) also get a **decision record** in
`docs/decisions/` (copy `templates/decision_record.md`): what we chose, what we rejected, *why*.

## Git conventions

- `journal/` – commit straight to `main`. Message: `journal: neha - relay lens calc`.
- everything else (docs, code, CAD, tools) – branch + pull request + one teammate's approval.
  Branch names: `optics/…`, `sw/…`, `cad/…`, `docs/…`.
- Milestones are tagged: `v0.1-first-projection`, `v0.2-first-exposure`, …
- Tasks live in GitHub Issues, labelled by subsystem (`tools/create_labels.sh`).

## Files

| Kind | Where | Notes |
|---|---|---|
| Notebook scans | `journal/YYYY/MM/<entry>/` | made small by `prep_scans.py` (≈1600 px, JPEG) |
| CAD | `cad/<part>/` – STEP/STL exports + native files | tracked by Git LFS (see `.gitattributes`) |
| Measurements | `data/YYYY-MM-DD_<what>/` | CSV + a short README: setup, units, instrument |
| Layouts (GDS) | `data/layouts/` | LFS |
| Code | `src/` | |
| Photos / videos | `docs/media/` for a few; link videos instead of committing them | |

## Privacy – decide before every commit

**Never commit:** prices, quotations, invoices, vendor contacts, budget numbers, anything institutional.
Those live in a separate **private** place (a private repo or the team Drive). `docs/05-bom-procurement/`
holds the part list *without* prices. If something sensitive is committed, tell the team immediately –
removing it from Git history is painful, so don't wait.
