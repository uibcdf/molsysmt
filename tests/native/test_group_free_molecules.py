"""Protecting the component fallback without inventing group hierarchy."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm


@pytest.fixture(
    params=[
        "rdkit.Mol",
        "molsysmt.Topology",
        "molsysmt.MolSys",
        "molsysmt.MolSysDict",
        "h5msm",
    ]
)
def group_free_system(request, tmp_path):
    from rdkit import Chem

    source = Chem.MolFromSmiles("CCO.COC")
    if request.param == "rdkit.Mol":
        return source
    native = msm.convert(source, to_form="molsysmt.MolSys")
    if request.param == "h5msm":
        return msm.convert(native, to_form=str(tmp_path / "molecules.h5msm"))
    return msm.convert(native, to_form=request.param)


def test_group_free_molecule_inventory_and_atom_membership(group_free_system):
    assert msm.get(group_free_system, n_groups=True) == 0
    assert msm.get(group_free_system, n_molecules=True) == 2
    assert msm.get(group_free_system, element="atom", molecule_index=True) == [
        0,
        0,
        0,
        1,
        1,
        1,
    ]
    assert msm.get(
        group_free_system, element="molecule", molecule_index=True, atom_index=True
    ) == [[0, 1], [[0, 1, 2], [3, 4, 5]]]
    assert msm.get(group_free_system, n_groups=True) == 0


@pytest.mark.parametrize(
    "selection,indices,atoms",
    [
        ([1, 0, 1], [1, 0, 1], [[3, 4, 5], [0, 1, 2], [3, 4, 5]]),
        ([], [], []),
        ("atom_index==0", [0], [[0, 1, 2]]),
    ],
)
def test_group_free_molecule_selection(group_free_system, selection, indices, atoms):
    result = msm.get(
        group_free_system,
        element="molecule",
        selection=selection,
        molecule_index=True,
        atom_index=True,
    )
    assert result == [indices, atoms]


def test_native_rebuild_keeps_no_groups_and_string_ids():
    from molsysmt.native import MolSys

    molsys = MolSys(n_atoms=3)
    topology = molsys.topology
    molsys.chemical_states._append_chemical_state_bonds([[0, 1]])
    molsys.rebuild_components()
    molsys.rebuild_molecules()
    assert topology.n_groups == 0
    assert topology.n_molecules == 2
    assert topology.molecules.molecule_id.tolist() == ["0", "1"]
    np.testing.assert_array_equal(
        msm.get(topology, element="atom", molecule_index=True), [0, 0, 1]
    )
    before = topology.atoms.copy(deep=True)
    msm.get(topology, element="molecule", atom_index=True)
    pd.testing.assert_frame_equal(before, pd.DataFrame(topology.atoms))


def test_explicit_group_based_molecules_are_preserved():
    builder = msm.MolSysBuilder()
    a = builder.add_atom(atom_name="C", atom_type="C")
    b = builder.add_atom(atom_name="O", atom_type="O")
    builder.add_group([a], group_name="LIG")
    builder.add_group([b], group_name="LIG")
    molsys = builder.build()
    molsys.topology.groups["molecule_index"] = [0, 0]
    molsys.topology.reset_molecules(n_molecules=1)
    molsys.topology.molecules["molecule_id"] = ["declared"]
    assert msm.get(molsys, element="molecule", atom_index=True) == [[0, 1]]
    assert molsys.topology.n_molecules == 1
    assert molsys.topology.molecules.molecule_id.tolist() == ["declared"]


def test_group_free_molecule_axis_uses_reference_not_active_state_components():
    from rdkit import Chem

    from molsysmt.native._chemical_state import Components_DataFrame
    from molsysmt.native._topology_infer import molecule_indices_from_atoms

    molsys = msm.convert(Chem.MolFromSmiles("CCO.COC"), to_form="molsysmt.MolSys")
    topology = molsys.topology
    other = molsys.chemical_states.append_state()
    state = molsys.chemical_states._states[other]
    state.state_id = "joined"
    state.component_indices[:] = 0
    state.components = Components_DataFrame(n_components=1)
    with molsys.chemical_states._using_chemical_state(other):
        assert molecule_indices_from_atoms(topology).tolist() == [0, 0, 0, 1, 1, 1]


def test_charged_disconnected_components_keep_source_molecule_axis():
    from rdkit import Chem

    source = Chem.MolFromSmiles("[Na+].CC(=O)[O-]")
    original = source.ToBinary()
    native = msm.convert(source, to_form="molsysmt.MolSys")
    assert msm.get(native, n_molecules=True) == 2
    assert msm.get(native, n_groups=True) == 0
    assert msm.get(native, element="atom", molecule_index=True) == [0, 1, 1, 1, 1]
    assert source.ToBinary() == original


def test_dictionary_to_builder_keeps_explicit_group_absence_on_build():
    from rdkit import Chem

    native = msm.convert(Chem.MolFromSmiles("CCO.COC"), to_form="molsysmt.MolSys")
    records = msm.convert(native, to_form="molsysmt.MolSysDict")
    builder = msm.convert(records, to_form="molsysmt.MolSysBuilder")
    output = builder.build()
    assert output.topology.n_groups == 0
    assert output.topology.n_molecules == 2
    assert msm.get(output, element="molecule", atom_index=True) == [
        [0, 1, 2],
        [3, 4, 5],
    ]


def test_native_source_builder_preserves_declared_group_free_molecule_axis():
    from rdkit import Chem

    source = msm.convert(Chem.MolFromSmiles("CCO.COC"), to_form="molsysmt.MolSys")
    output = msm.MolSysBuilder(source).build()
    assert output.topology.n_groups == 0
    assert output.topology.n_molecules == 2
    assert msm.get(output, element="molecule", atom_index=True) == [
        [0, 1, 2],
        [3, 4, 5],
    ]


def test_builder_rejects_unsupported_input_with_the_declared_diagnostic():
    from molsysmt._private.smonitor import ArgumentChoiceError

    with pytest.raises(
        ArgumentChoiceError, match="MolSysBuilder can only be initialized"
    ):
        msm.MolSysBuilder(object())
    assert msm.MolSysBuilder().n_atoms == 0
