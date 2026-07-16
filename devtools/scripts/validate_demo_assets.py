"""Validating bundled demo assets against their independent manifest."""

from __future__ import annotations

import json
from pathlib import Path

import h5py


REPOSITORY = Path(__file__).resolve().parents[2]
DATA_DIR = REPOSITORY / "molsysmt" / "data"
MANIFEST = DATA_DIR / "demo_manifest.json"


def validate() -> None:
    """Validating schema version, hierarchy sizes, state metadata, and recipes."""

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    order = manifest["expected_order"]
    paths = {
        "atoms": "topology/atoms/atom_id",
        "groups": "topology/groups/group_id",
        "components": "topology/components/component_id",
        "molecules": "topology/molecules/molecule_id",
        "entities": "topology/entities/entity_id",
        "chains": "topology/chains/chain_id",
        "bonds": "topology/bonds/atom1_index",
        "structures": "structures/coordinates",
    }

    for artifact in manifest["artifacts"]:
        path = DATA_DIR / "h5msm" / artifact["file"]
        recipe = artifact["recipe"]
        if recipe.endswith(".py") and not (REPOSITORY / recipe).is_file():
            raise AssertionError(f"Missing generation recipe: {recipe}")
        with h5py.File(path, "r") as file:
            assert str(file.attrs["version"]) == manifest["h5msm_target_version"]
            observed = [len(file[paths[name]]) for name in order]
            assert observed == artifact["expected"], (path.name, observed)
            assert "topology/chemical_states/0" in file
            state = file["topology/chemical_states/0"]
            assert state.attrs["connectivity_completeness"] == "complete"
            assert state.attrs["component_evidence"] == "unknown"
            assert "formal_charge" not in state["atom_attributes"]
            assert file["structures/coordinates"].shape == (
                artifact["expected"][-1], artifact["expected"][0], 3
            )

    legacy = REPOSITORY / "tests/form/file_h5msm/data/alanine_dipeptide_v03.h5msm"
    with h5py.File(legacy, "r") as file:
        assert str(file.attrs["version"]) == "0.3"
    print(f"Validated {len(manifest['artifacts'])} H5MSM 0.4 demos and one 0.3 fixture")


if __name__ == "__main__":
    validate()
