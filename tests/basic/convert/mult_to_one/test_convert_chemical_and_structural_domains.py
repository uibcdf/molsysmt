"""Checking declared composition of chemical and structural index domains."""

from itertools import permutations

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import ChemicalStates, MolecularMechanics, MolSys, Topology


@pytest.fixture
def domains():
    system = MolSys(n_atoms=4)
    system.chemical_states.add_bonds([[0, 1], [2, 3]])
    msm.set(system.chemical_states, element="atom", formal_charge=[0, 1, -1, 0])
    first = system.chemical_states._states[0]
    first.state_id = "neutral-reference"
    first.connectivity_completeness = "complete"
    second = first.copy()
    second.state_id = "charged-reference"
    second.atom_attributes["formal_charge"] = pd.array([1, 0, 0, -1], dtype="Int64")
    second.provenance_index = 12
    system.chemical_states._append_state(second, set_as_reference=True)
    system.structures.append(
        coordinates=puw.quantity(np.arange(36).reshape(3, 4, 3), "angstrom"),
        box=puw.quantity(np.repeat((np.eye(3) * 20)[None], 3, axis=0), "angstrom"),
        time=puw.quantity([0, 1000, 2000], "fs"),
    )
    system.structures.structure_id = np.array(["frame-a", "frame-b", "frame-c"])
    return system.chemical_states, system.structures


def _source(states, structures, dictionary, reverse):
    chemistry = (
        msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
        if dictionary
        else states
    )
    return [structures, chemistry] if reverse else [chemistry, structures]


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_compose_chemical_and_structural_domains_without_inventing_topology(
    domains, dictionary, reverse
):
    states, structures = domains
    result = msm.convert(
        _source(states, structures, dictionary, reverse), to_form="molsysmt.MolSys"
    )
    assert result.topology is None and not result.interactions
    assert msm.get(result, n_atoms=True, n_structures=True) == [4, 3]
    assert result.chemical_states.n_chemical_states == 2
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result.chemical_states is not states and result.structures is not structures
    assert result._structure_chemical_state_indices is None
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    for actual, expected in zip(result.chemical_states._states, states._states):
        pd.testing.assert_frame_equal(actual.atom_attributes, expected.atom_attributes)
        pd.testing.assert_frame_equal(
            actual.bonds, expected.bonds, check_frame_type=False
        )
        assert actual.state_id == expected.state_id
        assert actual.provenance_index == expected.provenance_index
        assert actual.connectivity_completeness == "complete"
    assert puw.get_unit(result.structures.coordinates) == puw.unit("nm")
    assert puw.get_unit(result.structures.time) == puw.unit("ps")
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        np.arange(36).reshape(3, 4, 3) * 0.1,
        atol=1e-12,
        rtol=0,
    )
    # The default result owns its domains, so editing it leaves both inputs intact.
    result.chemical_states._states[1].atom_attributes.loc[0, "formal_charge"] = 99
    result.structures.set_box(
        value=puw.quantity(np.repeat((np.eye(3) * 3)[None], 3, axis=0), "nm")
    )
    assert states._states[1].atom_attributes.loc[0, "formal_charge"] == 1
    np.testing.assert_allclose(
        puw.get_value(structures.box, to_unit="nm"),
        np.repeat((np.eye(3) * 2)[None], 3, axis=0),
        atol=1e-12,
        rtol=0,
    )


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
def test_selected_composition_remaps_bonds_charges_and_frames_in_requested_order(
    domains, dictionary, reverse
):
    states, structures = domains
    with puw.context(standard_units=["angstrom", "fs", "degree"]):
        result = msm.convert(
            _source(states, structures, dictionary, reverse),
            selection=[3, 2, 0],
            structure_indices=[2, 0, 2],
        )
    assert result.topology is None
    assert result.chemical_states.n_atoms == 3
    assert result.chemical_states.reference_chemical_state_index == 1
    for state in result.chemical_states._states:
        assert state.bonds[["atom1_index", "atom2_index"]].to_numpy().tolist() == [
            [0, 1]
        ]
    assert result.chemical_states._states[1].atom_attributes.formal_charge.tolist() == [
        -1,
        0,
        1,
    ]
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        (np.arange(36).reshape(3, 4, 3) * 0.1)[[2, 0, 2]][:, [3, 2, 0]],
        atol=1e-12,
        rtol=0,
    )
    np.testing.assert_array_equal(
        puw.get_value(result.structures.time, to_unit="ps"), [2, 0, 2]
    )
    assert result.structures.structure_id.tolist() == ["frame-c", "frame-a", "frame-c"]
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    assert states.n_atoms == 4 and structures.n_atoms == 4


@pytest.mark.parametrize("dictionary", [False, True])
def test_incompatible_full_atom_axes_fail_before_a_selection_can_hide_them(
    domains, dictionary
):
    states, structures = domains
    shorter = structures.extract(atom_indices=[0, 1, 2])
    with pytest.raises(StructuralInconsistencyError, match="atom (counts|domain)"):
        msm.convert(_source(states, shorter, dictionary, False), selection=[0, 1])


def test_copy_policy_and_single_state_implicit_association(domains):
    states, structures = domains
    single = states.copy()
    single._replace_states([single._states[0]], reference_index=0)
    result = msm.convert([single, structures], copy_if_all=False)
    assert result.chemical_states is single and result.structures is structures
    assert result._structure_chemical_state_indices is None
    assert result._get_structure_chemical_state_indices().tolist() == [0, 0, 0]
    selected = msm.convert([single, structures], selection=[1, 0], copy_if_all=False)
    assert (
        selected.chemical_states is not single and selected.structures is not structures
    )


def test_composed_domains_persist_through_public_h5msm_conversion(domains, tmp_path):
    states, structures = domains
    path = str(tmp_path / "domains.h5msm")
    msm.convert(
        [states, structures],
        to_form=path,
        selection=[3, 2, 0],
        structure_indices=[2, 0],
    )
    restored = msm.convert(path)
    assert restored.topology is None
    assert restored.chemical_states.reference_chemical_state_index == 1
    assert restored.chemical_states._states[1].state_id == "charged-reference"
    assert restored.chemical_states._states[
        1
    ].atom_attributes.formal_charge.tolist() == [-1, 0, 1]
    np.testing.assert_array_equal(
        puw.get_value(restored.structures.time, to_unit="ps"), [2, 0]
    )
    assert pd.isna(restored._get_structure_chemical_state_indices()).all()


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("indices", [[2, 0, 2], [1], []])
def test_explicit_chemistry_and_dcd_read_only_requested_structures(
    domains, tmp_path, monkeypatch, dictionary, reverse, indices
):
    states, structures = domains
    from functools import wraps

    from molsysmt.form import _dict_modules, load_converter
    from molsysmt.native import Topology

    path = str(tmp_path / "coordinates.dcd")
    formats = pytest.importorskip("mdtraj.formats")
    # The DCD writer's low-level numerical boundary uses angstroms.
    with formats.DCDTrajectoryFile(path, mode="w") as file:
        file.write(
            puw.get_value(structures.coordinates, to_unit="angstrom").astype(np.float32)
        )
    module = _dict_modules["file:dcd"]
    original = load_converter(module, module._convert_to["molsysmt.Structures"])
    requested = []

    @wraps(original)
    def read(item, **kwargs):
        requested.append(list(kwargs["structure_indices"]))
        return original(item, **kwargs)

    monkeypatch.setitem(module._convert_to, "molsysmt.Structures", read)
    chemistry = (
        msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
        if dictionary
        else states
    )
    topology = Topology(n_atoms=4)
    topology.atoms["atom_id"] = ["A", "B", "C", "D"]
    providers = [topology, chemistry, path]
    if reverse:
        providers.reverse()
    result = msm.convert(providers, selection=[0, 2, 3], structure_indices=indices)
    assert requested == [indices]
    assert result.topology.atoms.atom_id.tolist() == ["A", "C", "D"]
    assert result.chemical_states.n_chemical_states == 2
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result.chemical_states.get(element="atom", formal_charge=True) == [1, 0, -1]
    assert result.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[1, 2]]
    assert result._structure_chemical_state_indices is None
    assert result.structures.coordinates.shape == (len(indices), 3, 3)
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        puw.get_value(structures.coordinates, to_unit="nm")[indices][:, [0, 2, 3]],
        atol=1e-6,
        rtol=0,
    )
    assert states.n_atoms == 4
    assert states.get(element="atom", formal_charge=True) == [1, 0, 0, -1]


@pytest.fixture
def inventory_domains(domains):
    states, structures = domains
    topology = Topology(n_atoms=4)
    topology.atoms["atom_id"] = pd.array(["a", "b", "c", "d"], dtype="string")
    topology.atoms["atom_name"] = pd.array(["C1", "N1", "O1", "H1"], dtype="string")
    return topology, states, structures


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("order", list(permutations(range(3))))
def test_inventory_chemistry_structures_composition_preserves_explicit_domains(
    inventory_domains, dictionary, order
):
    topology, states, structures = inventory_domains
    chemistry = (
        msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
        if dictionary
        else states
    )
    providers = [topology, chemistry, structures]
    result = msm.convert([providers[index] for index in order])

    assert result.topology is not topology
    assert result.chemical_states is not states
    assert result.structures is not structures
    assert result.topology.atoms.atom_id.tolist() == ["a", "b", "c", "d"]
    assert result.topology.atoms.atom_name.tolist() == ["C1", "N1", "O1", "H1"]
    assert not hasattr(result.topology, "bonds")
    assert not hasattr(result.topology, "chemical_states")
    assert result.chemical_states.n_chemical_states == 2
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result._structure_chemical_state_indices is None
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    for index, (state, charges) in enumerate(
        zip(result.chemical_states._states, [[0, 1, -1, 0], [1, 0, 0, -1]])
    ):
        assert state.atom_attributes.formal_charge.tolist() == charges
        assert state.bonds[["atom1_index", "atom2_index"]].values.tolist() == [
            [0, 1],
            [2, 3],
        ]
        assert state.state_id == ["neutral-reference", "charged-reference"][index]
        assert state.connectivity_completeness == "complete"
    assert result.chemical_states._states[1].provenance_index == 12
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="angstrom"),
        np.arange(36).reshape(3, 4, 3),
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        puw.get_value(result.structures.box, to_unit="angstrom"),
        np.repeat((np.eye(3) * 20)[None], 3, axis=0),
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_array_equal(
        puw.get_value(result.structures.time, to_unit="ps"), [0, 1, 2]
    )

    # Neither assembly nor editing the independent result may rewrite its inputs.
    result.topology.atoms.loc[0, "atom_id"] = "changed"
    result.chemical_states._states[1].atom_attributes.loc[0, "formal_charge"] = 99
    result.structures.set_coordinates(
        structure_indices=[0],
        indices=[0],
        value=puw.quantity([[[99, 0, 0]]], "nm"),
    )
    assert topology.atoms.atom_id.tolist() == ["a", "b", "c", "d"]
    assert states._states[1].atom_attributes.formal_charge.tolist() == [1, 0, 0, -1]
    assert puw.get_value(structures.coordinates, to_unit="nm")[0, 0, 0] == 0
    if dictionary:
        assert chemistry.get(element="atom", formal_charge=True) == [1, 0, 0, -1]


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("atoms,indices", [([0, 2, 3], [2, 0, 2]), ([], [])])
def test_inventory_composition_projects_domains_together(
    inventory_domains, dictionary, reverse, atoms, indices
):
    topology, states, structures = inventory_domains
    chemistry = (
        msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
        if dictionary
        else states
    )
    providers = [topology, chemistry, structures]
    if reverse:
        providers.reverse()
    with puw.context(standard_units=["angstrom", "fs", "degree"]):
        result = msm.convert(providers, selection=atoms, structure_indices=indices)
    assert result.topology.atoms.atom_id.tolist() == (["a", "c", "d"] if atoms else [])
    assert result.chemical_states.n_atoms == len(atoms)
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result.chemical_states._states[1].atom_attributes.formal_charge.tolist() == (
        [1, 0, -1] if atoms else []
    )
    for state in result.chemical_states._states:
        assert state.bonds[["atom1_index", "atom2_index"]].values.tolist() == (
            [[1, 2]] if atoms else []
        )
    assert result.structures.coordinates.shape == (len(indices), len(atoms), 3)
    np.testing.assert_allclose(
        puw.get_value(result.structures.coordinates, to_unit="nm"),
        (np.arange(36).reshape(3, 4, 3) * 0.1)[indices][:, atoms],
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_array_equal(
        puw.get_value(result.structures.time, to_unit="ps"), indices
    )
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    assert topology.n_atoms == states.n_atoms == structures.n_atoms == 4
    assert structures.n_structures == 3


@pytest.mark.parametrize("dictionary", [False, True])
@pytest.mark.parametrize("invalid", ["topology", "chemistry", "structures"])
def test_inventory_composition_rejects_full_atom_conflicts_before_selection(
    inventory_domains, dictionary, invalid
):
    topology, states, structures = inventory_domains
    if invalid == "topology":
        topology = Topology(n_atoms=3)
    elif invalid == "chemistry":
        states = states._extract_atoms([0, 1, 2])
    else:
        structures = structures.extract(atom_indices=[0, 1, 2])
    chemistry = (
        msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
        if dictionary
        else states
    )
    with pytest.raises(StructuralInconsistencyError, match="atom (domain|counts)"):
        msm.convert([topology, chemistry, structures], selection=[0, 1])
    assert inventory_domains[0].atoms.atom_id.tolist() == ["a", "b", "c", "d"]
    assert inventory_domains[1].reference_chemical_state_index == 1
    assert inventory_domains[2].coordinates.shape == (3, 4, 3)


@pytest.mark.parametrize(
    "duplicate", ["topology", "chemistry", "mixed-chemistry", "structures"]
)
def test_dictionary_composition_rejects_repeated_domains(inventory_domains, duplicate):
    topology, states, structures = inventory_domains
    chemistry = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    providers = [topology, chemistry, structures]
    extra = {
        "topology": topology,
        "chemistry": chemistry,
        "mixed-chemistry": states,
        "structures": structures,
    }[duplicate]
    with pytest.raises(StructuralInconsistencyError, match="repeat"):
        msm.convert([*providers, extra])
    assert topology.atoms.atom_id.tolist() == ["a", "b", "c", "d"]
    assert states.n_chemical_states == 2
    assert structures.coordinates.shape == (3, 4, 3)


def test_dictionary_composition_keeps_single_state_and_no_final_copy_policy(
    inventory_domains,
):
    topology, states, structures = inventory_domains
    single = states.copy()
    single._replace_states([single._states[0]], reference_index=0)
    chemistry = msm.convert(single, to_form="molsysmt.ChemicalStatesDict")
    result = msm.convert([topology, chemistry, structures], copy_if_all=False)
    assert result.topology is not topology
    assert result.structures is structures
    assert result.chemical_states._states[0].state_id == "neutral-reference"
    assert result._get_structure_chemical_state_indices().tolist() == [0, 0, 0]
    result.chemical_states._states[0].atom_attributes.loc[0, "formal_charge"] = 99
    assert chemistry.get(element="atom", formal_charge=True) == [0, 1, -1, 0]


def test_dictionary_inventory_composition_persists_selected_domains(
    inventory_domains, tmp_path
):
    topology, states, structures = inventory_domains
    chemistry = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    path = str(tmp_path / "inventory-chemical-dictionary.h5msm")
    msm.convert(
        [topology, chemistry, structures],
        to_form=path,
        selection=[0, 2, 3],
        structure_indices=[2, 0],
    )
    restored = msm.convert(path)
    assert restored.topology.atoms.atom_id.tolist() == ["a", "c", "d"]
    assert restored.chemical_states.reference_chemical_state_index == 1
    assert restored.chemical_states._states[1].provenance_index == 12
    assert restored.chemical_states._states[
        1
    ].atom_attributes.formal_charge.tolist() == [1, 0, -1]
    assert restored.chemical_states.get_bonds()[
        ["atom1_index", "atom2_index"]
    ].values.tolist() == [[1, 2]]
    assert pd.isna(restored._get_structure_chemical_state_indices()).all()
    np.testing.assert_allclose(
        puw.get_value(restored.structures.coordinates, to_unit="nm"),
        (np.arange(36).reshape(3, 4, 3) * 0.1)[[2, 0]][:, [0, 2, 3]],
        rtol=0,
        atol=1e-12,
    )


def test_dictionary_inventory_composition_preserves_zero_states(inventory_domains):
    topology, _, structures = inventory_domains
    payload = msm.convert(
        ChemicalStates(n_atoms=4), to_form="molsysmt.ChemicalStatesDict"
    )
    result = msm.convert([topology, payload, structures])
    assert result.chemical_states.n_atoms == 4
    assert result.chemical_states.n_chemical_states == 0
    assert result.chemical_states.reference_chemical_state_index is None
    assert pd.isna(result._get_structure_chemical_state_indices()).all()
    assert result.topology.atoms.atom_id.tolist() == ["a", "b", "c", "d"]
    assert payload.get(n_chemical_states=True) == 0


@pytest.mark.parametrize("reverse", [False, True])
def test_dictionary_inventory_composition_preserves_mechanics(
    inventory_domains, reverse
):
    topology, states, structures = inventory_domains
    payload = msm.convert(states, to_form="molsysmt.ChemicalStatesDict")
    mechanics = MolecularMechanics(
        forcefield="declared-only", partial_charge=[0.1, 0.2, -0.4, 0.1]
    )
    providers = [topology, payload, structures, mechanics]
    if reverse:
        providers.reverse()
    result = msm.convert(providers, selection=[0, 2, 3], structure_indices=[2, 0])
    assert result.topology.atoms.atom_id.tolist() == ["a", "c", "d"]
    assert result.chemical_states.reference_chemical_state_index == 1
    assert result.molecular_mechanics.forcefield == "declared-only"
    np.testing.assert_allclose(msm.get(result, partial_charge=True), [0.1, -0.4, 0.1])
    result.molecular_mechanics.partial_charge = [9.0, 9.0, 9.0]
    np.testing.assert_allclose(
        msm.get(mechanics, element="atom", partial_charge=True), [0.1, 0.2, -0.4, 0.1]
    )
