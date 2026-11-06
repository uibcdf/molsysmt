"""Checking declared connectivity against excluded geometric inference policies."""

import builtins

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from tests.build.test_get_residue_chemical_coverage import MLY, MSE, SEP, TPO
from tests.conversion_truth.test_pdb_fidelity import (
    _pdb_atom_line,
    _pdb_link_line,
    _pdb_ssbond_line,
)

METHODS = [
    "supported_group_templates",
    "supported_group_templates_with_hydrogen_aliases",
]
SIDE_CHAIN_PAIRS = [[0, 1], [2, 3], [4, 5]]


def _pdb(declarations):
    # Three sulfurs form an equilateral 2-Angstrom triangle. The remaining
    # unsupported atoms are intentionally close: proximity must not add edges.
    rows = [
        ("CB", "CYS", 1, "C", (-1.5, 0, 0)),
        ("SG", "CYS", 1, "S", (0, 0, 0)),
        ("CB", "CYS", 2, "C", (3.5, 0, 0)),
        ("SG", "CYS", 2, "S", (2, 0, 0)),
        ("CB", "CYS", 3, "C", (1, 3.2, 0)),
        ("SG", "CYS", 3, "S", (1, 1.732, 0)),
        ("O", "HOH", 4, "O", (0.1, 0, 0)),
        ("H1", "HOH", 4, "H", (0.2, 0, 0)),
        ("H2", "HOH", 4, "H", (0.1, 0.1, 0)),
        ("C1", "LIG", 5, "C", (0.3, 0, 0)),
        ("N1", "LIG", 5, "N", (0.4, 0, 0)),
        ("O1", "LIG", 5, "O", (0.5, 0, 0)),
        ("ZN", "ZN", 6, "Zn", (0.1, 0.1, 0)),
        ("N", "ZZZ", 7, "N", (0.6, 0, 0)),
        ("CA", "ZZZ", 7, "C", (0.7, 0, 0)),
        ("C", "ZZZ", 7, "C", (0.8, 0, 0)),
        ("O", "ZZZ", 7, "O", (0.9, 0, 0)),
        ("CB", "ZZZ", 7, "C", (0.7, 0.1, 0)),
    ]
    text = "HEADER    BOUNDED CONNECTIVITY POLICIES\n"
    text += "".join(
        _pdb_atom_line(serial, name, group, "A", index, xyz, element)
        for serial, (name, group, index, element, xyz) in enumerate(rows, 1)
    )
    expected = []
    if declarations != "none":
        text += "CONECT   10   11\n"
        text += _pdb_link_line("O", "HOH", "A", 4, "ZN", "ZN", "A", 6)
        text += _pdb_ssbond_line("A", 1, "A", 2)
        expected = [[1, 3], [6, 12], [9, 10]]
    if declarations == "competing":
        text += _pdb_ssbond_line("A", 1, "A", 3)
        expected.append([1, 5])
    return text + "END\n", sorted(expected)


def _pairs(source):
    return (
        source.chemical_states.get_bonds()[["atom1_index", "atom2_index"]]
        .to_numpy(dtype=np.int64)
        .tolist()
    )


def _assert_policies(report, unsupported=(3, 4, 5, 6)):
    policies = report["excluded_inference_policies"]
    assert policies["disulfides"] == "retain_stored_edges_only"
    assert policies["metal_coordination"] == "retain_stored_edges_only"
    assert policies["unsupported_group_geometry"] == "disabled"
    assert policies["unsupported_group_indices"].dtype == np.int64
    assert policies["unsupported_group_indices"].tolist() == list(unsupported)


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize("declarations", ["none", "single", "competing"])
@pytest.mark.parametrize("route", ["native", "text", "file", "handler"])
def test_native_composition_keeps_declared_edges_without_geometric_repair(
    method, declarations, route, tmp_path, monkeypatch
):
    text, declared = _pdb(declarations)
    path = tmp_path / "boundary.pdb"
    path.write_text(text)
    explicit = msm.convert(text, get_missing_bonds=False)
    before = explicit.chemical_states.get_bonds().copy(deep=True)
    source = explicit
    if route == "text":
        source = text
    elif route == "file":
        source = str(path)
    elif route == "handler":
        source = msm.convert(path, to_form="molsysmt.PDBFileHandler")
    original_import = builtins.__import__

    def reject_openmm(name, *args, **kwargs):
        if name == "openmm" or name.startswith("openmm."):
            pytest.fail("Native boundary qualification must not import OpenMM")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_openmm)
    try:
        with puw.context(standard_units=["pm", "fs"]):
            result = msm.build.infer_covalent_bonds(
                source, method=method, return_report=True
            )
        output, report = result["molecular_system"], result["report"]
        assert _pairs(output) == sorted(declared + SIDE_CHAIN_PAIRS)
        assert report["added_bonded_atom_pairs"].tolist() == SIDE_CHAIN_PAIRS
        _assert_policies(report)
        assert [group["template"] for group in report["heavy_groups"][3:]] == [None] * 4
        assert all(
            "no_exact_group_template" in group["reason_codes"]
            for group in report["heavy_groups"][3:]
        )
        bonds = output.chemical_states.get_bonds()
        for index, pair in enumerate(_pairs(output)):
            assert bonds.loc[index, "evidence"] == (
                "explicit" if pair in declared else "inferred"
            )
        for domain in ("atoms", "groups", "chains", "molecules", "entities"):
            pd.testing.assert_frame_equal(
                getattr(output.topology, domain), getattr(explicit.topology, domain)
            )
        np.testing.assert_array_equal(
            puw.get_value(output.structures.coordinates, to_unit="nm"),
            puw.get_value(explicit.structures.coordinates, to_unit="nm"),
        )
        pd.testing.assert_frame_equal(explicit.chemical_states.get_bonds(), before)
        assert path.read_text() == text
    finally:
        if route == "handler":
            assert not source.file.closed
            source.close()


@pytest.mark.parametrize("route", ["file", "text", "handler"])
@pytest.mark.parametrize("declarations", ["none", "single", "competing"])
def test_pdb_native_engine_preserves_the_same_boundaries_and_declaration_audit(
    route, declarations, tmp_path
):
    text, declared = _pdb(declarations)
    path = tmp_path / "reader.pdb"
    path.write_text(text)
    handler = None
    source = text if route == "text" else str(path)
    if route == "handler":
        handler = msm.convert(path, to_form="molsysmt.PDBFileHandler")
        source = handler
    try:
        output = msm.convert(
            source,
            get_missing_bonds=True,
            bond_inference_engine="MolSysMT",
        )
        assert _pairs(output) == sorted(declared + SIDE_CHAIN_PAIRS)
        history = output.chemical_states.get_preparation_history()
        assert len(history) == 2
        declarations_report = history[0]["report"]["declaration_issues"]
        assert declarations_report["conflicting_disulfide_partners"] is (
            declarations == "competing"
        )
        _assert_policies(history[1]["report"])
    finally:
        if handler is not None:
            assert not handler.file.closed
            handler.close()


def test_three_geometric_disulfide_candidates_do_not_choose_a_covalent_partner():
    text, _ = _pdb("none")
    source = msm.convert(text, get_missing_bonds=False)
    analysis = msm.interactions.disulfides.get_disulfide_candidates(
        source, pbc=False, output_type="molsysmt.Interactions"
    )
    assert analysis.n_interactions == 3
    pairs, distances = msm.interactions.disulfides.get_disulfide_candidates(
        source, pbc=False
    )
    assert pairs[0].tolist() == [[1, 3], [1, 5], [3, 5]]
    np.testing.assert_allclose(
        puw.get_value(distances[0], to_unit="angstrom"), 2.0, atol=5e-5, rtol=0
    )
    output = msm.build.infer_covalent_bonds(source)
    assert _pairs(output) == SIDE_CHAIN_PAIRS
    assert _pairs(source) == []


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize(
    "group_name,spec", [("MSE", MSE), ("SEP", SEP), ("TPO", TPO), ("MLY", MLY)]
)
def test_curated_modified_groups_keep_their_own_literal_connectivity(
    group_name, spec, method
):
    names, elements, reference_pairs = spec
    builder = msm.MolSysBuilder()
    atoms = [
        builder.add_atom(atom_name=name, atom_type=element)
        for name, element in zip(names, elements)
    ]
    builder.add_group(atoms, group_name=group_name)
    source = builder.build()
    expected = sorted(
        sorted([names.index(first), names.index(second)])
        for first, second, _ in reference_pairs
    )
    result = msm.build.infer_covalent_bonds(source, method=method, return_report=True)
    assert _pairs(result["molecular_system"]) == expected
    assert result["report"]["heavy_groups"][0]["template"]["group_name"] == group_name
    assert result["report"]["excluded_inference_policies"][
        "unsupported_group_indices"
    ].shape == (0,)
    assert _pairs(source) == []


def test_policy_indices_are_original_history_after_extraction_and_h5msm(tmp_path):
    text, declared = _pdb("single")
    source = msm.convert(text, get_missing_bonds=False)
    result = msm.build.infer_covalent_bonds(source, return_report=True)
    _assert_policies(result["report"])
    result["report"]["excluded_inference_policies"]["unsupported_group_indices"][:] = -1
    output = msm.extract(result["molecular_system"], selection=[9, 10, 12])
    assert _pairs(output) == [[0, 1]]
    path = str(tmp_path / "policies.h5msm")
    msm.convert(output, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys")
    saved = restored.chemical_states.get_preparation_history()[-1]
    assert saved["index_scope"] == "operation"
    _assert_policies(saved["report"])
    assert saved["report"]["n_atoms"] == 18
    assert saved["report"]["source_bond_correspondence"].shape == (len(declared), 2)
    assert _pairs(restored) == [[0, 1]]


def test_nonfinite_unsupported_geometry_is_not_used_to_fabricate_bonds():
    text, declared = _pdb("single")
    source = msm.convert(text, get_missing_bonds=False)
    xyz = puw.get_value(source.structures.coordinates, to_unit="nm").copy()
    xyz[0, 6:] = np.nan
    source.structures.coordinates = puw.quantity(xyz, "nm")
    result = msm.build.infer_covalent_bonds(source, return_report=True)
    assert _pairs(result["molecular_system"]) == sorted(declared + SIDE_CHAIN_PAIRS)
    _assert_policies(result["report"])
    np.testing.assert_array_equal(
        puw.get_value(result["molecular_system"].structures.coordinates, to_unit="nm"),
        xyz,
    )


@pytest.mark.parametrize("method", METHODS)
@pytest.mark.parametrize(
    "selection,unsupported", [([1, 3], []), ([6, 7, 8], [3]), ([], [])]
)
def test_selection_cannot_promote_proximity_or_remove_existing_source_edges(
    method, selection, unsupported
):
    text, declared = _pdb("competing")
    source = msm.convert(text, get_missing_bonds=False)
    result = msm.build.infer_covalent_bonds(
        source, selection=selection, method=method, return_report=True
    )
    assert _pairs(result["molecular_system"]) == declared
    assert result["report"]["added_bonded_atom_pairs"].shape == (0, 2)
    _assert_policies(result["report"], unsupported)


@pytest.mark.parametrize("kind", ["symmetry", "missing_site", "malformed_label"])
def test_native_reader_does_not_replace_unresolved_ssbond_with_distance(kind):
    text, _ = _pdb("none")
    line = list(_pdb_ssbond_line("A", 1, "A", 2))
    if kind == "symmetry":
        line[66:72] = "  2555"
        expected_status = "unsupported_symmetry"
    elif kind == "missing_site":
        line[31:35] = "  99"
        expected_status = "missing_endpoint"
    else:
        line[25:28] = "ALA"
        expected_status = "malformed_endpoint"
    text = text.removesuffix("END\n") + "".join(line) + "END\n"
    output = msm.convert(text, get_missing_bonds=True, bond_inference_engine="MolSysMT")
    assert _pairs(output) == SIDE_CHAIN_PAIRS
    history = output.chemical_states.get_preparation_history()
    diagnostic = history[0]["report"]["declaration_issues"]
    assert diagnostic["unresolved"]
    assert diagnostic["records"]["status"].tolist() == [expected_status]
    assert diagnostic["records"]["accepted"].tolist() == [False]
    _assert_policies(history[1]["report"])


def test_existing_coordination_type_is_retained_without_recertification():
    text, declared = _pdb("single")
    source = msm.convert(text, get_missing_bonds=False)
    msm.set(source, element="bond", selection=[1], bond_type="dative")
    before = source.chemical_states.get_bonds().copy(deep=True)
    result = msm.build.infer_covalent_bonds(source, return_report=True)
    report = result["report"]
    output = result["molecular_system"]
    assert _pairs(output) == sorted(declared + SIDE_CHAIN_PAIRS)
    for old_index, new_index in report["source_bond_correspondence"]:
        assert (
            output.chemical_states.get_bonds().loc[new_index, "bond_type"]
            == before.loc[old_index, "bond_type"]
        )
    _assert_policies(report)
    pd.testing.assert_frame_equal(source.chemical_states.get_bonds(), before)
