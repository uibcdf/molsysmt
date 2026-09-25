#!/usr/bin/env python
"""Validate a clean installation of the coordinated Conda staging pair."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import pathlib
import re
import sys

_PDB_TEXT = (
    "ATOM      1  N   MET A   1      11.104  13.207   8.551  1.00 20.00           N\n"
    "ATOM      2  CA  MET A   1      12.560  13.329   8.276  1.00 20.00           C\n"
    "ATOM      3  C   MET A   1      13.189  11.956   8.001  1.00 20.00           C\n"
    "ATOM      4  O   MET A   1      12.589  10.935   8.353  1.00 20.00           O\n"
    "END\n"
)
_STAGING_CHANNEL_ROOT = "https://conda.anaconda.org/uibcdf/label/staging"
_CONDA_SUBDIRS = {
    "linux-64",
    "linux-aarch64",
    "osx-64",
    "osx-arm64",
    "win-64",
    "noarch",
}


def _require_staging_provenance(record: dict, distribution_name: str) -> None:
    """Reject a Conda record that did not come from the exact staging label."""

    channel = record.get("channel")
    url = record.get("url")
    filename = record.get("fn")
    digest = record.get("sha256")
    if not isinstance(channel, str) or not isinstance(url, str):
        raise RuntimeError(f"{distribution_name} Conda record lacks staging provenance")
    url_root = f"{_STAGING_CHANNEL_ROOT}/"
    url_parts = (
        url.removeprefix(url_root).split("/") if url.startswith(url_root) else []
    )
    if (
        len(url_parts) != 2
        or url_parts[0] not in _CONDA_SUBDIRS
        or not isinstance(filename, str)
        or url_parts[1] != filename
        or not isinstance(digest, str)
        or re.fullmatch(r"[0-9a-f]{64}", digest) is None
    ):
        raise RuntimeError(
            f"{distribution_name} Conda record has incomplete staging artifact identity"
        )
    subdir = url_parts[0]
    allowed_channels = {
        _STAGING_CHANNEL_ROOT,
        f"{_STAGING_CHANNEL_ROOT}/{subdir}",
        "uibcdf/label/staging",
        f"uibcdf/label/staging/{subdir}",
    }
    if channel not in allowed_channels:
        raise RuntimeError(
            f"{distribution_name} came from a non-staging channel: {channel}"
        )


def _require_conda_install(
    distribution_name: str,
    expected_version: str,
    *,
    require_abi3: bool = False,
    require_staging_provenance: bool = False,
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
    record = json.loads(conda_records[0].read_text(encoding="utf-8"))
    if require_staging_provenance:
        _require_staging_provenance(record, distribution_name)
    if require_abi3:
        build = str(record.get("build", ""))
        if not build.startswith("pyabi3h"):
            raise RuntimeError(f"MolSysMT resolved non-ABI3 Conda build {build!r}")
        requirements = record.get("depends", [])
        requirement_names = {
            requirement.split()[0]
            for requirement in requirements
            if isinstance(requirement, str) and requirement.split()
        }
        missing = {
            "python",
            "cpython",
            "_python_abi3_support",
            "py-mmcif",
        } - requirement_names
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


def _require_bundled_bcif_conversion(molsysmt) -> None:
    """Exercise the packaged py-mmcif runtime without network access."""

    source = molsysmt.systems["chicken villin HP35"]["1vii.bcif.gz"]
    try:
        item = molsysmt.convert(source, to_form="molsysmt.MolSys")
    except Exception as exception:
        raise RuntimeError("Bundled BCIF conversion failed") from exception

    if item.topology.n_atoms != 596:
        raise RuntimeError(
            "Bundled BCIF conversion returned "
            f"{item.topology.n_atoms} atoms, expected 596"
        )


def _require_pdb_text_viewer_load(molsysmt, molsysviewer) -> None:
    """Exercise PDB-text discovery and Viewer loading without a file path."""

    try:
        form = molsysmt.get_form(_PDB_TEXT)
        if form != "string:pdb_text":
            raise RuntimeError(f"PDB text was classified as {form!r}")

        item = molsysmt.convert(_PDB_TEXT, to_form="molsysmt.MolSys")
        if item.topology.n_atoms != 4:
            raise RuntimeError(
                f"PDB-text conversion returned {item.topology.n_atoms} atoms, expected 4"
            )

        view = molsysviewer.MolSysView(debug_js=True)
        try:
            view.load(_PDB_TEXT)
            loaded = getattr(view, "_molsys", None)
            if loaded is None:
                raise RuntimeError("Viewer did not retain the loaded molecular system")
            n_atoms = molsysmt.get(loaded, element="atom", n_atoms=True)
            if n_atoms != 4:
                raise RuntimeError(f"Viewer retained {n_atoms} atoms, expected 4")
        finally:
            view.close()
    except Exception as exception:
        raise RuntimeError("PDB-text Viewer integration failed") from exception


def validate(
    molsysmt_version: str,
    molsysviewer_version: str,
    *,
    require_staging_provenance: bool = False,
) -> None:
    """Validate the installed package pair and its native/runtime resources."""

    _require_conda_install(
        "molsysmt",
        molsysmt_version,
        require_abi3=True,
        require_staging_provenance=require_staging_provenance,
    )
    _require_conda_install(
        "molsysviewer",
        molsysviewer_version,
        require_staging_provenance=require_staging_provenance,
    )

    _require_version("molsysmt", molsysmt_version)
    _require_version("molsysviewer", molsysviewer_version)

    import molsysmt._rust as rust
    import molsysviewer

    import molsysmt

    importlib.import_module("molsysviewer.runtime_contract")

    if molsysmt.__version__ != molsysmt_version:
        raise RuntimeError(
            f"molsysmt.__version__ is {molsysmt.__version__}, expected {molsysmt_version}"
        )

    _require_bundled_bcif_conversion(molsysmt)
    _require_pdb_text_viewer_load(molsysmt, molsysviewer)

    prefix = pathlib.Path(sys.prefix).resolve()
    rust_path = pathlib.Path(rust.__file__).resolve()
    if prefix not in rust_path.parents:
        raise RuntimeError(
            f"molsysmt._rust resolves outside the environment: {rust_path}"
        )

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
    parser.add_argument("--require-staging-provenance", action="store_true")
    args = parser.parse_args()
    validate(
        args.molsysmt_version,
        args.molsysviewer_version,
        require_staging_provenance=args.require_staging_provenance,
    )


if __name__ == "__main__":
    main()
