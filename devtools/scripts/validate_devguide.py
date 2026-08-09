#!/usr/bin/env python3
"""Checking structural integrity of the MolSysMT developer guide."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

try:  # imported as devtools.scripts.validate_devguide by the tests
    from devtools.scripts import devguide_index, devguide_reports
except ImportError:  # run as a script, with devtools/scripts on the path
    import devguide_index
    import devguide_reports


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DEVGUIDE_ROOT = REPOSITORY_ROOT / "devguide"

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
RETIRED_NAMES = {
    "architecture.md": "CORE_SPECIFICATION.md",
    "auxiliary_data_and_nativization.md": "BUILD_ECOSYSTEM.md",
    "element_and_native_rebuild.md": "CORE_SPECIFICATION.md",
    "molsys_builder.md": "BUILDER_API.md",
    "scalability_and_heavy_trajectories_v2.md": "SCALABILITY.md",
}


def _active_documents() -> list[Path]:
    documents = []
    for suffix in ("*.md", "*.ipynb"):
        documents.extend(DEVGUIDE_ROOT.rglob(suffix))
    return sorted(path for path in documents if "archive" not in path.parts)


def _link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(maxsplit=1)[0]
    return unquote(target.split("#", maxsplit=1)[0])


def validate() -> list[str]:
    errors: list[str] = []

    for document in _active_documents():
        text = document.read_text(encoding="utf-8")
        relative = document.relative_to(REPOSITORY_ROOT)

        if "file://" in text:
            errors.append(f"{relative}: contains a machine-specific file:// link")
        if str(REPOSITORY_ROOT) in text:
            errors.append(f"{relative}: contains an absolute repository path")

        for retired, replacement in RETIRED_NAMES.items():
            if retired in text:
                errors.append(
                    f"{relative}: references retired {retired!r}; use {replacement!r}"
                )

        if document.suffix != ".md":
            continue

        for match in MARKDOWN_LINK.finditer(text):
            target = _link_target(match.group(1))
            if not target or target.startswith(
                ("#", "http://", "https://", "mailto:", "data:")
            ):
                continue
            resolved = (document.parent / target).resolve()
            try:
                resolved.relative_to(REPOSITORY_ROOT)
            except ValueError:
                errors.append(f"{relative}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                errors.append(f"{relative}: broken local link: {target}")

    errors.extend(devguide_reports.validate_all())
    errors.extend(_stale_indexes())

    return errors


def _stale_indexes() -> list[str]:
    """The generated queue indexes must agree with the front matter they render."""

    stale, errors = devguide_index.process(check=True)
    return errors + [
        f"{path}: generated index is stale; run "
        f"python devtools/scripts/devguide_index.py"
        for path in stale
    ]


def main() -> int:
    errors = validate()
    if errors:
        print("Developer-guide validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Developer-guide validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
