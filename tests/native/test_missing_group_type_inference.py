"""Keep missing group types unknown through native molecule reconstruction."""

import numpy as np
import pandas as pd
import pytest

from molsysmt.native import Topology


@pytest.mark.parametrize("missing", [None, pd.NA, np.nan])
def test_missing_group_type_does_not_break_molecule_reconstruction(missing):
    topology = Topology(n_groups=1, n_molecules=1)
    topology.groups["group_name"] = ["LIG"]
    topology.groups["group_type"] = [missing]
    topology.groups["molecule_index"] = pd.array([0], dtype="Int64")
    topology.rebuild_molecules(redefine_indices=False, redefine_names=False)
    assert topology.molecules["molecule_type"].tolist() == ["unknown"]
    assert topology.groups["group_type"].isna().all()
    assert topology.groups["molecule_index"].tolist() == [0]


@pytest.mark.parametrize("missing", [None, pd.NA, np.nan])
def test_missing_last_group_type_preserves_unknown_and_allows_reconstruction(missing):
    topology = Topology(n_groups=2, n_molecules=1)
    topology.groups["group_name"] = ["ALA", "LIG"]
    topology.groups["group_type"] = ["amino acid", missing]
    topology.groups["molecule_index"] = pd.array([0, 0], dtype="Int64")
    topology.rebuild_molecules(redefine_indices=False, redefine_names=False)
    assert topology.molecules["molecule_type"].tolist() == ["peptide"]
    assert pd.isna(topology.groups.iloc[1]["group_type"])


def test_new_group_without_assigned_name_or_type_has_an_unknown_molecule():
    topology = Topology(n_groups=1, n_molecules=1)
    topology.groups["molecule_index"] = pd.array([0], dtype="Int64")
    topology.rebuild_molecules(redefine_indices=False, redefine_names=False)
    assert topology.molecules["molecule_type"].tolist() == ["unknown"]
    assert topology.groups["group_name"].isna().all()
    assert topology.groups["group_type"].isna().all()
