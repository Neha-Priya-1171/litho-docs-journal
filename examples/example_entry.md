---
title: "(EXAMPLE) DMD pixel to wafer pixel and exposure dose sanity check"
date: 2026-10-03
author: neha
people: [neha]
subsystem: [optics]
components: [DMD, objective]
keywords: [magnification, dose, resolution]
cross_project: none
hours: 2
status: done
promote_to_docs: "yes"
---

# (EXAMPLE) DMD pixel to wafer pixel and exposure dose sanity check

*This is an illustrative entry showing the expected level of detail. It is not a real session.*

## Goal of this session
Check how big one DMD pixel is on the wafer for a candidate projection magnification, and what exposure time a given irradiance implies.

## What I did
1. Used p_wafer = M × p with a 7.6 µm DMD pixel pitch and M = 0.25.
2. Used D = I × t with I = 10 mW/cm² and t = 5 s.
3. Wrote both calculations on notebook pages 12–13 (scans below).

## Results and numbers
- p_wafer = 0.25 × 7.6 µm = **1.9 µm** projected pixel pitch.
- D = 10 mW/cm² × 5 s = **50 mJ/cm²**.
- 1.9 µm is the projected *pixel pitch*, not the lithographic resolution: resolution still depends on wavelength, NA, aberrations, focus and resist.

## Decisions and why
None. M = 0.25 is only a candidate until the objective and field of view are fixed.

## Problems and what didn't work
None this session. Unit slip (mW vs W) caught and fixed on page 12.

## Open questions
- Which wavelength do we freeze? It changes the resist dose needed.
- What field of view does the objective give with this magnification?

## Next steps
- Neha: repeat the calculation for 2–3 candidate objectives.
- Mihir: check DMD datasheet pixel pitch against the module we plan to buy.

## Files added or changed
`data/2026-10-03_dose-calc/dose.csv`

## Handwritten notes
<!-- scans would be embedded here by tools/prep_scans.py -->

## Links
- Project baseline: docs/index.md
