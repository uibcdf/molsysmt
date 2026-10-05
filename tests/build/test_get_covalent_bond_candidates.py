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

HYDROGEN_METHOD = "observed_hydrogen_template_consensus"


def _hydrogen_source(extra_names=("H", "HA", "HB1", "HB2", "HB3"), n_structures=1):
    return _source(
        [
            (
                "ALA",
                ["N", "CA", "C", "O", "CB", *extra_names],
                ["N", "C", "C", "O", "C", *(["H"] * len(extra_names))],
            )
        ],
        n_structures=n_structures,
    )


def test_observed_hydrogen_consensus_has_literal_pairs_roles_and_detached_evidence():
    source = _hydrogen_source()
    before = source.topology.atoms.copy(deep=True)
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    default = msm.build.get_covalent_bond_candidates(source)
    assert default["bonded_atom_pairs"].tolist() == ALA_PAIRS
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].tolist() == [
        [0, 5],
        [1, 6],
        [4, 7],
        [4, 8],
        [4, 9],
    ]
    assert report["missing_mask"].tolist() == [True] * 5
    assert report["group_indices"].tolist() == [0] * 5
    h = report["groups"][0]["hydrogen_coverage"]
    assert h["atom_indices"].tolist() == [5, 6, 7, 8, 9]
    assert h["parent_atom_indices"].tolist() == [0, 1, 4, 4, 4]
    assert h["eligible_mask"].tolist() == [True] * 5
    assert h["selected_mask"].tolist() == [True] * 5
    assert h["inventory_status"] == "compatible_subset"
    assert h["variant_offsets"].shape == (6,)
    assert h["variant_offsets"][0] == 0
    assert h["variant_offsets"][-1] == len(h["variant_indices"])
    assert h["issues"] == []
    assert report["method"] == HYDROGEN_METHOD
    assert "hydrogen_inventory_completeness" in report["unassessed_checks"]
    assert "hydrogen_placement" in report["unassessed_checks"]
    h["parent_atom_indices"][:] = -1
    report["groups"][0]["template"]["provenance"].clear()
    pd.testing.assert_frame_equal(source.topology.atoms, before)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), coordinates
    )
    assert source.topology.n_bonds == 0


@pytest.mark.parametrize(
    "selection,expected",
    [([6, 1, 6], [[1, 6]]), ([6], []), ([], []), ("atom_index in [1, 6]", [[1, 6]])],
)
def test_hydrogen_method_keeps_source_indices_and_both_selected_endpoints(
    selection, expected
):
    report = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(), selection=selection, method=HYDROGEN_METHOD
    )
    assert report["bonded_atom_pairs"].tolist() == expected
    assert report["bonded_atom_pairs"].shape == (len(expected), 2)
    assert report["bonded_atom_pairs"].dtype == np.int64
    assert report["missing_mask"].dtype == np.bool_


def test_unknown_hydrogen_names_are_sparse_issues_without_guessing_aliases():
    report = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(("H", "HN1", "XX")), method=HYDROGEN_METHOD
    )
    assert report["bonded_atom_pairs"].tolist() == [[0, 5]]
    h = report["groups"][0]["hydrogen_coverage"]
    assert h["parent_atom_indices"].tolist() == [0, -1, -1]
    assert h["eligible_mask"].tolist() == [True, False, False]
    assert [entry["atom_index"] for entry in h["issues"]] == [6, 7]
    assert all(
        "unrecognized_hydrogen_name" in entry["reason_codes"] for entry in h["issues"]
    )
    assert h["inventory_status"] == "unassessed"
    assert report["groups"][0]["status"] == "partial"


def test_missing_heavy_parent_is_reported_without_attaching_to_a_nearby_atom():
    source = _source([("ALA", ["N", "CA", "C", "O", "HB1"], ["N", "C", "C", "O", "H"])])
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    issue = report["groups"][0]["hydrogen_coverage"]["issues"][0]
    assert issue["reference_parent_names"] == ["CB"]
    assert "missing_hydrogen_parent" in issue["reason_codes"]


def test_hydrogen_labeled_as_a_heavy_reference_atom_is_rejected():
    source = _source([("ALA", ["N", "CA", "C", "O", "CB"], ["N", "C", "C", "H", "C"])])
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (
        "hydrogen_reference_element_conflict"
        in report["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


@pytest.mark.parametrize(
    "kind,order,expected",
    [
        (None, None, True),
        ("covalent", 1, True),
        ("dative", None, False),
        ("covalent", 2, False),
    ],
)
def test_stored_hydrogen_edges_have_missing_masks_and_reject_type_order_conflicts(
    kind, order, expected
):
    source = _hydrogen_source(("H",))
    source.topology.add_bonds([[0, 5]])
    msm.set(source, element="bond", bond_type=kind, bond_order=order)
    before = source.topology.bonds.copy(deep=True)
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].tolist() == ([[0, 5]] if expected else [])
    if expected:
        assert report["missing_mask"].tolist() == [False]
    else:
        assert report["groups"][0]["hydrogen_coverage"]["issues"]
    pd.testing.assert_frame_equal(source.topology.bonds, before)


@pytest.mark.parametrize(
    "field,value",
    [
        ("formal_charge", 1),
        ("n_unpaired_electrons", 1),
        ("n_implicit_hydrogens", 1),
        ("n_explicit_hydrogens", 1),
        ("atom_is_aromatic", True),
    ],
)
def test_nonstandard_stored_hydrogen_assignments_are_not_overwritten(field, value):
    source = _hydrogen_source(("H",))
    msm.set(source, element="atom", selection=[5], **{field: value})
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (
        "nonstandard_stored_hydrogen_assignment"
        in report["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )
    assert msm.get(source, element="atom", selection=[5], **{field: True}) == [value]


@pytest.mark.parametrize("extra_partner", [1, 6])
def test_declared_other_hydrogen_partner_blocks_candidates_including_across_groups(
    extra_partner,
):
    source = _source(
        [
            ("ALA", ["N", "CA", "C", "O", "CB", "H"], ["N", "C", "C", "O", "C", "H"]),
            ("ALA", ["N", "CA", "C", "O", "CB"], ["N", "C", "C", "O", "C"]),
        ]
    )
    source.topology.add_bonds([[5, extra_partner]])
    report = msm.build.get_covalent_bond_candidates(
        source, selection=[0, 5], method=HYDROGEN_METHOD
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (
        "conflicting_stored_hydrogen_partner"
        in report["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


@pytest.mark.parametrize("method", [None, "unknown", 7])
def test_candidate_method_is_validated(method):
    with pytest.raises(ArgumentError):
        msm.build.get_covalent_bond_candidates(_source(), method=method)


def test_hydrogen_candidates_do_not_require_geometry_and_empty_arrays_are_typed():
    report = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(n_structures=0).topology, method=HYDROGEN_METHOD
    )
    assert report["structure_index"] is None
    assert report["bonded_atom_pairs"].tolist() == [
        [0, 5],
        [1, 6],
        [4, 7],
        [4, 8],
        [4, 9],
    ]
    empty = msm.build.get_covalent_bond_candidates(_source(), method=HYDROGEN_METHOD)
    assert empty["bonded_atom_pairs"].shape == (0, 2)
    h = empty["groups"][0]["hydrogen_coverage"]
    for name in ("atom_indices", "parent_atom_indices", "variant_indices"):
        assert h[name].shape == (0,)
        assert h[name].dtype == np.int64
    assert h["variant_offsets"].tolist() == [0]


@pytest.mark.parametrize("reference_change", ["different_parent", "missing_edge"])
def test_all_matching_variants_must_agree_on_one_hydrogen_parent(
    monkeypatch, reference_change
):
    from molsysmt._private import residue_chemical_coverage as reference

    original = reference._template

    def contradictory_reference(name, names, cache):
        template = deepcopy(original(name, names, cache))
        if name == "ALA":
            # Synthetic conflicting reference: reject a first-variant shortcut.
            variant = template["candidates"][0][1]
            variant["bonds"] = [pair for pair in variant["bonds"] if "H" not in pair]
            if reference_change == "different_parent":
                variant["bonds"].append(["H", "CB"])
        return template

    monkeypatch.setattr(reference, "_template", contradictory_reference)
    report = msm.build.get_covalent_bond_candidates(
        _hydrogen_source(("H",)), method=HYDROGEN_METHOD
    )
    assert report["bonded_atom_pairs"].shape == (0, 2)
    issue = report["groups"][0]["hydrogen_coverage"]["issues"][0]
    assert "ambiguous_hydrogen_parent" in issue["reason_codes"]


def test_unknown_hydrogen_element_is_not_inferred_from_its_name():
    source = _hydrogen_source(("H",))
    source.topology.atoms.at[5, "atom_type"] = None
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (
        "hydrogen_element_unassessed"
        in report["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


def test_aromatic_hydrogen_bond_is_not_silently_replaced_with_a_single_bond():
    source = _hydrogen_source(("H",))
    source.topology.add_bonds([[0, 5]])
    msm.set(
        source,
        element="bond",
        bond_type="covalent",
        bond_order=1,
        bond_is_aromatic=True,
    )
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert (
        "conflicting_stored_hydrogen_bond_order"
        in report["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


def test_modified_heavy_only_template_does_not_invent_hydrogen_reference():
    source = _source(
        [
            (
                "MSE",
                ["N", "CA", "C", "O", "CB", "CG", "SE", "CE", "H"],
                ["N", "C", "C", "O", "C", "C", "Se", "C", "H"],
            )
        ]
    )
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert report["groups"][0]["template"]["group_name"] == "MSE"
    assert (
        "heavy_only_template"
        in report["groups"][0]["hydrogen_coverage"]["issues"][0]["reason_codes"]
    )


def test_local_parent_consensus_does_not_claim_a_joint_inventory_template():
    source = _hydrogen_source(("H", "HN2", "HB1"))
    report = msm.build.get_covalent_bond_candidates(source, method=HYDROGEN_METHOD)
    assert report["bonded_atom_pairs"].tolist() == [[0, 5], [0, 6], [4, 7]]
    h = report["groups"][0]["hydrogen_coverage"]
    assert h["eligible_mask"].tolist() == [True, True, True]
    assert h["inventory_status"] == "unassessed"
    assert h["joint_variant_indices"].size == 0
    assert report["groups"][0]["status"] == "partial"


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


@pytest.mark.parametrize("method", ["exact_heavy_group_templates", HYDROGEN_METHOD])
def test_pdb_candidate_generation_never_imports_openmm(tmp_path, monkeypatch, method):
    filename = str(tmp_path / "ala.pdb")
    msm.convert(_hydrogen_source(), to_form=filename)
    original = builtins.__import__

    def reject_openmm(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("The native template method attempted an OpenMM import")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_openmm)
    expected = (
        ALA_PAIRS
        if method == "exact_heavy_group_templates"
        else [[0, 5], [1, 6], [4, 7], [4, 8], [4, 9]]
    )
    report = msm.build.get_covalent_bond_candidates(filename, method=method)
    assert report["bonded_atom_pairs"].tolist() == expected


def test_hydrogen_h5msm_queries_keep_bounded_structure_and_state_access(
    tmp_path, monkeypatch
):
    source = _hydrogen_source(n_structures=3)
    source.chemical_states.append_state()
    source.chemical_states._set_reference_index(None)
    msm.set(source, element="system", structure_chemical_state_index=[0, 1, None])
    filename = str(tmp_path / "hydrogens.h5msm")
    msm.convert(source, to_form=filename)
    from molsysmt.form import _h5msm05_modular

    def reject_full_read(*args, **kwargs):
        pytest.fail("H candidate queries must not materialize the trajectory")

    monkeypatch.setattr(
        _h5msm05_modular, "read_independent_structures", reject_full_read
    )
    with puw.context(standard_units=["pm", "ps"]):
        report = msm.build.get_covalent_bond_candidates(
            filename,
            selection=[6, 1],
            structure_indices=1,
            chemical_state="structure",
            method=HYDROGEN_METHOD,
        )
    assert report["bonded_atom_pairs"].tolist() == [[1, 6]]
    assert report["chemical_state_index"] == 1
    assert report["structure_index"] == 1
    unresolved = msm.build.get_covalent_bond_candidates(
        filename,
        structure_indices=2,
        chemical_state="structure",
        method=HYDROGEN_METHOD,
    )
    assert unresolved["bonded_atom_pairs"].shape == (0, 2)
    assert "chemical_state_unassociated" in unresolved["groups"][0]["reason_codes"]


def test_nondefault_length_policy_preserves_candidates_and_coordinates():
    source = _source()
    before = deepcopy(source.structures.coordinates)
    with puw.context(standard_units=["pm", "ps"]):
        report = msm.build.get_covalent_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == ALA_PAIRS
    assert puw.are_close(source.structures.coordinates, before)
