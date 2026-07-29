#!/usr/bin/env python
"""Validate the Four Paths course structure.

Enforces the contract established by the 2026-07-22 renumbering
(``devguide/pending_proposals/course_module_renumbering_scheme.md`` and
``devguide/archive/resolved_bugs/course_module_numbering_overlaps.md``):

- the Common Core is exactly modules 1..20 (no gaps, no duplicates);
- each Path is exactly modules 21..54 (no gaps, no duplicates);
- every ``index.md`` toctree entry resolves to an existing notebook, and no on-disk
  notebook is missing from its section toctree;
- ``course_manifest.yml`` lists every notebook with a unique semantic id, and each
  notebook declares a matching MyST label ``(id)=`` before its top heading;
- ``.ipynb_checkpoints`` are excluded everywhere.

Exit code 0 on success, 1 on any violation. Imports nothing from MolSysMT.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
COURSE = REPO / "docs" / "content" / "course"
SECTIONS = {
    "00_Common_Core": ("core", range(1, 21)),
    "01_Path_Alzheimer": ("alzheimer", range(21, 55)),
    "02_Path_Enzyme": ("enzyme", range(21, 55)),
    "03_Path_Antiviral": ("antiviral", range(21, 55)),
    "04_Path_Biophysics": ("biophysics", range(21, 55)),
}


def notebooks(d: Path):
    return [p for p in d.glob("*.ipynb") if ".ipynb_checkpoints" not in p.parts]


def num_of(p: Path) -> int:
    return int(re.match(r"(\d+)_", p.name).group(1))


def label_of(nb_path: Path):
    nb = json.loads(nb_path.read_text())
    for cell in nb["cells"]:
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]
            m = re.search(r"\(([a-z0-9-]+)\)=", src)
            return m.group(1) if m else None
    return None


def load_manifest(errors):
    path = COURSE / "course_manifest.yml"
    if not path.exists():
        errors.append(f"missing manifest: {path}")
        return {}
    man = {}
    cur = None
    for line in path.read_text().splitlines():
        m = re.match(r"- id: (.*)", line)
        if m:
            cur = m.group(1).strip()
        m = re.match(r"  path: (.*)", line)
        if m and cur:
            man[m.group(1).strip()] = cur
    return man


def toctree_entries(index_md: Path):
    if not index_md.exists():
        return None
    return set(re.findall(r"([0-9]{2}_[A-Za-z0-9_]+\.ipynb)", index_md.read_text()))


def main() -> int:
    errors: list[str] = []
    manifest = load_manifest(errors)
    seen_ids: dict[str, str] = {}

    for d, (section, expected) in SECTIONS.items():
        sec_dir = COURSE / d
        if not sec_dir.is_dir():
            errors.append(f"missing section directory: {d}")
            continue
        nbs = notebooks(sec_dir)
        nums = sorted(num_of(p) for p in nbs)

        # 1. exact numeric contract (no gaps, no duplicates)
        if nums != list(expected):
            errors.append(
                f"{d}: numbering {nums[:3]}..{nums[-3:]} != expected "
                f"{expected.start}..{expected.stop - 1} (gaps/dups/wrong range)"
            )

        # 2. toctree <-> disk agreement
        toc = toctree_entries(sec_dir / "index.md")
        disk = {p.name for p in nbs}
        if toc is None:
            errors.append(f"{d}: missing index.md")
        else:
            for missing in sorted(toc - disk):
                errors.append(f"{d}: toctree references nonexistent notebook {missing}")
            for orphan in sorted(disk - toc):
                errors.append(f"{d}: notebook {orphan} not listed in index.md toctree")

        # 3. manifest + label consistency
        for p in nbs:
            rel = f"{d}/{p.name}"
            mid = manifest.get(rel)
            if mid is None:
                errors.append(f"{rel}: not in course_manifest.yml")
                continue
            if mid in seen_ids:
                errors.append(f"duplicate manifest id {mid}: {seen_ids[mid]} and {rel}")
            seen_ids[mid] = rel
            lab = label_of(p)
            if lab is None:
                errors.append(f"{rel}: no MyST label declared")
            elif lab != mid:
                errors.append(f"{rel}: label ({lab}) != manifest id ({mid})")

    total = sum(len(notebooks(COURSE / d)) for d in SECTIONS)
    if errors:
        print("Course structure validation FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"Course structure valid: {total} notebooks "
          f"(20 core + 4x34 paths), toctrees, manifest, and labels consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
