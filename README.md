# Litho Documentation & Journal – maskless photolithography stepper

A from-scratch maskless photolithography system built by the Hacker Fab team at Mahindra University.
A digital chip layout (GDS) is rasterised, shown on a DMD, and projected through a microscope objective onto
photoresist-coated silicon. A camera sharing the same optics is used for viewing, alignment and focus.

> **Status:** early build – see [docs/milestones.md](docs/milestones.md) for where we are.

```
GDS layout → rasteriser → DMD → projection optics → beam splitter → objective → resist on wafer
                                                         ↑
                                                       camera (view / align / focus)
```

## Where to look

| I want to… | Go to |
|---|---|
| understand the machine | [docs/index.md](docs/index.md) |
| see the current state of each subsystem | [docs/](docs/) – optics, mechanical/CAD, electronics, software, calibration, process |
| know why we chose something | [docs/decisions/](docs/decisions/) |
| see known problems | [docs/known-issues.md](docs/known-issues.md) |
| see what the team actually did, day by day | [journal/INDEX.md](journal/INDEX.md) (by person and by subsystem) |
| find the reference material we build on | [docs/references.md](docs/references.md) |

## How this repo is organised

- **`docs/`** – the curated, verified picture of the project. Changed only through reviewed pull requests.
- **`journal/`** – the raw, dated record of every work session, including handwritten-note scans.
  Append-only, one file per person per session.
- **`cad/`, `data/`, `src/`** – CAD sources and exports, raw measurements, software.

**Writing a journal entry? Start with [journal/README.md](journal/README.md).**
Team workflow: [CONTRIBUTING.md](CONTRIBUTING.md). First-time setup: [SETUP.md](SETUP.md).


