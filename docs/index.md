# Lithographer – system overview

*Curated and verified. For the raw day-by-day record see the repo's `journal/`.*

## Goal
Build a maskless photolithography system from scratch: take a digital layout (GDS) and transfer it onto
photoresist-coated silicon with digitally controlled optical exposure.

```
GDS / CAD layout → pattern processing → DMD → projection optics → beam splitter
                 → microscope objective → photoresist on wafer → UV exposure → development
```

The DMD replaces the physical photomask. A camera shares the optical path (via the beam splitter) so it sees the same
wafer region that is exposed; it drives alignment, focus and calibration. An optional eyepiece path for human viewing
is possible but needs proper UV protection (see [safety](07-safety.md)).

## Core engineering principle
Every DMD pixel → known wafer coordinate → camera observes it → stage positions it → software controls the exposure.

## Key relations we design with
| Relation | Meaning |
|---|---|
| p_wafer = M × p | projected DMD pixel pitch (p = DMD pitch, M = projection magnification) |
| R ≈ k₁ λ / NA | resolution; DMD pixel size alone does **not** set it |
| DOF ≈ k₂ λ / NA² | depth of focus shrinks fast as NA rises |
| D = I × t | exposure dose = irradiance × time |

## Subsystems
| Folder | Covers |
|---|---|
| [01-optics](01-optics/README.md) | UV source, illumination, DMD, projection, beam splitter, objective, camera optics |
| [02-mechanical-cad](02-mechanical-cad/README.md) | frame, mounts, XYZ(θ) stage, wafer holder, enclosure |
| [03-electronics](03-electronics/README.md) | LED driver, thermal sensing, motors, controller, sensors, interlocks |
| [04-software](04-software/README.md) | GDS → raster → DMD, camera, alignment, autofocus, motion, GUI |
| [05-bom-procurement](05-bom-procurement/README.md) | part list and status (no prices) |
| [06-calibration-tests](06-calibration-tests/README.md) | camera, stage, DMD→wafer, distortion, illumination calibration; test results |
| [07-safety](07-safety.md) | UV and lab safety |
| [08-process](08-process/README.md) | wafer prep, coating, bake, exposure, development, inspection |
| [09-cross-project](09-cross-project/README.md) | interfaces with spin coater, sputter, furnace |

Also: [milestones](milestones.md) · [decisions](decisions/README.md) · [known issues](known-issues.md) · [references](references.md)
