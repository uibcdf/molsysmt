#!/usr/bin/env python
"""Validating the private Rust extension contract of a MolSysMT wheel."""

from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
from zipfile import ZipFile


def validate_wheel(wheel_path: Path) -> list[str]:
    """Returning contract violations found inside a MolSysMT wheel."""

    problems: list[str] = []
    with ZipFile(wheel_path) as archive:
        names = archive.namelist()

        extensions = [
            name
            for name in names
            if PurePosixPath(name).parent == PurePosixPath("molsysmt")
            and PurePosixPath(name).name.startswith("_rust.")
            and PurePosixPath(name).suffix in {".so", ".pyd", ".dylib"}
        ]
        if len(extensions) != 1:
            problems.append(
                "expected exactly one private molsysmt/_rust extension, "
                f"found {len(extensions)}: {extensions}"
            )

        legacy_names = [name for name in names if "msm_rust_kernels" in name]
        if legacy_names:
            problems.append(
                "legacy msm_rust_kernels package entries remain: "
                f"{legacy_names}"
            )

        bytecode = [
            name
            for name in names
            if "__pycache__" in PurePosixPath(name).parts or name.endswith(".pyc")
        ]
        if bytecode:
            problems.append(
                f"wheel contains {len(bytecode)} bytecode/cache entries"
            )

        for required in (
            "molsysmt/py.typed",
            "molsysmt/data/demo_manifest.json",
        ):
            if required not in names:
                problems.append(f"required wheel entry is missing: {required}")

        wheel_metadata = [
            name for name in names if name.endswith(".dist-info/WHEEL")
        ]
        if len(wheel_metadata) != 1:
            problems.append(
                "expected exactly one .dist-info/WHEEL file, "
                f"found {len(wheel_metadata)}"
            )
        else:
            content = archive.read(wheel_metadata[0]).decode("utf-8")
            if "Root-Is-Purelib: false" not in content:
                problems.append("wheel is not marked as a platform wheel")
            if not any(
                line.startswith("Tag: cp311-abi3-")
                for line in content.splitlines()
            ):
                problems.append("wheel does not declare a cp311-abi3 tag")

        entry_points = [
            name for name in names if name.endswith(".dist-info/entry_points.txt")
        ]
        if len(entry_points) != 1:
            problems.append(
                "expected exactly one entry_points.txt file, "
                f"found {len(entry_points)}"
            )
        else:
            content = archive.read(entry_points[0]).decode("utf-8")
            if "[molsysviewer.addons]" not in content:
                problems.append("molsysviewer.addons entry-point group is missing")
            if "molsysmt = molsysviewer_molsysmt" not in content:
                problems.append("MolSysViewer's MolSysMT entry point is missing")

    return problems


def main() -> int:
    """Running the wheel validator from the command line."""

    parser = argparse.ArgumentParser()
    parser.add_argument("wheel", type=Path)
    args = parser.parse_args()

    problems = validate_wheel(args.wheel)
    if problems:
        print("MolSysMT Rust wheel validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1

    print(f"MolSysMT Rust wheel validation passed: {args.wheel}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
