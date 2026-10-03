# Software

**Status:** not started  ·  **Owner:** 

## Scope
GDS handler, rasteriser (vector → binary/grayscale), DMD control (pattern sequencing, timing, triggering), camera acquisition, alignment (ΔX, ΔY, Δθ), autofocus, stage control, calibration, GUI, logging. Python first; C/C++ only where timing needs it. Code lives in `src/`.

## Current state (verified)
*Nothing promoted yet. Add results here via PR, each with an evidence link to journal entries / data.*

## Open questions / decisions pending
- DMD control interface
- alignment algorithm and mark design
- how software and motion controller share responsibilities

## Raw history
See the journal for this subsystem: [by-subsystem view](../../journal/INDEX.md).
