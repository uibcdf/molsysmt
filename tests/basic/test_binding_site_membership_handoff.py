"""Check the finite public molecular facts offered to BindingMT under #746."""

import copy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Structures

puw = msm.pyunitwizard


@pytest.fixture
def source():
    molsys = MolSys(n_atoms=6, n_groups=3, n_chains=1, n_molecules=3, n_entities=3)
    topology = molsys.topology
    topology.atoms["atom_id"] = ["02", "same", "02", "4", "05", "last"]
    topology.atoms["atom_name"] = ["a", "b", "c", "d", "e", "f"]
    topology.atoms["atom_type"] = ["C"] * 6
    topology.atoms["group_index"] = pd.array([0, 1, 0, 2, 1, 2], dtype="Int64")
    topology.atoms["chain_index"] = pd.array([0] * 6, dtype="Int64")
    topology.groups["group_id"] = ["02", "same", "02"]
    topology.groups["group_name"] = ["LIG"] * 3
    topology.groups["group_type"] = ["small molecule"] * 3
    topology.groups["molecule_index"] = pd.array([0, 1, 2], dtype="Int64")
    topology.molecules["entity_index"] = pd.array([0, 1, 2], dtype="Int64")
    topology.chains["chain_id"] = ["A"]
    molsys.structures.coordinates = puw.quantity(
        np.arange(54, dtype=float).reshape(3, 6, 3), "nm"
    )
    molsys.structures.time = puw.quantity([10, 20, 30], "ps")
    second = molsys.chemical_states.append_state()
    assert second == 1
    msm.set(molsys, chemical_state=0, formal_charge=[1, 0, 0, 0, 0, 0])
    msm.set(molsys, chemical_state=1, formal_charge=[0, 0, 1, 0, 0, 0])
    msm.set(molsys, structure_chemical_state_index=[1, 0, 0])
    return molsys


def test_explicit_queries_keep_entry_order_without_using_ids_as_indices(source):
    assert source.get(n_atoms=True, n_groups=True, n_structures=True) == [6, 3, 3]
    assert msm.select(source, selection=[5, 1, 2], structure_indices=[2]) == [5, 1, 2]
    assert source.get(element="atom", selection=[5, 1, 2, 5], atom_index=True) == [
        5,
        1,
        2,
        5,
    ]
    assert source.get(element="atom", selection=[2, 0], atom_id=True) == ["02", "02"]
    assert source.get(element="group", selection=[2, 0], group_id=True) == ["02", "02"]
    # Expressions and active masks deliver source-ordered sets, not entry order.
    assert msm.select(source, "atom_index in [5, 1, 2]", structure_indices=[2]) == [
        1,
        2,
        5,
    ]
    assert msm.select(source, [5, 1, 2], mask=[2, 5, 1], structure_indices=[2]) == [
        1,
        2,
        5,
    ]


def test_group_expansion_preserves_declared_group_order_and_atom_relationships(source):
    assert source.get(element="group", selection=[2, 0], atom_index=True) == [
        [3, 5],
        [0, 2],
    ]
    assert msm.get(source, element="group", selection=[2, 0], atom_index=True) == [
        [3, 5],
        [0, 2],
    ]
    assert msm.select(source, "group_index in [2, 0]", structure_indices=[2]) == [
        0,
        2,
        3,
        5,
    ]
    assert source.get(element="atom", selection=[3, 5, 0, 2], group_index=True) == [
        2,
        2,
        0,
        0,
    ]


@pytest.mark.parametrize(
    "element,selection",
    [("atom", [-1]), ("atom", [6]), ("group", [-1]), ("group", [3])],
)
def test_public_selection_refuses_indices_outside_the_declared_axis(
    source, element, selection
):
    with pytest.raises(ArgumentError):
        msm.select(source, element=element, selection=selection, structure_indices=[2])


def test_known_empty_groups_and_unknown_parentage_are_distinct(source):
    source.topology.atoms["group_index"] = pd.array([0, 1, 0, 1, 1, 1], dtype="Int64")
    assert source.get(element="group", selection=[2], atom_index=True) == [[]]
    source.topology.atoms.loc[5, "group_index"] = pd.NA
    assert pd.isna(source.get(element="atom", selection=[5], group_index=True)[0])
    assert source.get(n_atoms=True, n_groups=True) == [6, 3]
    # Counts do not certify complete stored parentage or chemical interpretation.
    assert source.get(element="group", selection=[2], atom_index=True) == [[]]


def test_structure_state_queries_are_explicit_and_mixed_or_unknown_states_refuse(
    source,
):
    assert source.chemical_states.get(
        n_chemical_states=True, chemical_state_index=True
    ) == [2, [0, 1]]
    assert source.get(
        structure_indices=[2, 0, 2], structure_chemical_state_index=True
    ) == [0, 1, 0]
    assert msm.select(
        source, "formal_charge>0", structure_indices=[2], chemical_state="structure"
    ) == [0]
    assert msm.select(
        source, "formal_charge>0", structure_indices=[0], chemical_state="structure"
    ) == [2]
    with pytest.raises(StructuralInconsistencyError):
        msm.select(
            source,
            "formal_charge>0",
            structure_indices=[2, 0, 2],
            chemical_state="structure",
        )
    msm.set(source, structure_indices=[2], structure_chemical_state_index=pd.NA)
    with pytest.raises(StructuralInconsistencyError):
        msm.select(
            source, "formal_charge>0", structure_indices=[2], chemical_state="structure"
        )


@pytest.mark.parametrize("structures", [[-1], [3]])
def test_structure_queries_and_extraction_refuse_out_of_range_occurrences(
    source, structures
):
    with pytest.raises(ArgumentError):
        source.get(structure_indices=structures, structure_chemical_state_index=True)
    with pytest.raises(ArgumentError):
        msm.extract(source, selection=[0], structure_indices=structures)


def declared_extraction_map():
    # The caller knows this map because it requested a unique native subset,
    # whose documented output order is ascending source atom index.
    return dict(
        schema="molsysmt.atom_map@1",
        n_source_atoms=6,
        n_output_atoms=3,
        source_to_output_atom_indices=[-1, 0, 1, -1, -1, 2],
        output_to_source_atom_indices=[1, 2, 5],
    )


@pytest.mark.parametrize("length,time", [("nm", "ps"), ("pm", "fs")])
def test_extraction_permutation_saved_axes_and_repeated_occurrences(
    source, tmp_path, length, time
):
    before = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    with puw.context(standard_units=[length, time, "radians"]):
        subset = msm.extract(source, selection=[5, 1, 2], structure_indices=[2, 0, 2])
        assert subset.get(element="atom", atom_id=True) == ["same", "02", "last"]
        # Group rows follow first surviving atom occurrence, not requested group
        # order and not an independently sorted source-group vector.
        assert subset.get(element="group", group_id=True) == ["same", "02", "02"]
        source_groups = source.get(
            element="atom", selection=[1, 2, 5], group_index=True
        )
        target_groups = subset.get(element="atom", group_index=True)
        assert dict(zip(source_groups, target_groups)) == {1: 0, 0: 1, 2: 2}
        assert subset.get(structure_chemical_state_index=True) == [0, 1, 0]
        np.testing.assert_array_equal(
            puw.get_value(subset.get(coordinates=True), to_unit="nm"),
            before[[2, 0, 2]][:, [1, 2, 5]],
        )
        permuted = msm.permute_atoms(subset, [2, 0, 1], return_report=True)
        target = permuted["molecular_system"]
        maps = msm.compose_atom_maps([declared_extraction_map(), permuted["report"]])
        assert maps["output_to_source_atom_indices"].tolist() == [5, 1, 2]
        assert maps["source_to_output_atom_indices"].tolist() == [-1, 1, 2, -1, -1, 0]
        assert target.get(element="atom", group_index=True) == [2, 0, 1]
        assert target.get(structure_chemical_state_index=True) == [0, 1, 0]
        assert target.chemical_states.get(chemical_state_index=True) == [0, 1]
        path = str(tmp_path / "declared-axis.h5msm")
        msm.convert(target, to_form=path)
        restored = msm.convert(path, to_form="molsysmt.MolSys")
        assert restored.get(element="atom", atom_id=True) == ["last", "same", "02"]
        assert restored.get(structure_chemical_state_index=True) == [0, 1, 0]
        assert msm.select(
            restored,
            "formal_charge>0",
            structure_indices=[1],
            chemical_state="structure",
        ) == [2]
        assert (
            msm.select(
                restored,
                "formal_charge>0",
                structure_indices=[0],
                chemical_state="structure",
            )
            == []
        )
        np.testing.assert_array_equal(
            puw.get_value(restored.get(coordinates=True), to_unit="nm"),
            before[[2, 0, 2]][:, [5, 1, 2]],
        )
        # Repeated source structure 2 has two target occurrences: an inverse
        # relation is [[1], [], [0, 2]], not a one-to-one integer atom map.
        assert restored.get(n_structures=True) == 3
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), before
    )
    assert source.get(element="atom", group_index=True) == [0, 1, 0, 2, 1, 2]


@pytest.mark.parametrize(
    "field,value",
    [
        ("output_to_source_atom_indices", [1, 2, 6]),
        ("source_to_output_atom_indices", [-1, 1, 0, -1, -1, 2]),
    ],
)
def test_contradictory_or_out_of_range_maps_refuse_without_partial_success(
    field, value
):
    record = declared_extraction_map()
    record[field] = value
    before = copy.deepcopy(record)
    with pytest.raises(StructuralInconsistencyError):
        msm.compose_atom_maps([record])
    assert record == before


def test_omitted_members_are_exposed_and_missing_maps_are_not_identity():
    mapped = msm.compose_atom_maps([declared_extraction_map()])
    assert mapped["source_atom_status"].tolist() == [
        "omitted",
        "retained",
        "retained",
        "omitted",
        "omitted",
        "retained",
    ]
    assert mapped["source_to_output_atom_indices"][[0, 5]].tolist() == [-1, 2]
    with pytest.raises(ArgumentError):
        msm.compose_atom_maps([None])


def test_generated_current_group_member_has_no_original_atom_index():
    builder = msm.MolSysBuilder()
    builder.add_atom(atom_type="C", atom_name="parent")
    builder.set_coordinates(puw.quantity([[[0.0, 0.0, 0.0]]], "nm"))
    original = builder.build()
    result = msm.build.add_terminal_atoms(
        original,
        [{"parent_atom_index": 0, "atom_type": "H"}],
        puw.quantity([[[0.0, 0.0, 0.109]]], "nm"),
    )
    target = result["molecular_system"]
    mapped = msm.compose_atom_maps([result["report"]])
    assert original.get(element="group", selection=[0], atom_index=True) == [[0]]
    assert target.get(element="group", selection=[0], atom_index=True) == [[0, 1]]
    assert mapped["output_to_source_atom_indices"].tolist() == [0, -1]
    assert mapped["generated_output_atom_indices"].tolist() == [1]


def test_counts_and_labels_do_not_establish_unchanged_coordinates(source):
    changed = source.copy()
    msm.set(
        changed,
        selection=[0],
        structure_indices=[2],
        coordinates=puw.quantity([[[99.0, 0.0, 0.0]]], "nm"),
    )
    assert changed.get(n_atoms=True, n_groups=True, n_structures=True) == source.get(
        n_atoms=True, n_groups=True, n_structures=True
    )
    assert changed.get(element="atom", atom_id=True) == source.get(
        element="atom", atom_id=True
    )
    assert not np.array_equal(
        puw.get_value(changed.get(coordinates=True), to_unit="nm"),
        puw.get_value(source.get(coordinates=True), to_unit="nm"),
    )


def test_native_domain_attachment_refuses_mismatched_atoms_before_publication(source):
    before = source.structures
    wrong = Structures()
    wrong.coordinates = puw.quantity(np.zeros((3, 5, 3)), "nm")
    with pytest.raises(StructuralInconsistencyError):
        source.structures = wrong
    assert source.structures is before
