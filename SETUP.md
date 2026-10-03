# First-time setup (one person, ~30 minutes)

1. **Create the GitHub repo** (start **private**; make it public later when `README` + `docs/` are presentable).
   Push this folder as the first commit.
2. **Edit `team.yml`** – your three ids/names and GitHub usernames.
3. **Edit `.github/CODEOWNERS`** – replace the placeholder usernames. Owners are auto-requested as reviewers on PRs.
4. **Git LFS:** every teammate runs `git lfs install` once (https://git-lfs.com). GitHub's free LFS quota is
   small (about 1 GB storage / 1 GB bandwidth a month), so keep CAD exports and GDS files tidy.
5. **Python:** `python -m venv .venv`, activate it, `pip install -r requirements.txt`.
6. **Actions:** make sure GitHub Actions is enabled (Settings → Actions). The `journal` workflow lints every entry and
   rebuilds the indexes on each push.
7. **Labels (optional):** `./tools/create_labels.sh` (needs the GitHub CLI).
8. **Branch rules – pick one mode:**
   - **Mode A (recommended for 3 people): convention.** No branch protection. `journal/` is pushed straight to `main`;
     everything else goes through a PR by agreement (CODEOWNERS auto-requests the reviewers).
   - **Mode B (strict): Settings → Rules → Rulesets** → require a pull request + "Require review from Code Owners",
     with *required approvals = 0*. Then docs/code PRs need an owner's approval, but journal-only PRs merge with no
     review. Note that GitHub cannot exempt a folder from "require a PR", so journal entries then also go via a PR
     (`gh pr create --fill && gh pr merge --auto --squash`), and the index-rebuild bot needs to be allowed to
     push (add it to the ruleset bypass list), or switch the workflow to open a PR instead.
9. **Optional docs website:** `pip install mkdocs-material`, `mkdocs serve` to preview. To publish, run the
   `docs-site` workflow manually (Actions tab) and set Settings → Pages → source = `gh-pages` branch.
   (Pages on a private repo needs a paid GitHub plan; for a student team, publish only once the repo is public.)
10. **Finance / procurement:** create a separate **private** repo (e.g. `litho-admin`) or a private Drive folder for
    prices, quotes and the procurement status sheet. Do not put those in this repo.
11. Send everyone `journal/README.md` – it is the user guide. Everyone writes their first entry with `python tools/new_entry.py`. Look at
    `examples/example_entry.md` for the expected level of detail.

## Handy commands

```bash
python tools/new_entry.py                  # new journal entry
python tools/prep_scans.py ENTRY.md --from FOLDER   # import + shrink + embed notebook photos
python tools/lint_journal.py               # check all entries
python tools/build_indexes.py              # rebuild by-person / by-subsystem views locally
mkdocs serve                               # preview the docs site
```
