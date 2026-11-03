"""Keep chemical-site structure scope consistent without losing source chemistry."""

from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys

SPATIAL = "atom_index >= 0 within 0.15 nm of atom_index == 0"


def _system():
    builder = msm.MolSysBuilder()
    for index, symbol in enumerate(("O", "H", "H")):
        builder.add_atom(
            atom_id=str(index), atom_name=f"{symbol}{index}", atom_type=symbol
        )
    builder.add_bond(0, 1, bond_type="covalent", bond_order=1)
    builder.add_bond(0, 2, bond_type="covalent", bond_order=1)
    xyz = np.zeros((3, 3, 3))
    xyz[:, :, 0] = [[0, 0.1, 0.5], [0, 0.1, 0.5], [0, 0.5, 0.1]]
    builder.set_coordinates(msm.pyunitwizard.quantity(xyz, "nm"))
    source = builder.build()
    source.chemical_states._states[0].connectivity_completeness = "complete"
    source.chemical_states.append_state()
    source.chemical_states._states[1] = deepcopy(source.chemical_states._states[0])
    source.chemical_states.remove_bonds([1], chemical_state=1)
    source._set_structure_chemical_state_indices([1, 0, 1])
    return source


@pytest.fixture(params=["resident", "h5msm"])
def source(request, tmp_path):
    native = _system()
    if request.param == "resident":
        return native
    path = str(tmp_path / "sites.h5msm")
    msm.convert(native, to_form=path)
    return path


def _assert_sites(result, selected, state):
    expected = [[0, 1], [0, 2]] if state == 0 else [[0, 1]]
    expected = [pair for pair in expected if all(atom in selected for atom in pair)]
    assert result["donor_hydrogen_pairs"].tolist() == expected
    assert result["donor_hydrogen_pairs"].shape == (len(expected), 2)
    assert result["acceptor_atom_indices"].tolist() == ([0] if 0 in selected else [])
    assert result["selected_atom_indices"].tolist() == selected
    assert result["atom_source_indices"].tolist() == [0, 1, 2]
    assert result["chemical_state_index"] == state
    for key in ("donor_hydrogen_pairs", "acceptor_atom_indices", "atom_source_indices"):
        assert result[key].dtype == np.int64


@pytest.mark.parametrize("indices", ["all", None, 0, [2, 0, 2], []])
@pytest.mark.parametrize("state", ["reference", 0, 1])
@pytest.mark.parametrize("selection", ["all", [0, 1], "atom_index <= 1"])
def test_valid_nonspatial_scope_preserves_full_graph_and_source_indices(
    source, indices, state, selection
):
    result = msm.interactions.hbonds.get_hbond_sites(
        source, selection=selection, structure_indices=indices, chemical_state=state
    )
    selected = [0, 1, 2] if selection == "all" else [0, 1]
    _assert_sites(result, selected, 1 if state == 1 else 0)


@pytest.mark.parametrize("indices", [[-1], [3], [0.5], [True], [[0]], "bad", 1.2])
@pytest.mark.parametrize("state", ["reference", 1, "structure"])
@pytest.mark.parametrize("selection", ["all", "atom_index >= 0", SPATIAL])
def test_invalid_structure_scope_is_rejected_for_every_selection_and_state(
    source, indices, state, selection
):
    with pytest.raises(ArgumentError, match="structure_indices"):
        msm.interactions.hbonds.get_hbond_sites(
            source, selection=selection, structure_indices=indices, chemical_state=state
        )


@pytest.mark.parametrize("indices,selected", [(0, [0, 1]), ([2, 0, 2], [0, 2])])
@pytest.mark.parametrize("state", ["reference", 1, "structure"])
def test_spatial_selection_uses_the_requested_source_structures(
    source, indices, selected, state
):
    result = msm.interactions.hbonds.get_hbond_sites(
        source, selection=SPATIAL, structure_indices=indices, chemical_state=state
    )
    _assert_sites(result, selected, 0 if state == "reference" else 1)


@pytest.mark.parametrize("indices", ["all", None])
def test_none_and_all_preserve_the_selector_first_structure_convention(source, indices):
    result = msm.interactions.hbonds.get_hbond_sites(
        source, selection=SPATIAL, structure_indices=indices
    )
    _assert_sites(result, [0, 1], 0)


@pytest.mark.parametrize("indices", [[], [2, 1], "all", None])
def test_structure_assigned_sites_require_one_known_state(source, indices):
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_sites(
            source, structure_indices=indices, chemical_state="structure"
        )


def test_empty_spatial_scope_is_rejected_instead_of_using_an_unrequested_structure(
    source,
):
    with pytest.raises(ArgumentError):
        msm.interactions.hbonds.get_hbond_sites(
            source, selection=SPATIAL, structure_indices=[]
        )


@pytest.mark.parametrize("indices", ["all", None])
@pytest.mark.parametrize("form", ["resident", "h5msm"])
def test_coordinate_free_site_recognition_remains_available(tmp_path, indices, form):
    native = _system()
    source = MolSys._from_partial_domains(
        topology=native.topology.copy(), chemical_states=native.chemical_states.copy()
    )
    if form == "h5msm":
        path = str(tmp_path / "chemical.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.hbonds.get_hbond_sites(source, structure_indices=indices)
    _assert_sites(result, [0, 1, 2], 0)
    with pytest.raises(ArgumentError, match="structure_indices"):
        msm.interactions.hbonds.get_hbond_sites(source, structure_indices=[0])


def test_index_site_queries_never_read_h5_structures(tmp_path, monkeypatch):
    from molsysmt.form import _h5msm05_modular

    path = str(tmp_path / "sites.h5msm")
    msm.convert(_system(), to_form=path)

    def reject(*args, **kwargs):
        raise AssertionError("Index-only recognition must not read structural series.")

    monkeypatch.setattr(_h5msm05_modular, "read_independent_structures", reject)
    result = msm.interactions.hbonds.get_hbond_sites(path, structure_indices=[2, 0, 2])
    _assert_sites(result, [0, 1, 2], 0)


def test_h5_spatial_context_reads_only_the_requested_rows(tmp_path, monkeypatch):
    from molsysmt.form import _h5msm05_modular

    path = str(tmp_path / "sites.h5msm")
    msm.convert(_system(), to_form=path)
    original = _h5msm05_modular.read_independent_structures
    scopes = []

    def observed(root, *, structure_indices=None, **kwargs):
        scopes.append(np.asarray(structure_indices).tolist())
        return original(root, structure_indices=structure_indices, **kwargs)

    monkeypatch.setattr(_h5msm05_modular, "read_independent_structures", observed)
    result = msm.interactions.hbonds.get_hbond_sites(
        path, selection=SPATIAL, structure_indices=[2, 0, 2], chemical_state="structure"
    )
    _assert_sites(result, [0, 2], 1)
    assert scopes == [[2, 0, 2]]


def test_success_and_failure_leave_resident_domains_and_state_associations_unchanged():
    source = _system()
    states = source.chemical_states
    records = [
        (state.bonds.copy(deep=True), state.atom_attributes.copy(deep=True))
        for state in states._states
    ]
    atoms = source.topology.atoms.copy(deep=True)
    xyz = msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm").copy()
    for indices in (0, [2, 0, 2], [-1], [3], []):
        try:
            msm.interactions.hbonds.get_hbond_sites(
                source, selection=SPATIAL, structure_indices=indices, chemical_state=1
            )
        except ArgumentError:
            assert indices in ([-1], [3], [])
    assert states.reference_chemical_state_index == 0
    assert source._get_structure_chemical_state_indices(resolved=True).tolist() == [
        1,
        0,
        1,
    ]
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    for state, (bonds, attributes) in zip(states._states, records, strict=True):
        pd.testing.assert_frame_equal(state.bonds, bonds)
        pd.testing.assert_frame_equal(state.atom_attributes, attributes)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"), xyz
    )


@pytest.mark.parametrize("form", ["resident", "h5msm"])
def test_coordinate_free_spatial_queries_require_coordinates(tmp_path, form):
    native = _system()
    source = MolSys._from_partial_domains(
        topology=native.topology.copy(), chemical_states=native.chemical_states.copy()
    )
    if form == "h5msm":
        path = str(tmp_path / "chemical.h5msm")
        msm.convert(source, to_form=path)
        source = path
    result = msm.interactions.hbonds.get_hbond_sites(
        source, selection="atom_index <= 1"
    )
    _assert_sites(result, [0, 1], 0)
    with pytest.raises(ArgumentError, match="requires source coordinates"):
        msm.interactions.hbonds.get_hbond_sites(source, selection=SPATIAL)
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_sites(source, chemical_state="structure")


def test_spatial_scope_survives_nondefault_length_units(source):
    with msm.pyunitwizard.context(standard_units=["angstrom", "ps"]):
        result = msm.interactions.hbonds.get_hbond_sites(
            source, selection=SPATIAL, structure_indices=[2, 0, 2]
        )
        _assert_sites(result, [0, 2], 0)


def test_ambiguous_h5_state_rejects_before_any_structural_read(tmp_path, monkeypatch):
    from molsysmt.form import _h5msm05_modular

    path = str(tmp_path / "sites.h5msm")
    msm.convert(_system(), to_form=path)

    def reject(*args, **kwargs):
        raise AssertionError(
            "Resolve ambiguous state metadata before reading coordinates."
        )

    monkeypatch.setattr(_h5msm05_modular, "read_independent_structures", reject)
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_sites(
            path, selection=SPATIAL, chemical_state="structure"
        )


@pytest.mark.parametrize("form", ["resident", "h5msm"])
def test_unknown_structure_state_does_not_fall_back_to_reference(tmp_path, form):
    source = _system()
    source._set_structure_chemical_state_indices([1, None, 1])
    if form == "h5msm":
        path = str(tmp_path / "unknown.h5msm")
        msm.convert(source, to_form=path)
        source = path
    with pytest.raises(StructuralInconsistencyError):
        msm.interactions.hbonds.get_hbond_sites(
            source, structure_indices=[1], chemical_state="structure"
        )
    result = msm.interactions.hbonds.get_hbond_sites(
        source, structure_indices=[2, 0, 2], chemical_state="structure"
    )
    _assert_sites(result, [0, 1, 2], 1)
