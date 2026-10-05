"""Checking exact template candidates against literal independent edge inventories."""

import builtins
from copy import deepcopy

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError


def _source(groups=None, n_structures=1):
    groups = (
        [("ALA", ["N", "CA", "C", "O", "CB"], ["N", "C", "C", "O", "C"])]
        if groups is None
        else groups
    )
    builder = msm.MolSysBuilder()
    n_atoms = 0
    for name, names, elements in groups:
        atoms = [
            builder.add_atom(atom_name=atom_name, atom_type=element)
            for atom_name, element in zip(names, elements)
        ]
        builder.add_group(atoms, group_name=name)
        n_atoms += len(atoms)
    if n_structures:
        builder.set_coordinates(
            puw.quantity(np.zeros((n_structures, n_atoms, 3)), "nm")
        )
    return builder.build()


ALA_PAIRS = [[0, 1], [1, 2], [1, 4], [2, 3]]


def test_exact_pairs_provenance_and_detached_nonmutation():
    source = _source()
    atoms = source.topology.atoms.copy(deep=True)
    bonds = source.topology.bonds.copy(deep=True)
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == ALA_PAIRS
    assert report["group_indices"].tolist() == [0] * 4
    assert report["missing_mask"].tolist() == [True] * 4
    assert report["bonded_atom_pairs"].dtype == np.int64
    assert report["missing_mask"].dtype == np.bool_
    assert report["evidence"] == "inferred_candidate"
    assert report["method"] == "exact_heavy_group_templates"
    assert report["schema"] == "molsysmt.covalent_bond_candidates@1"
    assert report["software"]["molsysmt"]
    assert len(report["groups"][0]["template"]["provenance"]["packaged_sha256"]) == 64
    assert {"hydrogen_edges", "inter_group_links", "protonation", "valence"} <= set(
        report["unassessed_checks"]
    )
    report["bonded_atom_pairs"][:] = -1
    report["groups"][0]["template"]["provenance"].clear()
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    pd.testing.assert_frame_equal(source.topology.bonds, bonds)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), coordinates
    )


def test_existing_edges_have_an_aligned_missing_mask():
    source = _source()
    source.topology.add_bonds([[1, 4]])
    msm.set(source, element="bond", bond_type="covalent")
    report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == ALA_PAIRS
    assert report["missing_mask"].tolist() == [True, True, False, True]
    assert msm.get(source, bonded_atom_pairs=True) == [[1, 4]]


@pytest.mark.parametrize(
    "selection, expected",
    [([4, 1, 4], [[1, 4]]), ("atom_index in [1, 4]", [[1, 4]]), ([0], []), ([], [])],
)
def test_atom_selection_keeps_source_indices_and_both_endpoints(selection, expected):
    report = msm.build.get_covalent_bond_candidates(_source(), selection=selection)
    assert report["bonded_atom_pairs"].tolist() == expected
    assert report["bonded_atom_pairs"].shape == (len(expected), 2)
    assert report["group_indices"].shape == (len(expected),)
    assert report["missing_mask"].shape == (len(expected),)


def test_missing_atom_leaves_only_mapped_pairs_and_a_partial_group():
    source = _source([("ALA", ["N", "CA", "C", "O"], ["N", "C", "C", "O"])])
    report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == [[0, 1], [1, 2], [2, 3]]
    assert report["groups"][0]["status"] == "partial"
    assert report["groups"][0]["blocked_by_missing_atom_name_pairs"] == [["CA", "CB"]]


@pytest.mark.parametrize(
    "name, names, elements, reason",
    [
        (
            "ALA",
            ["N", "CA", "C", "O", "CB", "CB"],
            ["N", "C", "C", "O", "C", "C"],
            "ambiguous_atom_names",
        ),
        (
            "ALA",
            ["N", "CA", "C", "O", "XX"],
            ["N", "C", "C", "O", "C"],
            "unexpected_heavy_atoms",
        ),
        (
            "ALA",
            ["N", "CA", "C", "O", "CB"],
            ["N", "C", "C", "N", "C"],
            "heavy_element_conflict",
        ),
        ("LIG", ["C1", "C2"], ["C", "C"], "no_exact_group_template"),
        ("HOH", ["O", "H1", "H2"], ["O", "H", "H"], "no_exact_group_template"),
        ("ZN", ["ZN"], ["Zn"], "no_exact_group_template"),
    ],
)
def test_unsupported_or_conflicting_groups_are_explicit(name, names, elements, reason):
    report = msm.build.get_covalent_bond_candidates(_source([(name, names, elements)]))
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert report["groups"][0]["status"] == "unassessed"
    assert report["groups"][0]["group_name"] == name
    assert reason in report["groups"][0]["reason_codes"]


def test_contradictory_stored_intragroup_edge_blocks_candidates():
    source = _source()
    source.topology.add_bonds([[0, 4]])
    msm.set(source, element="bond", bond_type="covalent")
    report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert report["groups"][0]["reason_codes"] == ["conflicting_stored_chemistry"]
    assert msm.get(source, bonded_atom_pairs=True) == [[0, 4]]


def test_modified_group_uses_its_own_template_and_selenium():
    source = _source(
        [
            (
                "MSE",
                ["N", "CA", "C", "O", "CB", "CG", "SE", "CE"],
                ["N", "C", "C", "O", "C", "C", "Se", "C"],
            )
        ]
    )
    report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == [*ALA_PAIRS, [4, 5], [5, 6], [6, 7]]
    assert report["groups"][0]["template"]["group_name"] == "MSE"
    assert "MSE.json" in report["groups"][0]["template"]["resource"]


@pytest.mark.parametrize("structure_index", [0, 1])
def test_structure_indices_are_not_structure_ids(structure_index):
    source = _source(n_structures=2)
    source.structures.structure_id = ["10", "200"]
    report = msm.build.get_covalent_bond_candidates(
        source, structure_indices=structure_index
    )
    assert report["structure_index"] == structure_index
    assert report["bonded_atom_pairs"].tolist() == ALA_PAIRS


def test_multiple_structures_require_an_explicit_index():
    with pytest.raises(ArgumentError):
        msm.build.get_covalent_bond_candidates(_source(n_structures=2))


def test_topology_without_structures_is_assessed_without_fabricated_geometry():
    report = msm.build.get_covalent_bond_candidates(_source(n_structures=0).topology)
    assert report["structure_index"] is None
    assert report["bonded_atom_pairs"].tolist() == ALA_PAIRS


@pytest.mark.parametrize("input_form", ["modular_file", "legacy_file", "handler"])
def test_native_h5msm_matches_the_same_source_atom_axis(tmp_path, input_form):
    source = _source(n_structures=2)
    filename = str(tmp_path / "candidates.h5msm")
    handler_input = input_form == "handler"
    if input_form != "modular_file":
        from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm
        from molsysmt.native import H5MSMFileHandler

        # The native handler owns the legacy schema; public writes use 0.5.
        to_file_h5msm(source, output_filename=filename)
        item = H5MSMFileHandler(filename) if handler_input else filename
    else:
        msm.convert(source, to_form=filename)
        item = filename
    try:
        report = msm.build.get_covalent_bond_candidates(
            item, selection=[1, 4], structure_indices=1
        )
        if handler_input:
            assert item.file.id.valid
    finally:
        if handler_input:
            item.close()
    assert report["bonded_atom_pairs"].tolist() == [[1, 4]]
    assert report["structure_index"] == 1
    assert report["n_atoms"] == 5


@pytest.mark.parametrize("file_input", [False, True])
def test_state_association_and_missing_association_remain_explicit(
    file_input, tmp_path, monkeypatch
):
    source = _source(n_structures=3)
    source.chemical_states.append_state()
    source.chemical_states._set_reference_index(None)
    msm.set(source, element="system", structure_chemical_state_index=[0, 1, None])
    if file_input:
        filename = str(tmp_path / "states.h5msm")
        msm.convert(source, to_form=filename)
        source = filename
        from molsysmt.form import _h5msm05_modular

        def reject_full_read(*args, **kwargs):
            pytest.fail("Numeric candidate queries must not materialize the trajectory")

        monkeypatch.setattr(
            _h5msm05_modular, "read_independent_structures", reject_full_read
        )
    resolved = msm.build.get_covalent_bond_candidates(
        source, selection=[1, 4], structure_indices=1, chemical_state="structure"
    )
    assert resolved["chemical_state_index"] == 1
    assert resolved["bonded_atom_pairs"].tolist() == [[1, 4]]
    unresolved = msm.build.get_covalent_bond_candidates(
        source, structure_indices=2, chemical_state="structure"
    )
    assert unresolved["bonded_atom_pairs"].shape == (0, 2)
    assert unresolved["groups"][0]["reason_codes"] == ["chemical_state_unassociated"]
    ambiguous = msm.build.get_covalent_bond_candidates(source, structure_indices=0)
    assert ambiguous["groups"][0]["reason_codes"] == ["chemical_state_ambiguous"]


@pytest.mark.parametrize(
    "kwargs",
    [
        {"selection": [-1]},
        {"selection": [5]},
        {"selection": [True]},
        {"chemical_state": "guess"},
        {"structure_indices": [1]},
        {"skip_digestion": "yes"},
    ],
)
def test_public_argument_validation(kwargs):
    with pytest.raises(ArgumentError):
        msm.build.get_covalent_bond_candidates(_source(), **kwargs)


def test_pdb_candidate_generation_never_imports_openmm(tmp_path, monkeypatch):
    filename = str(tmp_path / "ala.pdb")
    msm.convert(_source(), to_form=filename)
    original = builtins.__import__

    def reject_openmm(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("The native template method attempted an OpenMM import")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_openmm)
    assert (
        msm.build.get_covalent_bond_candidates(filename)["bonded_atom_pairs"].tolist()
        == ALA_PAIRS
    )


def test_nondefault_length_policy_preserves_candidates_and_coordinates():
    source = _source()
    before = deepcopy(source.structures.coordinates)
    with puw.context(standard_units=["pm", "ps"]):
        report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == ALA_PAIRS
    assert puw.are_close(source.structures.coordinates, before)
