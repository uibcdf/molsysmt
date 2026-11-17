"""Receive the complete sparse-analysis recipe and its native ownership boundary."""

import re
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize("length_unit,time_unit", [("nm", "ps"), ("pm", "fs")])
def test_sparse_recipe_preserves_coverage_handles_and_chemical_owner(
    length_unit, time_unit
):
    page = ROOT / "docs/content/user/cookbook/querying_sparse_interactions.md"
    blocks = re.findall(r"^```python\n(.*?)^```", page.read_text(), re.M | re.S)
    namespace = {}
    with msm.pyunitwizard.context(
        standard_units=[length_unit, time_unit, "radians", "elementary_charge"]
    ):
        for block in blocks:
            exec(compile(block, str(page), "exec"), namespace)
        original = namespace["interactions"]
        assert original.evaluated_structure_indices.tolist() == [0, 1, 3]
        assert original.n_interactions == 2
        assert namespace["old_view"].n_interactions == 1
        persisted = namespace["stored"].query(structure_indices=[3, 0]).to_dict()
        assert persisted["occurrence_indices"].tolist() == [1, 0]
        assert persisted["measure_units"]["distance"] == "nm"
        np.testing.assert_allclose(persisted["measurements"]["distance"], [0.36, 0.2])
        assert namespace["subset"].interactions["example"].n_atoms == 3
        assert namespace["molsys_trimmed"].get(n_atoms=True) == 8
        assert set(
            namespace["molsys_edited"]
            .interactions["example"]
            .evaluated_structure_indices.tolist()
        ) == {0, 1, 3}
        assert not hasattr(namespace["molsys"].topology, "bonds")
        assert namespace["molsys"].chemical_states.get(n_bonds=True) == 1
        assert namespace["old_coverage"].evaluated_structure_indices.tolist() == [0]
        assert (
            namespace["molsys"]
            .interactions["before_bond_edit"]
            .evaluated_structure_indices.size
            == 0
        )
        assert namespace["chemical_snapshot"].get(n_bonds=True) == 0
