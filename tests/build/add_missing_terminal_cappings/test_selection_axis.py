"""Terminal repair must resolve source atom selections before expansion."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.fixture(scope="module")
def peptide():
    return msm.build.build_peptide("AlaValPro", engine="MolSysMT")


def assert_unchanged(source, before):
    pd.testing.assert_frame_equal(source.topology.atoms, before.topology.atoms)
    pd.testing.assert_frame_equal(source.topology.groups, before.topology.groups)
    pd.testing.assert_frame_equal(
        pd.DataFrame(source.chemical_states.get_bonds()),
        pd.DataFrame(before.chemical_states.get_bonds()),
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(before.structures.coordinates, to_unit="nm"),
    )


@pytest.mark.parametrize("kind", ["list", "array", "mask", "expression", "all"])
def test_full_source_atom_selections_are_equivalent(peptide, kind):
    before = peptide.copy()
    selection = {
        "list": list(range(peptide.get_n_atoms())),
        "array": np.arange(peptide.get_n_atoms()),
        "mask": np.ones(peptide.get_n_atoms(), dtype=bool),
        "expression": "group_index in [0, 1, 2]",
        "all": "all",
    }[kind]
    result = msm.build.add_missing_terminal_cappings(
        peptide, selection=selection, N_terminal="ACE", C_terminal="NME"
    )
    assert result.get_n_atoms() == 52
    assert result.get(element="group", group_name=True) == [
        "ACE",
        "ALA",
        "VAL",
        "PRO",
        "NME",
    ]
    assert_unchanged(peptide, before)


def test_partial_internal_group_is_not_a_chemical_terminus(peptide):
    before = peptide.copy()
    atom = msm.select(peptide, selection="group_index==1")[0]
    result = msm.build.add_missing_terminal_cappings(peptide, selection=[atom])
    assert_unchanged(result, peptide)
    assert_unchanged(peptide, before)


@pytest.mark.parametrize("selection", [[], "group_name=='ABSENT'"])
def test_empty_selection_does_not_add_terminal_atoms(peptide, selection):
    result = msm.build.add_missing_terminal_cappings(
        peptide, selection=selection, N_terminal="ACE", C_terminal="NME"
    )
    assert result is not peptide
    assert_unchanged(result, peptide)


@pytest.mark.parametrize("selection", [[-1], [1000], [1.5], [[0]], [True, 1], None])
def test_invalid_source_atom_selection_preserves_source(peptide, selection):
    before = peptide.copy()
    with pytest.raises(ArgumentError):
        msm.build.add_missing_terminal_cappings(peptide, selection=selection)
    assert_unchanged(peptide, before)


@pytest.mark.parametrize("group", [0, 1])
def test_terminal_assessment_keeps_full_chain_context(peptide, group):
    assert msm.build.get_missing_terminal_cappings(peptide, selection=[group]) == {}


@pytest.mark.parametrize("syntax", ["MolSysMT", "MDTraj"])
def test_numeric_and_boolean_axes_do_not_depend_on_query_syntax(peptide, syntax):
    for selection in [np.arange(peptide.get_n_atoms()), [True] * peptide.get_n_atoms()]:
        result = msm.build.add_missing_terminal_cappings(
            peptide,
            selection=selection,
            syntax=syntax,
            N_terminal="ACE",
            C_terminal="NME",
        )
        assert result.get_n_atoms() == 52


@pytest.mark.parametrize("form", ["molsysmt.MolSys", "mdtraj.Trajectory"])
def test_selection_reaches_only_the_touched_component_after_atom_repair(peptide, form):
    if form == "mdtraj.Trajectory":
        pytest.importorskip("mdtraj")
    source = msm.merge([peptide, peptide], keep_ids=False)
    source = msm.remove(source, selection='group_index==0 and atom_name=="CB"')
    # A repair in the first component moves the original atom position of the
    # second component. Group membership must carry the selection across it.
    selected = msm.select(source, selection="group_index in [0, 3]")
    source = msm.convert(source, to_form=form)
    result = msm.build.add_missing_terminal_cappings(
        source, selection=selected, N_terminal="ACE", C_terminal="NME"
    )
    assert msm.get_form(result) == form
    assert msm.get(result, n_atoms=True) == 104, (
        msm.get(result, element="group", group_name=True),
        msm.get(source, element="component", component_type=True),
        selected,
    )
    assert msm.get(source, n_atoms=True) == 79
    # MDTraj reconstructs molecules from connectivity and cannot store the
    # independently declared native inventory; compare with its own source.
    assert msm.get(result, n_molecules=True) == msm.get(source, n_molecules=True)
    if form == "molsysmt.MolSys":
        assert msm.get(result, n_molecules=True) == 2
    groups = msm.get(result, element="group", group_name=True)
    assert groups == ["ACE", "ALA", "VAL", "PRO", "NME"] * 2


def test_two_structures_and_nondefault_units_keep_local_group_scope(peptide):
    source = msm.append_structures(peptide, peptide, in_place=False)
    before = source.copy()
    selected = msm.select(source, selection="group_index==2")[:1]
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "coulomb"]):
        result = msm.build.add_missing_terminal_cappings(source, selection=selected)
    assert msm.get(result, n_structures=True) == 2
    assert result.get_n_atoms() == source.get_n_atoms() + 1
    assert (
        msm.select(result, selection='group_index==0 and atom_name in ["H2", "H3"]')
        == []
    )
    old_indices = result.topology.atoms.index[result.topology.atoms.atom_name.ne("OXT")]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm")[
            :, old_indices
        ],
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
    )
    assert_unchanged(source, before)


@pytest.mark.parametrize(
    "selection", [np.array([True]), np.zeros((2, 2), bool), [True, 0.0]]
)
def test_invalid_boolean_shape_or_mixed_type_is_rejected(peptide, selection):
    with pytest.raises(ArgumentError):
        msm.build.add_missing_terminal_cappings(peptide, selection=selection)


def test_only_selected_component_receives_caps(peptide):
    source = msm.merge([peptide, peptide], keep_ids=False)
    source = msm.remove(source, selection='group_index==0 and atom_name=="CB"')
    before = source.copy()
    selected = msm.select(source, selection="group_index==3")[:1]
    result = msm.build.add_missing_terminal_cappings(
        source, selection=selected, N_terminal="ACE", C_terminal="NME"
    )
    assert result.get_n_atoms() == 91
    assert result.get(element="group", group_name=True) == [
        "ALA",
        "VAL",
        "PRO",
        "ACE",
        "ALA",
        "VAL",
        "PRO",
        "NME",
    ]
    assert msm.select(result, selection='group_index==0 and atom_name=="CB"') == []
    assert_unchanged(source, before)
