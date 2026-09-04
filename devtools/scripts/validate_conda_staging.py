#!/usr/bin/env python
"""Validate a clean installation of the coordinated Conda staging pair."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import pathlib
import sys


def _require_conda_install(
    distribution_name: str,
    expected_version: str,
    *,
    require_abi3: bool = False,
) -> None:
    distribution = importlib.metadata.distribution(distribution_name)
    direct_url = distribution.read_text("direct_url.json")
    if direct_url is not None:
        direct_url_data = json.loads(direct_url)
        if direct_url_data.get("dir_info", {}).get("editable", False):
            raise RuntimeError(f"{distribution_name} is an editable installation")

    root = pathlib.Path(distribution.locate_file("")).resolve()
    prefix = pathlib.Path(sys.prefix).resolve()
    if root != prefix and prefix not in root.parents:
        raise RuntimeError(
            f"{distribution_name} resolves outside the active environment: {root}"
        )

    conda_records = list(
        (prefix / "conda-meta").glob(
            f"{distribution_name.lower()}-{expected_version}-*.json"
        )
    )
    if len(conda_records) != 1:
        raise RuntimeError(
            f"Expected one Conda record for {distribution_name} {expected_version}, "
            f"found {len(conda_records)}"
        )
    if require_abi3:
        record = json.loads(conda_records[0].read_text(encoding="utf-8"))
        build = str(record.get("build", ""))
        if not build.startswith("pyabi3h"):
            raise RuntimeError(
                f"MolSysMT resolved non-ABI3 Conda build {build!r}"
            )
        requirements = record.get("depends", [])
        requirement_names = {
            requirement.split()[0]
            for requirement in requirements
            if isinstance(requirement, str) and requirement.split()
        }
        missing = {"python", "cpython", "_python_abi3_support"} - requirement_names
        if missing:
            raise RuntimeError(
                "MolSysMT ABI3 Conda record is missing runtime requirements: "
                f"{sorted(missing)}"
            )
        if "python_abi" in requirement_names:
            raise RuntimeError(
                "MolSysMT ABI3 Conda record retains an exact python_abi requirement"
            )


def _require_version(distribution_name: str, expected: str) -> None:
    observed = importlib.metadata.version(distribution_name)
    if observed != expected:
        raise RuntimeError(
            f"{distribution_name} version is {observed}, expected {expected}"
        )


def validate(molsysmt_version: str, molsysviewer_version: str) -> None:
    """Validate the installed package pair and its native/runtime resources."""

    _require_conda_install("molsysmt", molsysmt_version, require_abi3=True)
    _require_conda_install("molsysviewer", molsysviewer_version)

    _require_version("molsysmt", molsysmt_version)
    _require_version("molsysviewer", molsysviewer_version)

    import molsysmt
    import molsysmt._rust as rust
    import molsysviewer
    importlib.import_module("molsysviewer.runtime_contract")

    if molsysmt.__version__ != molsysmt_version:
        raise RuntimeError(
            f"molsysmt.__version__ is {molsysmt.__version__}, expected {molsysmt_version}"
        )

    prefix = pathlib.Path(sys.prefix).resolve()
    rust_path = pathlib.Path(rust.__file__).resolve()
    if prefix not in rust_path.parents:
        raise RuntimeError(f"molsysmt._rust resolves outside the environment: {rust_path}")

    viewer_root = pathlib.Path(molsysviewer.__file__).resolve().parent
    for resource_name in ("runtime_actions.json", "viewer.js"):
        resource = viewer_root / resource_name
        if not resource.is_file():
            raise RuntimeError(f"MolSysViewer runtime resource is missing: {resource}")


def main() -> None:
    """Parse candidate versions and validate the active Conda environment."""

    parser = argparse.ArgumentParser()
    parser.add_argument("--molsysmt-version", required=True)
    parser.add_argument("--molsysviewer-version", required=True)
    args = parser.parse_args()
    validate(args.molsysmt_version, args.molsysviewer_version)


if __name__ == "__main__":
    main()
