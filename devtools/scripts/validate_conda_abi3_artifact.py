#!/usr/bin/env python
"""Validating MolSysMT's platform-specific Conda ABI3 artifact."""

from __future__ import annotations

import argparse
import json
import tempfile
from pathlib import Path


def _requirement_names(requirements: list[str]) -> set[str]:
    """Returning package names from rendered Conda requirements."""

    return {requirement.split()[0] for requirement in requirements}


def validate_extracted_artifact(root: Path, expected_subdir: str) -> list[str]:
    """Returning ABI3 contract violations from an extracted Conda package."""

    problems: list[str] = []
    index_path = root / "info" / "index.json"
    if not index_path.is_file():
        return ["package is missing info/index.json"]

    index = json.loads(index_path.read_text(encoding="utf-8"))
    if index.get("subdir") != expected_subdir:
        problems.append(
            f"package subdir is {index.get('subdir')!r}, expected {expected_subdir!r}"
        )
    if index.get("noarch") != "python":
        problems.append(
            "platform ABI3 package does not declare noarch: python relocation metadata"
        )
    if not str(index.get("build", "")).startswith("pyabi3h"):
        problems.append("package build string does not identify the ABI3 artifact")

    requirements = index.get("depends", [])
    if not isinstance(requirements, list) or not all(
        isinstance(requirement, str) for requirement in requirements
    ):
        problems.append("package dependencies are not a list of strings")
        requirements = []
    names = _requirement_names(requirements)
    for required in ("python", "cpython", "_python_abi3_support"):
        if required not in names:
            problems.append(f"package is missing the {required} ABI3 runtime requirement")
    if "python_abi" in names:
        problems.append("package retains an exact python_abi runtime requirement")
    python_specs = [item for item in requirements if item.split()[0] == "python"]
    if len(python_specs) != 1 or not all(
        bound in python_specs[0].replace(" ", "")
        for bound in (">=3.11", "<3.14")
    ):
        problems.append(
            "package does not declare exactly one Python >=3.11,<3.14 requirement"
        )

    extensions = [
        path.relative_to(root).as_posix()
        for path in root.rglob("_rust.*")
        if path.is_file() and path.suffix in {".so", ".pyd", ".dylib"}
    ]
    abi3_extensions = [path for path in extensions if "/_rust.abi3." in path]
    if len(extensions) != 1 or len(abi3_extensions) != 1:
        problems.append(
            "expected exactly one molsysmt/_rust.abi3 native extension, "
            f"found {extensions}"
        )
    elif not abi3_extensions[0].startswith("site-packages/molsysmt/"):
        problems.append(
            "ABI3 extension is not stored under the relocatable site-packages path: "
            f"{abi3_extensions[0]}"
        )
    return problems


def validate_artifact(package: Path, expected_subdir: str) -> list[str]:
    """Extracting a Conda artifact and returning ABI3 contract violations."""

    from conda_package_handling.api import extract

    with tempfile.TemporaryDirectory(prefix="molsysmt-conda-abi3-") as directory:
        root = Path(directory)
        extract(str(package.resolve()), str(root))
        return validate_extracted_artifact(root, expected_subdir)


def main() -> int:
    """Running the Conda ABI3 artifact validator."""

    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--expected-subdir", required=True)
    args = parser.parse_args()

    problems = validate_artifact(args.package, args.expected_subdir)
    if problems:
        print("MolSysMT Conda ABI3 validation failed:")
        for problem in problems:
            print(f"- {problem}")
        return 1
    print(
        "MolSysMT Conda ABI3 validation passed: "
        f"{args.package} | subdir={args.expected_subdir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
