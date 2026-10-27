"""Group insertion retains a group-free source's molecule axis and evidence."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


def source(smiles="CCO.COC"):
    from rdkit import Chem

    result = msm.convert(Chem.MolFromSmiles(smiles), to_form="molsysmt.MolSys")
    result.topology.molecules["molecule_id"] = pd.Series(
        [f"source-{i}" for i in range(result.topology.n_molecules)], dtype="string"
    )
    result.topology.molecules["molecule_name"] = [
        f"compound {i}" for i in range(result.topology.n_molecules)
    ]
    return result


@pytest.mark.parametrize(
    "groups", [[], [[0, 1, 2], [3, 4, 5]], [[2]], [[3, 4, 5]], [[2], [0, 1], [3, 4, 5]]]
)
@pytest.mark.parametrize("copy_mode", [None, True, False])
def test_full_and_partial_group_insertion_preserves_molecular_identity(
    groups, copy_mode
):
    molsys = source()
    reference = molsys.topology.molecules.copy(deep=True)
    atom_table = molsys.topology.atoms.copy(deep=True)
    builder = msm.MolSysBuilder(molsys)
    if copy_mode is not None:
        builder = builder.copy(deep=copy_mode)
    for atoms in groups:
        builder.add_group(atoms, group_name="LIG")
    result = builder.build()
    assert result.topology.n_molecules == 2
    pd.testing.assert_frame_equal(reference, pd.DataFrame(result.topology.molecules))
    assert msm.get(result, element="molecule", atom_index=True) == [
        [0, 1, 2],
        [3, 4, 5],
    ]
    assert msm.get(result, element="atom", molecule_index=True) == [0, 0, 0, 1, 1, 1]
    assert msm.get(
        result, element="molecule", selection=[1, 0, 1], atom_index=True
    ) == [[3, 4, 5], [0, 1, 2], [3, 4, 5]]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(
            msm.physchem.get_tpsa(result), to_unit="angstrom**2"
        ),
        [20.23, 9.23],
        atol=1e-12,
    )
    assert molsys.topology.n_groups == 0
    pd.testing.assert_frame_equal(atom_table, pd.DataFrame(molsys.topology.atoms))
    assert builder.build().topology.n_molecules == 2


def test_group_cannot_cross_inherited_molecules_and_rejection_is_atomic():
    builder = msm.MolSysBuilder(source())
    with pytest.raises(
        msm.StructuralInconsistencyError, match="multiple inherited source molecules"
    ):
        builder.add_group([0, 3], group_name="LIG")
    assert builder.n_groups == 0
    assert builder.n_molecules == 2
    assert builder.topology.atoms.group_index.isna().all()
    builder.add_group([0, 1, 2], group_name="LIG")
    assert builder.build().topology.n_molecules == 2


def test_single_source_molecule_can_have_multiple_groups_without_repartition():
    builder = msm.MolSysBuilder(source("CCO"))
    builder.add_group([2], group_name="POLAR")
    builder.add_group([0, 1], group_name="ALKYL")
    result = builder.build()
    assert result.topology.groups.molecule_index.tolist() == [0, 0]
    assert result.topology.molecules.molecule_id.tolist() == ["source-0"]
    assert msm.get(result, element="molecule", atom_index=True) == [[0, 1, 2]]


def test_reference_identity_is_not_taken_from_a_different_chemical_state():
    molsys = source()
    state = deepcopy(molsys.chemical_states._states[0])
    state.state_id = "joined"
    state.component_indices[:] = 0
    state.components = state.components.iloc[:1].copy()
    molsys.chemical_states._append_state(state, False)
    from molsysmt.native.topology import _ACTIVE_CHEMICAL_STATE_INDICES

    token = _ACTIVE_CHEMICAL_STATE_INDICES.set({id(molsys.topology): 1})
    try:
        builder = msm.MolSysBuilder(molsys)
    finally:
        _ACTIVE_CHEMICAL_STATE_INDICES.reset(token)
    builder.add_group([0, 1, 2], group_name="LIG")
    builder.add_group([3, 4, 5], group_name="LIG")
    assert builder.build().topology.n_molecules == 2


def test_new_atoms_and_explicit_new_molecule_remain_supported():
    builder = msm.MolSysBuilder(source("CCO"))
    builder.add_group([0, 1, 2], group_name="LIG")
    new_atom = builder.add_atom(atom_name="Ar", atom_type="Ar")
    group = builder.add_group([new_atom], group_name="AR")
    builder.add_molecule([group], molecule_id="new-argon", molecule_name="argon")
    result = builder.build()
    assert result.topology.molecules.molecule_id.tolist() == ["source-0", "new-argon"]
    assert msm.get(result, element="molecule", atom_index=True) == [[0, 1, 2], [3]]
