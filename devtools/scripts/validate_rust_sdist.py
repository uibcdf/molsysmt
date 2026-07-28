#!/usr/bin/env python
"""Validating the Rust-bearing MolSysMT source distribution."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
import tarfile


REQUIRED_SUFFIXES = {
    "LICENSE",
    "MANIFEST.in",
    "pyproject.toml",
    "rust-toolchain.toml",
    "rust/Cargo.toml",
    "rust/Cargo.lock",
    "rust/src/lib.rs",
    "molsysmt/__init__.py",
    "molsysmt/py.typed",
    "molsysmt/data/demo_manifest.json",
    "molsysviewer_molsysmt/__init__.py",
}
FORBIDDEN_SUFFIXES = {
    ".pyc",
    ".pyo",
    ".so",
    ".pyd",
    ".dylib",
    ".nbi",
    ".nbc",
}
FORBIDDEN_PARTS = {
    "__pycache__",
    ".pytest_cache",
    "target",
    ".git",
}
ALLOWED_ROOT_ENTRIES = {
    "CODE_OF_CONDUCT.md",
    "LICENSE",
    "MANIFEST.in",
    "PKG-INFO",
    "README.md",
    "molsysmt",
    "molsysmt.egg-info",
    "molsysviewer_molsysmt",
    "pyproject.toml",
    "rust",
    "rust-toolchain.toml",
    "setup.cfg",
}


def find_single_sdist(path: Path) -> Path:
    """Returning the single gzip-compressed source archive at a path."""

    path = path.resolve()
    archives = sorted(path.glob("*.tar.gz")) if path.is_dir() else [path]
    if len(archives) != 1 or not archives[0].is_file():
        raise RuntimeError(
            f"expected exactly one .tar.gz sdist at {path}, found {len(archives)}"
        )
    return archives[0]


def validate_sdist(path: Path) -> list[str]:
    """Returning all source-distribution contract violations."""

    problems = []
    with tarfile.open(path, mode="r:gz") as archive:
        members = [PurePosixPath(member.name) for member in archive.getmembers()]

    if not members:
        return ["source distribution is empty"]

    roots = {member.parts[0] for member in members if member.parts}
    if len(roots) != 1:
        problems.append(f"expected one archive root, found {sorted(roots)}")
        root = ""
    else:
        root = next(iter(roots))

    relative = {
        member.relative_to(root).as_posix()
        for member in members
        if root and member.parts and member.parts[0] == root and len(member.parts) > 1
    }
    missing = sorted(REQUIRED_SUFFIXES - relative)
    if missing:
        problems.append(f"required source files are missing: {missing}")

    unexpected_roots = sorted(
        {
            PurePosixPath(name).parts[0]
            for name in relative
            if PurePosixPath(name).parts
            and PurePosixPath(name).parts[0] not in ALLOWED_ROOT_ENTRIES
        }
    )
    if unexpected_roots:
        problems.append(
            f"source distribution contains unexpected top-level entries: "
            f"{unexpected_roots}"
        )

    forbidden = sorted(
        member.as_posix()
        for member in members
        if member.suffix in FORBIDDEN_SUFFIXES
        or FORBIDDEN_PARTS.intersection(member.parts)
    )
    if forbidden:
        preview = forbidden[:10]
        problems.append(
            f"cache, build, VCS, or binary artifacts are present: {preview}"
            + (f" (+{len(forbidden) - len(preview)} more)" if len(forbidden) > 10 else "")
        )

    rust_sources = {
        name for name in relative if name.startswith("rust/src/") and name.endswith(".rs")
    }
    if not rust_sources:
        problems.append("no Rust source files are present")

    return problems


def main() -> int:
    """Validating one source archive and printing a compact verdict."""

    parser = argparse.ArgumentParser()
    parser.add_argument("sdist_or_directory", type=Path)
    arguments = parser.parse_args()

    sdist = find_single_sdist(arguments.sdist_or_directory)
    problems = validate_sdist(sdist)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        return 1

    size_mb = sdist.stat().st_size / 1024.0**2
    print(
        "MolSysMT Rust sdist validation passed: "
        f"{sdist.name} | compressed_size={size_mb:.2f} MiB"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
