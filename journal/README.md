**First time here? Read [GETTING_STARTED.md](GETTING_STARTED.md).**

# Litho journal – how to use it

This folder is the **dated record of everything we do on Litho**: calculations, CAD, soldering, code, failed
experiments, meetings, procurement chasing, work on other projects that touches Litho. Anyone can open it months
later and answer *"what did X do?"* or *"what have we tried with the optics?"*

Browse it: **[INDEX.md](INDEX.md)** (everything) · `by-person/` · `by-subsystem/` · [PROMOTE_QUEUE.md](PROMOTE_QUEUE.md)
(results waiting to be written into the official docs). Those pages are auto-generated – never edit them by hand.

---

## The rule

> **Every time you work on Litho, you write one journal entry and push it before you close your laptop.**
> One entry = one person + one session. A short honest entry is better than a perfect missing one.

---

## One-time setup (each person, once)

Full walkthrough with install links: [GETTING_STARTED.md](../GETTING_STARTED.md). The short version, typed in the
VS Code terminal (**PowerShell** on Windows):

```powershell
git clone https://github.com/Neha-Priya-1171/litho-docs-journal.git
cd litho-docs-journal
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
setx LITHO_AUTHOR neha              # your id from team.yml; applies to NEW terminals
$env:LITHO_AUTHOR = "neha"          # same thing for the terminal that is open right now
```

Replace `neha` with your own id from `team.yml`. Your prompt starts with `(.venv)` when the environment is active.
You must run `.venv\Scripts\activate` again in every new terminal tab.

<details>
<summary>Mac / Linux version</summary>

```bash
git clone https://github.com/Neha-Priya-1171/litho-docs-journal.git
cd litho-docs-journal
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
echo 'export LITHO_AUTHOR=neha' >> ~/.zshrc     # bash users: ~/.bash_profile
```
</details>

**Windows tips**
- If `python` isn't found, try `py`. If activation says *running scripts is disabled*, run
  `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, open a new terminal, and retry.
- Put paths with spaces in quotes, e.g. `--from "C:\Users\you\Downloads\my notebook photos"`.
- Using Command Prompt instead of PowerShell? Activate with `.venv\Scripts\activate.bat`.
- Git LFS ships with Git for Windows. It's only needed once we commit large CAD/GDS files.

---

## Every session – step by step

**1. Before you start**
```bash
git pull
```

**2. Do your work.** On paper, write the **date and your name at the top of each page** and number the pages.

**3. After the session, create the entry**
```bash
python tools/new_entry.py
```
It asks for a short title and the subsystem(s) (optics, mechanical, cad, electrical, software, procurement,
calibration, process, cross-project). If two people worked together, add `--people nishchay,mihir`.
It creates `journal/YYYY/MM/YYYY-MM-DD_you_title.md` plus a folder for your scans.

**4. Fill in the entry** (open the file in any editor). Replace each comment with real text. Minimum is one line
per section; write `None.` where there's nothing to say:

| Section | What to write |
|---|---|
| Goal | what you set out to do |
| What I did | steps, enough for someone to repeat it |
| Results and numbers | values **with units**, links to files in `data/` |
| Decisions and why | choices made. A *major* choice also gets a record in `docs/decisions/` |
| Problems and what didn't work | **don't skip this** – failures are the most valuable part |
| Next steps | who does what next |

In the front matter at the top set: `hours`, `status` (`done` / `in-progress` / `blocked`), `components`
(e.g. `[objective, DMD]`), and `promote_to_docs: "yes"` if the result is ready to be turned into official docs.

**5. Attach your handwritten notes**
1. Photograph/scan the pages with a phone scanner app (Microsoft Lens, Adobe Scan, Google Drive scan). Put them
   in one folder on your computer.
2. Run
   ```bash
   python tools/prep_scans.py journal/2026/10/<your-entry>.md --from "C:\Users\you\Downloads\my-notebook-photos"
   ```
   Photos are rotated, shrunk to a repo-friendly size, renamed `p1.jpg, p2.jpg…` and embedded in the entry.
3. Retype any **number or equation you'll need later** into "Results and numbers". Scans aren't searchable.
4. Keep the paper notebook – the scan is a working copy.

**6. Check and push**
```bash
python tools/lint_journal.py
git add journal data cad src
git commit -m "journal: neha - relay lens calc"
git pull --rebase      # the index bot also commits to main, so always do this before pushing
git push
```
The repo's GitHub Action re-checks the entry and refreshes the indexes within a minute or two. If the **journal**
check shows a red ✗ in the Actions tab, open it – it names the file and the problem.

That's it.

---

## Updating, continuing and correcting

| Situation | What to do |
|---|---|
| You worked in two stretches the same day | Add to the **same** entry and push again. |
| You continue the same task tomorrow | **New entry**, new date. Link the earlier one under "Links". |
| Two separate topics on one day | Two entries (different titles/subsystems), so each shows up in the right subsystem view. |
| You and a teammate worked together | One of you writes it; list both in `people:`. They'll both see it in their by-person page. |
| You forgot yesterday | Write it today with `--date YYYY-MM-DD` for the day it happened. |
| Typo | Fix it in place. |
| You were **wrong** about a result | Don't rewrite history. Add at the bottom: `### Correction – 2026-10-09` and what is now believed (and why). |
| You're stuck | Set `status: blocked`, say what's needed under Next steps, and open a GitHub Issue. |
| A result is verified and useful | Set `promote_to_docs: "yes"`. Later, after it's written into `docs/` via PR, change to `"done"` and add `promoted_in: docs/01-optics/...`. |
| Work on spin coater / sputter / furnace that affects Litho | Entry with subsystem `cross-project` (or `process`); set `cross_project: spin-coater` etc. |

---

## Common errors from `lint_journal.py`

| Message | Fix |
|---|---|
| `section '## …' is empty` | Write something, or `None.` |
| `subsystem 'x' is not in team.yml` | Use one of the listed ids, comma-separated in `[ ]` |
| `date … does not match file name` | Make the front-matter `date:` equal the date in the file name |
| `author … does not match file name` | Your id must match the name in the file |
| `image/link target not found` | Re-run `prep_scans.py` or fix the path |
| `bad file name` | Use `tools/new_entry.py` instead of creating files by hand |
| `front matter is not valid YAML` | Check the `---` lines at the top, and that brackets/quotes are closed |

Warnings (yellow) don't block anything.

---

## No terminal? Use the GitHub website

1. On GitHub open `templates/journal_entry.md`, copy its contents.
2. Go to `journal/` → **Add file → Create new file**. Name it `2026/10/2026-10-03_yourid_short-title.md`
   (lowercase, no spaces) and paste in the template. Fill it in.
3. Create the scan folder by uploading photos (**Add file → Upload files**) into
   `journal/2026/10/2026-10-03_yourid_short-title/`. Photos from the website won't be auto-shrunk, so keep them
   under about 500 KB each (most scanner apps have a "reduce size" option), and embed them in the entry as
   `![p1](2026-10-03_yourid_short-title/p1.jpg)`.
4. Commit directly to `main`. The Action will tell you if anything in the entry needs fixing.

---

## What never goes in the journal

Prices, quotations, invoices, vendor contacts, budget numbers or anything institutional – those live in the
private admin repo / team Drive. Raw camera dumps and big CAD files: see "Files" in
[CONTRIBUTING.md](../CONTRIBUTING.md).
