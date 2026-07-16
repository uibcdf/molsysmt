"""Migrating the bundled H5MSM demos from version 0.3 to version 0.4."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

import h5py
import numpy as np

import molsysmt as msm


DATA_DIR = Path(__file__).resolve().parents[1]
MANIFEST = DATA_DIR / "demo_manifest.json"
H5MSM_DIR = DATA_DIR / "h5msm"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _snapshot(path: Path) -> dict[str, np.ndarray]:
    names = [
        "topology/atoms/atom_id",
        "topology/atoms/atom_name",
        "topology/groups/group_id",
        "topology/components/component_id",
        "topology/molecules/molecule_id",
        "topology/entities/entity_id",
        "topology/chains/chain_id",
        "topology/bonds/atom1_index",
        "topology/bonds/atom2_index",
        "structures/coordinates",
        "structures/box",
        "structures/time",
    ]
    with h5py.File(path, "r") as file:
        return {name: file[name][:] for name in names}


def _assert_equivalent(before: dict[str, np.ndarray], path: Path) -> None:
    with h5py.File(path, "r") as file:
        if str(file.attrs["version"]) != "0.4":
            raise RuntimeError(f"{path.name} was not written as H5MSM 0.4")
        for name, expected in before.items():
            observed = file[name][:]
            if name.endswith("_id"):
                expected = expected.astype(str)
                observed = observed.astype(str)
            np.testing.assert_equal(observed, expected)


def migrate() -> None:
    """Migrating every manifest-owned demo through the normalized native model."""

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for artifact in manifest["artifacts"]:
        path = H5MSM_DIR / artifact["file"]
        with h5py.File(path, "r") as file:
            version = str(file.attrs["version"])
        if version == "0.4":
            continue
        if version != "0.3":
            raise RuntimeError(f"Unsupported source version {version!r} in {path.name}")
        if _sha256(path) != artifact["source_sha256"]:
            raise RuntimeError(f"Legacy source checksum mismatch for {path.name}")

        before = _snapshot(path)
        molecular_system = msm.convert(path, to_form="molsysmt.MolSys")
        temporary = path.with_name(f".{path.stem}.v04.h5msm")
        try:
            msm.convert(
                molecular_system,
                to_form="file:h5msm",
                output_filename=temporary,
            )
            _assert_equivalent(before, temporary)
            os.replace(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)
        print(f"Migrated {path.name} to H5MSM 0.4")


if __name__ == "__main__":
    migrate()
