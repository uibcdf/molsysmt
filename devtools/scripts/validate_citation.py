#!/usr/bin/env python3
"""Validate release citation metadata and its derived public surfaces."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
CONCEPT_DOI = "10.5281/zenodo.1298752"
REPOSITORY_URL = "https://github.com/uibcdf/molsysmt"
PROJECT_TITLE = "MolSysMT"
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")

PUBLIC_SURFACES = (
    "README.md",
    "docs/index.ipynb",
    "docs/content/about/citation.md",
    "docs/_bibtex/software.bib",
    "docs/index.AGENTS.md",
)
HISTORICAL_DOIS = (
    "10.5281/zenodo.2530946",  # MolModMT, not MolSysMT
    "10.5281/zenodo.8092688",  # MolSysMT 0.8.1 version DOI
    "10.5281/8092688",  # malformed historical spelling
)


def _orcid(value: object) -> str:
    return str(value or "").removeprefix("https://orcid.org/")


def _cff_creators(payload: dict) -> set[tuple[str, str]]:
    return {
        (
            f"{author.get('family-names', '')}, {author.get('given-names', '')}",
            _orcid(author.get("orcid")),
        )
        for author in payload.get("authors", [])
    }


def _zenodo_creators(payload: dict) -> set[tuple[str, str]]:
    return {
        (str(creator.get("name", "")), _orcid(creator.get("orcid")))
        for creator in payload.get("creators", [])
    }


def validate_repository(repo: Path = REPO, expected_version: str | None = None) -> list[str]:
    """Return every citation-policy violation found below *repo*."""

    errors: list[str] = []
    cff_path = repo / "CITATION.cff"
    zenodo_path = repo / ".zenodo.json"

    try:
        cff = yaml.safe_load(cff_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"CITATION.cff cannot be parsed: {exc}"]
    try:
        zenodo = json.loads(zenodo_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f".zenodo.json cannot be parsed: {exc}"]

    version = str(cff.get("version", ""))
    released = cff.get("date-released")
    released_text = released.isoformat() if isinstance(released, date) else str(released)

    if cff.get("title") != PROJECT_TITLE:
        errors.append(f"CITATION.cff title must be {PROJECT_TITLE!r}")
    if cff.get("type") != "software":
        errors.append("CITATION.cff type must be 'software'")
    if not VERSION_RE.fullmatch(version):
        errors.append("CITATION.cff version must use X.Y.Z")
    if expected_version is not None and version != expected_version:
        errors.append(
            f"CITATION.cff version {version!r} does not match expected {expected_version!r}"
        )
    try:
        date.fromisoformat(released_text)
    except ValueError:
        errors.append("CITATION.cff date-released must use YYYY-MM-DD")
    if cff.get("doi") != CONCEPT_DOI:
        errors.append(f"CITATION.cff must use the concept DOI {CONCEPT_DOI}")
    if str(cff.get("url", "")).rstrip("/").lower() != REPOSITORY_URL.lower():
        errors.append(f"CITATION.cff url must be {REPOSITORY_URL}")
    if str(cff.get("license", "")).lower() != "mit":
        errors.append("CITATION.cff license must be MIT")

    if zenodo.get("title") != PROJECT_TITLE:
        errors.append(f".zenodo.json title must be {PROJECT_TITLE!r}")
    if zenodo.get("upload_type") != "software":
        errors.append(".zenodo.json upload_type must be 'software'")
    if str(zenodo.get("license", "")).lower() != "mit":
        errors.append(".zenodo.json license must be the string 'mit'")
    if "version" in zenodo or "publication_date" in zenodo:
        errors.append(
            ".zenodo.json must leave version and publication_date to the GitHub Release"
        )
    if _cff_creators(cff) != _zenodo_creators(zenodo):
        errors.append("CITATION.cff and .zenodo.json creators/ORCIDs disagree")

    for relative in PUBLIC_SURFACES:
        path = repo / relative
        if not path.is_file():
            errors.append(f"missing citation surface: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        if CONCEPT_DOI not in text:
            errors.append(f"{relative} does not name the concept DOI {CONCEPT_DOI}")
        for forbidden in HISTORICAL_DOIS:
            if forbidden in text:
                errors.append(f"{relative} freezes historical or invalid DOI {forbidden}")

    index_text = (repo / "docs/index.ipynb").read_text(encoding="utf-8")
    citation_text = (repo / "docs/content/about/citation.md").read_text(encoding="utf-8")
    bibtex_text = (repo / "docs/_bibtex/software.bib").read_text(encoding="utf-8")
    if f"release-v{version}-white.svg" not in index_text:
        errors.append("docs/index.ipynb release badge does not match CITATION.cff")
    for relative, text in (
        ("docs/index.ipynb", index_text),
        ("docs/content/about/citation.md", citation_text),
    ):
        if not re.search(rf"Version\s+(?:\\n)?{re.escape(version)}", text):
            errors.append(f"{relative} software citation does not match version {version}")
        if f"({released_text[:4]})" not in text:
            errors.append(f"{relative} software citation does not match release year")
    if not re.search(rf"^version = \{{{re.escape(version)}\}},$", bibtex_text, re.MULTILINE):
        errors.append("docs/_bibtex/software.bib version does not match CITATION.cff")
    if not re.search(rf"^year = \{{{re.escape(released_text[:4])}\}}$", bibtex_text, re.MULTILINE):
        errors.append("docs/_bibtex/software.bib year does not match CITATION.cff")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=REPO)
    parser.add_argument("--expected-version")
    args = parser.parse_args()

    errors = validate_repository(args.repo_root.resolve(), args.expected_version)
    if errors:
        print("Citation metadata: FAIL")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("Citation metadata: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
