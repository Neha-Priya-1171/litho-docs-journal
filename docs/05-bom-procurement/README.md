# BOM and procurement (public part – no prices)

**Prices, quotations, vendor contacts and budget numbers are kept in a private place, not in this repo.**

## Part list
| Item | Subsystem | Key specification | Part number / source type | Qty | Status |
|---|---|---|---|---|---|
| DLP/DMD module | optics | pixel pitch, wavelength compatibility | | 1 | |
| Camera | optics | mono CMOS, global shutter, C-mount, USB3 | | 1 | |
| Objective | optics | magnification, NA, working distance, UV compatibility | | 1 | |
| Beam splitter | optics | UV/near-UV suitable | | 1 | |
| UV LED + constant-current driver | electrical | wavelength, irradiance, thermal control | | 1 | |
| XYZ(θ) stage + motors/drivers | mechanical | travel, resolution, repeatability | | 1 | |
| UV power meter | calibration | wavelength range | | 1 | |

Status values: `not ordered` · `ordered` · `received` · `tested` · `rejected`.
Rule of thumb from the plan: freeze wavelength and architecture first, order the DMD module early (lead time), freeze
objective + projection geometry, then order the camera and critical optics.
