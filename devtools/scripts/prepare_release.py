#!/usr/bin/env python3
"""Update release-specific citation fields before creating a tag."""

from __future__ import annotations

import argparse
import calendar
import re
import sys
from datetime import date
from pathlib import Path

from validate_citation import VERSION_RE, validate_repository

REPO = Path(__file__).resolve().parents[2]


def _replace(path: Path, pattern: str, replacement: str, *, flags: int = 0) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, flags=flags)
    if count == 0:
        raise RuntimeError(f"release field not found in {path}")
    path.write_text(updated, encoding="utf-8")


def prepare_release(repo: Path, version: str, released: date) -> None:
    """Update the canonical and derived citation surfaces below *repo*."""

    if not VERSION_RE.fullmatch(version):
        raise ValueError("version must use X.Y.Z without a leading 'v'")

    cff = repo / "CITATION.cff"
    _replace(cff, r"^version: .+$", f"version: {version}", flags=re.MULTILINE)
    _replace(
        cff,
        r"^date-released: .+$",
        f"date-released: {released.isoformat()}",
        flags=re.MULTILINE,
    )

    index = repo / "docs/index.ipynb"
    _replace(index, r"release-v\d+\.\d+\.\d+-white\.svg", f"release-v{version}-white.svg")
    _replace(index, r"\(20\d{2}\)\. MolSysMT \(Version \d+\.\d+\.\d+\)",
             f"({released.year}). MolSysMT (Version {version})")

    citation = repo / "docs/content/about/citation.md"
    _replace(citation, r"\(20\d{2}\)\. MolSysMT \(Version\s*\n?\d+\.\d+\.\d+\)",
             f"({released.year}). MolSysMT (Version\n{version})")

    bibtex = repo / "docs/_bibtex/software.bib"
    key_version = version.replace(".", "_")
    _replace(bibtex, r"^@software\{[^,]+,", f"@software{{Prada-Gracia_MolSysMT_{key_version}_{released.year},",
             flags=re.MULTILINE)
    _replace(bibtex, r"^month = \w+,$", f"month = {calendar.month_abbr[released.month].lower()},",
             flags=re.MULTILINE)
    _replace(bibtex, r"^version = \{[^}]+\},$", f"version = {{{version}}},", flags=re.MULTILINE)
    _replace(bibtex, r"^year = \{\d{4}\}$", f"year = {{{released.year}}}", flags=re.MULTILINE)

    errors = validate_repository(repo, expected_version=version)
    if errors:
        raise RuntimeError("prepared citation did not validate:\n  - " + "\n  - ".join(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version")
    parser.add_argument("--date", default=date.today().isoformat(), dest="released")
    parser.add_argument("--repo-root", type=Path, default=REPO)
    args = parser.parse_args()
    try:
        released = date.fromisoformat(args.released)
        prepare_release(args.repo_root.resolve(), args.version, released)
    except (ValueError, RuntimeError) as exc:
        print(f"Release citation preparation: FAIL\n  {exc}")
        return 1
    print(
        f"Release citation preparation: PASS — {args.version} ({released.isoformat()})"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
