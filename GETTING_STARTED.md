# Getting started (new teammate, ~20 minutes)

Do this once per computer. After that, your daily routine is in [journal/README.md](journal/README.md).
Written for **Windows** first; Mac/Linux differences are marked.

## 1. Install the basics

| Tool | Get it | Check (in a terminal) |
|---|---|---|
| Git for Windows (includes Git LFS) | https://git-scm.com/download/win | `git --version` |
| Python 3.10+ | https://www.python.org/downloads/ – **tick "Add python.exe to PATH"** in the installer | `python --version` (or `py --version`) |
| VS Code | https://code.visualstudio.com | |
| VS Code extensions | open Extensions (Ctrl+Shift+X): *Python*, *Markdown All in One*, *YAML* | |

Restart VS Code after installing so it sees the new tools.

Tell Git who you are (once):

```powershell
git config --global user.name "Your Name"
git config --global user.email "the-email-on-your-github-account"
```

## 2. Get the repo

1. Ask the repo owner to add you under **Settings → Collaborators** and accept the email invite.
2. In VS Code press **Ctrl+Shift+P → Git: Clone**, paste the repo URL
   (`https://github.com/Neha-Priya-1171/litho-docs-journal.git`), choose a folder such as
   `C:\Users\you\Projects`, and click **Open**. Choose "Yes, I trust the authors".
3. Sign in to GitHub in the browser when VS Code asks.

## 3. Python environment

Open the VS Code terminal (**Ctrl+`**, PowerShell). It should already be inside the repo folder.

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

The prompt starts with `(.venv)` when active. Run the `activate` line again in every new terminal tab.
If VS Code asks about the new environment, click **Yes**.

*"Running scripts is disabled on this system"?* Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`,
open a new terminal, and retry.

## 4. Set your author id

Use your lowercase id from `team.yml` (for example `neha`).

```powershell
setx LITHO_AUTHOR yourid           # for NEW terminals
$env:LITHO_AUTHOR = "yourid"       # for the terminal that is open now
```

Mac/Linux: `echo 'export LITHO_AUTHOR=yourid' >> ~/.zshrc` (bash: `~/.bash_profile`), then open a new tab.

## 5. Check everything works

```powershell
git pull
python tools/lint_journal.py
```

You should see `checked N entries, 0 error(s)`.

## 6. Write your first entry

```powershell
python tools/new_entry.py
```

Fill in the generated file under `journal\YYYY\MM\` (write `None.` where a section doesn't apply), then:

```powershell
python tools/lint_journal.py
git add journal
git commit -m "journal: yourid - first entry"
git pull --rebase
git push
```

Open the **Actions** tab on GitHub and wait for a green tick, then open `journal/INDEX.md` to see your entry.

Attaching handwritten notes, correcting entries and the full daily routine: [journal/README.md](journal/README.md).

## Quick fixes

| Problem | Fix |
|---|---|
| `python` not recognised | Reinstall Python with "Add to PATH" ticked, or use `py` instead of `python` |
| `ModuleNotFoundError: yaml` | venv not active (look for `(.venv)`), or requirements not installed |
| Can't activate the venv | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, new terminal |
| Push rejected | `git pull --rebase`, then `git push` (the index bot commits to `main`) |
| Linter: "not in team.yml" | Use the exact id from `team.yml`; ask the owner to add you |
| iPhone photos are .HEIC | Export/share them as JPG, or `python -m pip install pillow-heif` |
| Stuck | Ask in the team chat and paste the exact error text |
