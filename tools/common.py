"""Shared helpers for the litho journal tools."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
JOURNAL = ROOT / "journal"
ENTRY_RE = re.compile(r"^(\d{4})-(\d{2})-(\d{2})_([a-z0-9-]+)_([a-z0-9-]+)\.md$")
FM_RE = re.compile(r"^---[ \t]*\n(.*?)\n---[ \t]*\n?(.*)$", re.S)
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
SCAN_EXT = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}
GENERATED_NAMES = {"README.md", "INDEX.md", "PROMOTE_QUEUE.md"}


def load_team():
    with open(ROOT / "team.yml", encoding="utf-8") as f:
        return yaml.safe_load(f)


def as_list(v):
    if v is None or v == "":
        return []
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v]
    return [str(v)]


def promote_value(meta):
    """YAML turns bare yes/no into booleans; normalise to 'yes'/'no'/'done'."""
    v = meta.get("promote_to_docs")
    if v is True:
        return "yes"
    if v is False:
        return "no"
    return str(v).strip().lower() if v is not None else ""


def parse_entry(path):
    """Return {'path','meta','body'} or raise ValueError with a readable message."""
    text = path.read_text(encoding="utf-8")
    m = FM_RE.match(text)
    if not m:
        raise ValueError("missing front matter (the --- block at the top of the file)")
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        raise ValueError(f"front matter is not valid YAML: {e}")
    if not isinstance(meta, dict):
        raise ValueError("front matter must be 'key: value' lines")
    return {"path": path, "meta": meta, "body": m.group(2)}


def scan_folder(entry_path):
    return entry_path.with_suffix("")


def scan_files(entry_path):
    folder = scan_folder(entry_path)
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in SCAN_EXT)


def iter_entry_paths():
    if not JOURNAL.is_dir():
        return []
    return sorted(p for p in JOURNAL.rglob("*.md") if ENTRY_RE.match(p.name))


def sections(body):
    """Map lowercase '## heading' -> content (HTML comments removed)."""
    out = {}
    for part in re.split(r"(?m)^## +", body)[1:]:
        head, _, content = part.partition("\n")
        content = re.sub(r"<!--.*?-->", "", content, flags=re.S).strip()
        out[head.strip().lower()] = content
    return out
