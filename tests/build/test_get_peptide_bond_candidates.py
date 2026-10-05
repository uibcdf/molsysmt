"""Protecting source-aware peptide proposals against literal structural cases."""

import builtins

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt._private.smonitor import ArgumentError
from molsysmt.native import Structures


def _pdb(
    chains=("A", "A"),
    *,
    breaks=(),
    group_ids=None,
    insertion_codes=None,
    alternate=False,
):
    lines = []
    serial = 0
    for group, chain in enumerate(chains):
        center = 3.4 * group
        positions = (
            (center - 2, 0, 0),
            (center - 1, 0, 0),
            (center, 0, 0),
            (center, 1.2, 0),
            (center - 1, 0, 1.5),
        )
        for name, (x, y, z) in zip(("N", "CA", "C", "O", "CB"), positions):
            labels = ("A", "B") if alternate and group == 0 and name == "C" else (" ",)
            for label in labels:
                serial += 1
                gid = group + 1 if group_ids is None else group_ids[group]
                code = " " if insertion_codes is None else insertion_codes[group]
                lines.append(
                    f"ATOM  {serial:5d} {name:^4}{label}ALA {chain}{gid:4d}{code}   {x:8.3f}{y:8.3f}{z:8.3f}{1.0:6.2f}{0.0:6.2f}          {name[0]:>2}  "
                )
        if group in breaks:
            lines.append("TER")
    return "\n".join([*lines, "END", ""])


def _source(**kwargs):
    return msm.convert(
        _pdb(**kwargs), to_form="molsysmt.MolSys", get_missing_bonds=False
    )


def test_adjacent_pair_roles_units_provenance_and_source_immutability():
    source = _source()
    atoms = source.topology.atoms.copy(deep=True)
    bonds = source.topology.bonds.copy(deep=True)
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["schema"] == "molsysmt.peptide_bond_candidates@1"
    assert report["method"] == "adjacent_backbone_distance"
    assert report["bonded_atom_pairs"].tolist() == [[2, 5]]
    assert report["group_pairs"].tolist() == [[0, 1]]
    assert report["carbon_atom_indices"].tolist() == [2]
    assert report["nitrogen_atom_indices"].tolist() == [5]
    assert report["missing_mask"].tolist() == [True]
    assert report["evidence"] == "inferred_candidate"
    assert report["software"]["molsysmt"]
    np.testing.assert_allclose(
        puw.get_value(report["distances"], to_unit="angstrom"), [1.4]
    )
    assert puw.get_value(
        report["parameters"]["effective_max_bond_length"], to_unit="nm"
    ) == pytest.approx(0.153)
    report["bonded_atom_pairs"][:] = -1
    report["group_coverage"]["groups"][0]["template"]["provenance"].clear()
    pd.testing.assert_frame_equal(source.topology.atoms, atoms)
    pd.testing.assert_frame_equal(source.topology.bonds, bonds)
    np.testing.assert_array_equal(
        puw.get_value(source.structures.coordinates, to_unit="nm"), coordinates
    )


@pytest.mark.parametrize("kwargs", [{"chains": ("A", "B")}, {"breaks": (0,)}])
def test_different_chains_and_same_label_ter_segments_are_excluded(kwargs):
    source = _source(**kwargs)
    assert msm.get(source, element="group", chain_index=True) == [0, 1]
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "different_source_chains" in report["links"][0]["reason_codes"]


def test_insertion_code_sites_remain_distinct_despite_equal_group_id():
    source = _source(group_ids=[10, 10], insertion_codes=[" ", "A"])
    assert msm.get(source, element="group", group_id=True) == ["10", "10"]
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == [[2, 5]]
    assert report["group_pairs"].tolist() == [[0, 1]]


def test_group_ids_are_labels_and_do_not_define_adjacency():
    report = msm.build.get_peptide_bond_candidates(_source(group_ids=[10, 200]))
    assert report["bonded_atom_pairs"].tolist() == [[2, 5]]


@pytest.mark.parametrize("selection", [[2, 10], "group_index in [0, 2]"])
def test_selection_gap_does_not_create_a_polymer_link(selection):
    source = _source(chains=("A", "A", "A"))
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    coordinates[0, 10, 0] = 0.14
    msm.set(source, coordinates=puw.quantity(coordinates, "nm"))
    report = msm.build.get_peptide_bond_candidates(source, selection=selection)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "nonconsecutive_source_groups" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize(
    "selection, expected",
    [([5, 2, 5], [[2, 5]]), ([2], []), ([], []), ("atom_index in [2, 5]", [[2, 5]])],
)
def test_atom_selection_requires_both_endpoints_and_preserves_typed_empties(
    selection, expected
):
    report = msm.build.get_peptide_bond_candidates(_source(), selection=selection)
    assert report["bonded_atom_pairs"].tolist() == expected
    assert report["bonded_atom_pairs"].shape == (len(expected), 2)
    assert report["group_pairs"].shape == (len(expected), 2)
    assert report["carbon_atom_indices"].shape == (len(expected),)
    assert report["bonded_atom_pairs"].dtype == np.int64
    assert report["missing_mask"].dtype == np.bool_
    assert puw.get_value(report["distances"], to_unit="nm").shape == (len(expected),)


@pytest.mark.parametrize(
    "chain_values", [[None] * 5 + [0] * 5, [0, 0, 0, 0, 1] + [0] * 5]
)
def test_missing_and_ambiguous_chain_membership_remain_unassessed(chain_values):
    source = _source()
    msm.set(
        source, element="atom", selection=list(range(5)), chain_index=chain_values[:5]
    )
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "missing_or_ambiguous_chain" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize("file_input", [False, True])
def test_alternate_backbone_sites_are_not_combined(tmp_path, file_input):
    source = _source(alternate=True)
    if file_input:
        filename = str(tmp_path / "alternate.h5msm")
        msm.convert(source, to_form=filename)
        source = filename
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "alternate_backbone_endpoint" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize(
    "kind, order, candidate",
    [
        ("covalent", 1, True),
        ("covalent", None, True),
        ("dative", None, False),
        ("covalent", 2, False),
    ],
)
def test_existing_peptide_edge_is_preserved_and_contradictions_block_candidates(
    kind, order, candidate
):
    source = _source()
    source.topology.add_bonds([[2, 5]])
    msm.set(source, element="bond", bond_type=kind, bond_order=order)
    before = source.topology.bonds.copy(deep=True)
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == ([[2, 5]] if candidate else [])
    if candidate:
        assert report["missing_mask"].tolist() == [False]
    else:
        assert "conflicting_stored_peptide_edge" in report["links"][0]["reason_codes"]
    pd.testing.assert_frame_equal(source.topology.bonds, before)


def test_backbone_endpoint_with_another_declared_external_partner_is_blocked():
    source = _source(chains=("A", "A", "A"))
    source.topology.add_bonds([[2, 10]])
    msm.set(source, element="bond", bond_type="covalent")
    report = msm.build.get_peptide_bond_candidates(source)
    assert [2, 5] not in report["bonded_atom_pairs"].tolist()
    assert "backbone_endpoint_already_linked" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize("file_input", [False, True])
@pytest.mark.parametrize("structure_index", [0, 1])
def test_structure_indices_and_state_association_use_one_bounded_structure(
    tmp_path, monkeypatch, file_input, structure_index
):
    source = _source()
    first = puw.get_value(source.structures.coordinates, to_unit="nm")[0]
    second = first.copy()
    second[5, 0] = 0.8
    source.structures = Structures(
        coordinates=puw.quantity(np.stack([first, second]), "nm"),
        structure_id=["10", "200"],
    )
    if file_input:
        filename = str(tmp_path / "selected.h5msm")
        msm.convert(source, to_form=filename)
        source = filename
        from molsysmt.form import _h5msm05_modular

        def reject_full_read(*args, **kwargs):
            pytest.fail("A numeric peptide query must not materialize the trajectory")

        monkeypatch.setattr(
            _h5msm05_modular, "read_independent_structures", reject_full_read
        )
    report = msm.build.get_peptide_bond_candidates(
        source, structure_indices=structure_index, chemical_state="structure"
    )
    assert report["structure_index"] == structure_index
    assert report["bonded_atom_pairs"].tolist() == (
        [[2, 5]] if structure_index == 0 else []
    )


@pytest.mark.parametrize("pbc", [False, True])
@pytest.mark.parametrize("unit", ["nm", "pm"])
def test_units_and_minimum_image_geometry(pbc, unit):
    source = _source()
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    coordinates[0, 5, 0] = 0.86
    msm.set(
        source,
        coordinates=puw.convert(puw.quantity(coordinates, "nm"), to_unit=unit),
        box=puw.quantity(np.eye(3)[None], "nm"),
    )
    with puw.context(standard_units=[unit, "ps"]):
        report = msm.build.get_peptide_bond_candidates(
            source, pbc=pbc, max_bond_length="150 pm"
        )
    assert report["bonded_atom_pairs"].tolist() == ([[2, 5]] if pbc else [])
    assert report["pbc_applied"] == pbc
    if pbc:
        np.testing.assert_allclose(
            puw.get_value(report["distances"], to_unit="nm"), [0.14]
        )


@pytest.mark.parametrize("ceiling", ["100 pm", "2 angstroms"])
def test_distance_ceiling_rejects_without_applying_bonds(ceiling):
    report = msm.build.get_peptide_bond_candidates(_source(), max_bond_length=ceiling)
    assert report["bonded_atom_pairs"].tolist() == (
        [] if ceiling == "100 pm" else [[2, 5]]
    )


def test_topology_without_coordinates_does_not_fabricate_a_geometry():
    report = msm.build.get_peptide_bond_candidates(_source().topology)
    assert report["structure_index"] is None
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "coordinates_unavailable" in report["links"][0]["reason_codes"]


def test_raw_pdb_query_does_not_import_openmm(monkeypatch):
    original = builtins.__import__

    def reject_openmm(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("A native peptide report must not invoke OpenMM")
        return original(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_openmm)
    report = msm.build.get_peptide_bond_candidates(_pdb())
    assert report["bonded_atom_pairs"].tolist() == [[2, 5]]


def test_atom_reordering_keeps_carbon_and_nitrogen_roles_separate_from_pair_sorting():
    text = _pdb().splitlines()
    order = [0, 5, 1, 6, 2, 7, 3, 8, 4, 9]
    source = msm.convert(
        "\n".join([*(text[index] for index in order), "END", ""]),
        to_form="molsysmt.MolSys",
        get_missing_bonds=False,
    )
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == [[1, 4]]
    assert report["carbon_atom_indices"].tolist() == [4]
    assert report["nitrogen_atom_indices"].tolist() == [1]


def test_terminal_oxt_blocks_an_outgoing_candidate():
    text = _pdb().replace("END\n", "")
    text += f"ATOM  {11:5d} {'OXT':^4} ALA A{1:4d}    {0.0:8.3f}{-1.2:8.3f}{0.0:8.3f}{1.0:6.2f}{0.0:6.2f}           O  \nEND\n"
    report = msm.build.get_peptide_bond_candidates(text)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "outgoing_terminal_carboxyl_oxygen" in report["links"][0]["reason_codes"]


def test_side_chain_alternate_sites_do_not_block_a_unique_backbone_pair():
    source = _source(alternate=True)
    source.structures.alternate_location = [
        {4: source.structures.alternate_location[0][2]}
    ]
    assert msm.build.get_peptide_bond_candidates(source)[
        "bonded_atom_pairs"
    ].tolist() == [[2, 5]]


@pytest.mark.parametrize("file_input", [False, True])
def test_unassociated_structure_does_not_guess_reference_chemistry(
    file_input, tmp_path
):
    source = _source()
    msm.set(source, element="system", structure_chemical_state_index=[None])
    if file_input:
        filename = str(tmp_path / "unassociated.h5msm")
        msm.convert(source, to_form=filename)
        source = filename
    report = msm.build.get_peptide_bond_candidates(source, chemical_state="structure")
    assert report["chemical_state_index"] is None
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "group_template_unassessed" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize("handler_input", [False, True])
def test_legacy_h5msm_and_caller_owned_handler_keep_the_source_pair(
    tmp_path, handler_input
):
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm
    from molsysmt.native import H5MSMFileHandler

    filename = str(tmp_path / "legacy.h5msm")
    to_file_h5msm(_source(), output_filename=filename)
    source = H5MSMFileHandler(filename) if handler_input else filename
    try:
        report = msm.build.get_peptide_bond_candidates(source)
        assert report["bonded_atom_pairs"].tolist() == [[2, 5]]
        if handler_input:
            assert source.file.id.valid
    finally:
        if handler_input:
            source.close()


@pytest.mark.parametrize("box", [np.zeros((1, 3, 3)), np.full((1, 3, 3), np.nan)])
def test_invalid_periodic_box_is_unassessed_instead_of_using_cartesian_geometry(box):
    source = _source()
    msm.set(source, box=puw.quantity(box, "nm"))
    report = msm.build.get_peptide_bond_candidates(source, pbc=True)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "invalid_periodic_box" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize("position", [0.0, np.nan])
def test_zero_or_nonfinite_endpoint_geometry_is_not_a_candidate(position):
    source = _source()
    coordinates = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    coordinates[0, 5] = [position, 0.0, 0.0]
    msm.set(source, coordinates=puw.quantity(coordinates, "nm"))
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].shape == (0, 2)


def test_explicit_conect_edge_is_a_stored_observation_and_is_not_rewritten():
    text = _pdb().replace("END\n", "CONECT    3    6\nEND\n")
    source = msm.convert(text, to_form="molsysmt.MolSys", get_missing_bonds=False)
    before = source.chemical_states.get_bonds().copy(deep=True)
    report = msm.build.get_peptide_bond_candidates(source)
    assert report["bonded_atom_pairs"].tolist() == [[2, 5]]
    assert report["missing_mask"].tolist() == [False]
    assert source.chemical_states.get_bonds()["evidence"].tolist() == ["explicit"]
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before)


def test_legacy_alternate_label_series_is_unassessed_instead_of_assumed_absent(
    tmp_path,
):
    import h5py

    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    filename = str(tmp_path / "legacy_alternate.h5msm")
    to_file_h5msm(_source(), output_filename=filename)
    with h5py.File(filename, "a") as file:
        group = file["structures"]
        if "alternate_location" in group:
            del group["alternate_location"]
        labels = np.full((1, 10), b"", dtype="S1")
        labels[0, 2] = b"A"
        group.create_dataset("alternate_location", data=labels)
    report = msm.build.get_peptide_bond_candidates(filename)
    assert report["bonded_atom_pairs"].shape == (0, 2)
    assert "unsupported_alternate_site_evidence" in report["links"][0]["reason_codes"]


@pytest.mark.parametrize(
    "arguments",
    [
        {"selection": [-1]},
        {"structure_indices": [1]},
        {"pbc": "yes"},
        {"skip_digestion": "yes"},
        {"max_bond_length": None},
        {"max_bond_length": "-1 nm"},
        {"max_bond_length": "1 ps"},
        {"max_bond_length": puw.quantity([1.0, 2.0], "nm")},
        {"max_bond_length": puw.quantity(np.nan, "nm")},
    ],
)
def test_invalid_public_arguments_are_refused(arguments):
    with pytest.raises(ArgumentError):
        msm.build.get_peptide_bond_candidates(_source(), **arguments)
