#!/usr/bin/env python
"""Validate stored notebook schemas without executing or repairing notebooks.

With no paths, inspect docs/content and docs/index.ipynb. Explicit files or
directories support small reproductions. Generated builds and editor checkpoints
are excluded. Missing inputs, unknown declared schemas and provider failures
reject the check; a successful Sphinx process cannot override its result.
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

import nbformat

REPO = Path(__file__).resolve().parents[2]
DEFAULT_INPUTS = (REPO / "docs" / "content", REPO / "docs" / "index.ipynb")
EXCLUDED_PARTS = frozenset({"_build", ".ipynb_checkpoints"})


def _reject_nonfinite_constant(value: str) -> None:
    raise ValueError("Non-finite constants are not JSON numbers.")


def validate_notebook(path: Path) -> list[str]:
    """Return bounded, content-free schema diagnostics for one stored source."""
    try:
        before = path.read_bytes()
        notebook = json.loads(before, parse_constant=_reject_nonfinite_constant)
    except (OSError, ValueError, UnicodeError) as error:
        return [f"Cannot read notebook JSON ({type(error).__name__})."]
    if not isinstance(notebook, dict):
        return ["Notebook JSON must be an object."]
    major, minor = notebook.get("nbformat"), notebook.get("nbformat_minor")
    if type(major) is not int or type(minor) is not int or minor < 0:
        return ["Declare integer nbformat and nonnegative nbformat_minor."]
    schema = nbformat.versions.get(major)
    if schema is None or minor > schema.nbformat_minor:
        return [f"Unsupported declared notebook schema {major}.{minor}."]

    original = copy.deepcopy(notebook)
    errors = []
    try:
        for error in nbformat.validator.iter_validate(
            notebook, version=major, version_minor=minor, relax_add_props=False
        ):
            # Exception messages can contain entire cells or embedded outputs.
            errors.append(
                f"Schema rejection at {json.dumps(list(error.absolute_path))}: "
                f"{error.validator}."
            )
            if len(errors) == 8:
                errors.append("Further schema diagnostics omitted.")
                break
    except Exception as error:
        errors.append(f"Notebook validation provider failed ({type(error).__name__}).")
    if notebook != original:
        errors.append("Notebook validation changed the in-memory source.")
    if not errors and major == 4 and minor >= 5:
        identifiers = [cell["id"] for cell in notebook["cells"]]
        if len(identifiers) != len(set(identifiers)):
            errors.append("Notebook cell identifiers must be unique.")
    try:
        if path.read_bytes() != before:
            errors.append("Notebook bytes changed during validation.")
    except OSError:
        errors.append("Notebook source disappeared during validation.")
    return errors


def collect_notebooks(inputs: list[Path]) -> tuple[list[Path], list[str]]:
    """Discover source files without silently accepting missing or empty inputs."""
    paths = set()
    errors = []
    for source in inputs:
        if source.is_file() and source.suffix == ".ipynb":
            candidates = [source]
        elif source.is_dir():
            candidates = list(source.rglob("*.ipynb"))
        else:
            errors.append(f"Missing or unsupported notebook input: {source}")
            continue
        for path in candidates:
            if not EXCLUDED_PARTS.intersection(path.parts):
                paths.add(path.resolve())
    if not paths:
        errors.append("No notebook sources were found.")
    return sorted(paths), errors


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    options = parser.parse_args(arguments)
    paths, errors = collect_notebooks(options.paths or list(DEFAULT_INPUTS))
    for path in paths:
        errors.extend(f"{path}: {message}" for message in validate_notebook(path))
    if errors:
        print("Notebook schema validation failed:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1
    print(f"Notebook schemas valid: {len(paths)} stored sources; no repairs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
