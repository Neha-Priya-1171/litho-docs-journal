#!/usr/bin/env python3
"""Shrink + auto-rotate notebook photos and attach them to a journal entry.

    # import photos from a folder (renamed p1.jpg, p2.jpg ... continuing any existing numbering)
    python tools/prep_scans.py journal/2026/10/2026-10-03_neha_optics.md --from ~/Downloads/notebook

    # just shrink / attach whatever is already in the entry's scan folder
    python tools/prep_scans.py journal/2026/10/2026-10-03_neha_optics.md
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

try:  # optional: iPhone HEIC support
    import pillow_heif
    pillow_heif.register_heif_opener()
    HEIC = True
except ImportError:
    HEIC = False

from common import ENTRY_RE, IMG_RE, ROOT, SCAN_EXT, scan_folder

IN_EXT = {".jpg", ".jpeg", ".png", ".webp"} | ({".heic", ".heif"} if HEIC else set())


def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", p.name)]


def shrink(src, dst, max_side, quality):
    with Image.open(src) as im0:
        im = ImageOps.exif_transpose(im0).convert("RGB")
    im.thumbnail((max_side, max_side), Image.LANCZOS)
    im.save(dst, "JPEG", quality=quality, optimize=True)


def md_ref(folder, f):
    if f.suffix.lower() == ".pdf":
        return f"[{f.name}]({folder.name}/{f.name})"
    return f"![{f.stem}]({folder.name}/{f.name})"


def attach(entry, folder, files):
    text = entry.read_text(encoding="utf-8")
    todo = [f for f in files if f"{folder.name}/{f.name}" not in text]
    if not todo:
        return 0
    lines = text.split("\n")
    idx = next((i for i, l in enumerate(lines) if l.strip().lower().startswith("## handwritten notes")), None)
    if idx is None:
        lines += ["", "## Handwritten notes", ""]
        idx = len(lines) - 3
    end = next((i for i in range(idx + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    refs = [i for i in range(idx + 1, end) if IMG_RE.search(lines[i]) or re.match(r"\[.*\]\(.*\.pdf\)", lines[i])]
    pos = (refs[-1] + 1) if refs else idx + 1
    block = [""]
    for f in todo:
        block += [md_ref(folder, f), ""]
    lines[pos:pos] = block
    entry.write_text("\n".join(lines), encoding="utf-8")
    return len(todo)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entry", help="the journal entry .md file")
    ap.add_argument("--from", dest="src", help="folder with photos/scans to import")
    ap.add_argument("--max", type=int, default=1600, help="longest side in px (default 1600)")
    ap.add_argument("--quality", type=int, default=80, help="JPEG quality (default 80)")
    a = ap.parse_args()

    entry = Path(a.entry).resolve()
    if not ENTRY_RE.match(entry.name) or not entry.exists():
        sys.exit("give the path to an existing journal entry (journal/YYYY/MM/YYYY-MM-DD_author_slug.md)")
    folder = scan_folder(entry)
    folder.mkdir(exist_ok=True)

    if a.src:
        src = Path(a.src).expanduser()
        files = sorted((p for p in src.iterdir() if p.suffix.lower() in IN_EXT), key=natural)
        if not files:
            sys.exit(f"no images found in {src}" + ("" if HEIC else " (for .heic photos: pip install pillow-heif)"))
        used = [int(m.group(1)) for f in folder.iterdir() if (m := re.fullmatch(r"p(\d+)\.jpg", f.name))]
        n = max(used, default=0)
        for f in files:
            n += 1
            shrink(f, folder / f"p{n}.jpg", a.max, a.quality)
        print(f"imported {len(files)} page(s) into {folder.relative_to(ROOT)}")
    else:
        for f in sorted(folder.iterdir()):
            if f.suffix.lower() in IN_EXT and (f.stat().st_size > 500_000 or max(Image.open(f).size) > a.max):
                dst = f if f.suffix.lower() in (".jpg", ".jpeg") else f.with_suffix(".jpg")
                shrink(f, dst, a.max, a.quality)
                if dst != f:
                    f.unlink()
                print(f"shrunk {dst.name}")

    scans = sorted((p for p in folder.iterdir() if p.suffix.lower() in SCAN_EXT), key=natural)
    added = attach(entry, folder, scans)
    print(f"attached {added} new image link(s) in {entry.relative_to(ROOT)}")
    print("reminder: copy any key numbers/equations from the pages into 'Results and numbers'.")


if __name__ == "__main__":
    main()
