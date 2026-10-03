#!/usr/bin/env bash
# One-off: create GitHub issue labels. Needs the GitHub CLI (https://cli.github.com) and `gh auth login`.
for l in optics mechanical cad electrical software calibration process procurement cross-project safety docs blocked; do
  gh label create "$l" --force
done
