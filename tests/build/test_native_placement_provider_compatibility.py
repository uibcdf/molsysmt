"""Keep public native placement compatible with supported Pandas providers."""

import warnings

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.fixture(scope="module")
def peptide():
    system = msm.build.build_peptide(
        "AAA", engine="MolSysMT", to_form="molsysmt.MolSys"
    )
    xyz = puw.get_value(system.structures.coordinates, to_unit="nm")
    system.structures.coordinates = puw.quantity(
        np.concatenate([xyz, xyz + [1.25, -0.5, 0.7]], axis=0), "nm"
    )
    # MolSysDict 0.2 deliberately excludes the experimental mechanics domain.
    system.molecular_mechanics = None
    return system


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "molsysmt.MolSysDict"])
@pytest.mark.parametrize("operation", ["hydrogens", "heavy_atoms", "cappings"])
def test_public_native_placement_preserves_bonds_without_provider_warnings(
    peptide, form, operation
):
    if operation == "hydrogens":
        source = msm.remove(peptide, selection='atom_type=="H"')
    elif operation == "heavy_atoms":
        source = msm.remove(peptide, selection='atom_name=="CB"')
    else:
        source = peptide.copy()
    before_atoms = source.topology.atoms.copy(deep=True)
    before_bonds = source.chemical_states.get_bonds().copy(deep=True)
    before_xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    item = msm.convert(source, to_form=form)

    with warnings.catch_warnings():
        # Pandas4Warning is not a FutureWarning: reject every warning here.
        warnings.simplefilter("error")
        if operation == "hydrogens":
            result = msm.build.add_missing_hydrogens(item, engine="MolSysMT")
        elif operation == "heavy_atoms":
            result = msm.build.add_missing_heavy_atoms(item, engine="MolSysMT")
        else:
            result = msm.build.add_missing_terminal_cappings(
                item, N_terminal="ACE", C_terminal="NME", engine="MolSysMT"
            )

    assert msm.get_form(result) == form
    observed = msm.convert(result, to_form="molsysmt.MolSys")
    bonds = observed.chemical_states.get_bonds()
    pairs = list(zip(bonds["atom1_index"], bonds["atom2_index"]))
    assert pairs == sorted(set(pairs))
    assert all(left < right for left, right in pairs)
    assert bonds.index.tolist() == list(range(len(bonds)))
    assert str(bonds["atom1_index"].dtype) == "Int64"
    assert str(bonds["atom2_index"].dtype) == "Int64"
    expected_groups = (
        ["ACE", "ALA", "ALA", "ALA", "NME"]
        if operation == "cappings"
        else ["ALA", "ALA", "ALA"]
    )
    assert observed.topology.groups["group_name"].tolist() == expected_groups
    expected_atoms = peptide.get(n_atoms=True) + (12 if operation == "cappings" else 0)
    assert observed.get(n_atoms=True) == expected_atoms

    # Identify original atoms by group position/name, allowing inserted cap groups.
    group_shift = int(operation == "cappings")
    new_index = {
        (int(row.group_index), row.atom_name): int(index)
        for index, row in observed.topology.atoms.iterrows()
    }
    old_to_new = [
        new_index[(int(row.group_index) + group_shift, row.atom_name)]
        for _, row in before_atoms.iterrows()
    ]
    observed_xyz = puw.get_value(observed.structures.coordinates, to_unit="nm")
    assert observed_xyz.shape == (2, expected_atoms, 3)
    np.testing.assert_array_equal(observed_xyz[:, old_to_new], before_xyz)
    for left, right in before_bonds[["atom1_index", "atom2_index"]].itertuples(
        index=False, name=None
    ):
        assert tuple(sorted((old_to_new[left], old_to_new[right]))) in pairs
    pd.testing.assert_frame_equal(source.topology.atoms, before_atoms)
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before_bonds)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), before_xyz
    )
