"""Checking literal PDB declarations, ambiguity and detached typed history."""

import numpy as np
import pytest

import molsysmt as msm
from tests.conversion_truth.test_pdb_fidelity import (
    _pdb_atom_line,
    _pdb_link_line,
    _pdb_ssbond_line,
)


def _atoms(*, alternate=False, third=False):
    first = _pdb_atom_line(1, "SG", "CYS", "A", 1, (0, 0, 0), "S")
    if alternate:
        first = first[:16] + "A" + first[17:]
        second_site = _pdb_atom_line(4, "SG", "CYS", "A", 1, (0, 1, 0), "S")
        first += second_site[:16] + "B" + second_site[17:]
    second = _pdb_atom_line(2, "SG", "CYS", "A", 2, (2.03, 0, 0), "S")
    last = _pdb_atom_line(3, "SG", "CYS", "A", 3, (-2.03, 0, 0), "S") if third else ""
    return first + second + last


def _link(**fields):
    line = list(_pdb_link_line("SG", "CYS", "A", 1, "SG", "CYS", "A", 2))
    for name, value in fields.items():
        start, stop = {"alt": (16, 17), "symmetry": (66, 72)}[name]
        line[start:stop] = f"{value:>{stop - start}}"
    return "".join(line)


def _read(text, route, tmp_path):
    filename = tmp_path / "declarations.pdb"
    filename.write_text(text)
    handler = None
    source = text
    if route == "file":
        source = filename
    elif route == "handler":
        handler = msm.convert(filename, to_form="molsysmt.PDBFileHandler")
        source = handler
    try:
        output = msm.convert(source, get_missing_bonds=False)
        if handler is not None:
            assert not handler.file.closed
        assert filename.read_text() == text
        return output
    finally:
        if handler is not None:
            handler.close()


def _diagnostics(output):
    history = output.chemical_states.get_preparation_history()
    report = history[0]["report"]
    assert report["schema"] == "molsysmt.pdb_connectivity@1"
    assert report["status"] == "disabled"
    diagnostic = report["declaration_issues"]
    assert diagnostic["schema"] == "molsysmt.pdb_declarations@1"
    assert diagnostic["atom_index_scope"] == "first_model_canonical_sites"
    table = diagnostic["records"]
    assert len({len(column) for column in table.values()}) == 1
    assert table["atom_indices"].dtype == np.int64
    assert table["atom_indices"].shape[1:] == (2,)
    assert table["line_number"].dtype == np.int64
    assert table["accepted"].dtype == bool
    assert table["conditional"].dtype == bool
    assert all(column.dtype.kind != "O" for column in table.values())
    return diagnostic, table


def _pairs(output):
    return (
        output.chemical_states.get_bonds()[["atom1_index", "atom2_index"]]
        .to_numpy(dtype=np.int64)
        .tolist()
    )


@pytest.mark.parametrize("route", ["file", "handler", "text"])
def test_redundant_declarations_preserve_one_edge_and_every_source_record(
    route, tmp_path
):
    records = [
        "CONECT    1    2\n",
        "CONECT    2    1\n",
        _link(),
        _pdb_ssbond_line("A", 1, "A", 2),
    ]
    text = "HEADER    DECLARATION EVIDENCE\n" + _atoms() + "".join(records) + "END\n"
    output = _read(text, route, tmp_path)
    diagnostic, table = _diagnostics(output)
    assert _pairs(output) == [[0, 1]]
    assert not diagnostic["unresolved"]
    assert diagnostic["repeated_pairs"]
    assert table["record_type"].tolist() == ["CONECT", "CONECT", "LINK", "SSBOND"]
    assert table["line_number"].tolist() == [4, 5, 6, 7]
    assert table["record_text"].tolist() == [
        line.rstrip("\n").ljust(80) for line in records
    ]
    assert table["status"].tolist() == [
        "accepted",
        "redundant",
        "redundant",
        "redundant",
    ]
    assert table["accepted"].tolist() == [True] * 4
    bonds = output.chemical_states.get_bonds()
    assert "bond_order" not in bonds or bonds["bond_order"].isna().all()
    # Historical evidence keeps the original reader axis after extraction.
    subset = msm.extract(output, selection=[1])
    assert _pairs(subset) == []
    retained = _diagnostics(subset)[1]
    np.testing.assert_array_equal(retained["atom_indices"], table["atom_indices"])


@pytest.mark.parametrize(
    "declaration,status,pair",
    [
        ("CONECT    1   99\n", "missing_endpoint", [0, -1]),
        ("CONECT   99    2\n", "missing_endpoint", [-1, 1]),
        ("CONECT    1    1\n", "self_reference", [0, 0]),
        ("CONECT    1\n", "missing_target", [0, -1]),
        (_link(alt="Z"), "missing_alternate", [0, 1]),
        (_link(symmetry="2555"), "unsupported_symmetry", [0, 1]),
    ],
)
def test_unresolved_declarations_are_located_without_inventing_edges(
    declaration, status, pair, tmp_path
):
    text = "HEADER    UNRESOLVED DECLARATION\n" + _atoms() + declaration + "END\n"
    output = _read(text, "text", tmp_path)
    assert _pairs(output) == []
    diagnostic, table = _diagnostics(output)
    assert diagnostic["unresolved"]
    assert _pairs(output) == []
    assert table["status"].tolist() == [status]
    assert table["atom_indices"].tolist() == [pair]
    assert table["line_number"].tolist() == [4]
    assert table["accepted"].tolist() == [False]


@pytest.mark.parametrize(
    "declaration", [_link(alt="A"), _pdb_ssbond_line("A", 1, "A", 2)]
)
def test_alternate_specific_connectivity_keeps_canonical_mapping_and_conditional_scope(
    declaration, tmp_path
):
    text = (
        "HEADER    CONDITIONAL CONNECTIVITY\n"
        + _atoms(alternate=True)
        + declaration
        + "END\n"
    )
    output = _read(text, "text", tmp_path)
    diagnostic, table = _diagnostics(output)
    assert not diagnostic["unresolved"]
    assert diagnostic["conditional_pairs"]
    assert table["status"].tolist() == ["conditional"]
    assert table["accepted"].all()
    assert table["conditional"].all()
    assert _pairs(output) == [[0, 1]]
    assert output.get_n_atoms() == 2


def test_disulfide_partner_conflicts_remain_declared_without_arbitrary_choice(tmp_path):
    text = "HEADER    CONTRADICTORY DISULFIDES\n" + _atoms(third=True)
    text += (
        _pdb_ssbond_line("A", 1, "A", 2) + _pdb_ssbond_line("A", 1, "A", 3) + "END\n"
    )
    output = _read(text, "text", tmp_path)
    diagnostic, table = _diagnostics(output)
    assert diagnostic["conflicting_disulfide_partners"]
    assert table["status"].tolist() == ["conflicting_disulfide_partners"] * 2
    assert table["accepted"].all()
    assert _pairs(output) == [[0, 1], [0, 2]]
    assert msm.get(output, connectivity_completeness=True) != "complete"


def test_typed_declaration_history_survives_h5msm_without_shared_arrays(tmp_path):
    text = "HEADER    PERSISTENT DECLARATION\n" + _atoms() + "CONECT    1   99\nEND\n"
    output = _read(text, "text", tmp_path)
    target = tmp_path / "declarations.h5msm"
    msm.convert(output, to_form=str(target))
    loaded = msm.convert(target)
    _, expected = _diagnostics(output)
    _, restored = _diagnostics(loaded)
    for name in expected:
        np.testing.assert_array_equal(restored[name], expected[name])
        assert restored[name].dtype == expected[name].dtype
    restored["atom_indices"][:] = 123
    assert _diagnostics(loaded)[1]["atom_indices"].tolist() == [[0, -1]]


def test_empty_declaration_columns_have_defined_shapes_and_types(tmp_path):
    output = _read("HEADER    NO DECLARATIONS\n" + _atoms() + "END\n", "text", tmp_path)
    diagnostic, table = _diagnostics(output)
    assert not diagnostic["unresolved"]
    assert table["atom_indices"].shape == (0, 2)
    assert table["line_number"].shape == (0,)


@pytest.mark.parametrize("kind", ["duplicate_serial", "duplicate_symbolic_identity"])
def test_ambiguous_identity_is_reported_without_selecting_first_match(kind, tmp_path):
    first = _pdb_atom_line(1, "SG", "CYS", "A", 1, (0, 0, 0), "S")
    second = _pdb_atom_line(
        1 if kind == "duplicate_serial" else 3, "SG", "CYS", "A", 1, (4, 0, 0), "S"
    )
    target = _pdb_atom_line(2, "SG", "CYS", "A", 2, (2, 0, 0), "S")
    declaration = "CONECT    1    2\n" if kind == "duplicate_serial" else _link()
    text = (
        "HEADER    AMBIGUOUS IDENTITY\n"
        + first
        + "TER\n"
        + second
        + target
        + declaration
        + "END\n"
    )
    output = _read(text, "text", tmp_path)
    assert _pairs(output) == []
    diagnostic, table = _diagnostics(output)
    assert diagnostic["unresolved"]
    assert table["status"].tolist() == ["ambiguous_endpoint"]
    assert table["atom_indices"].tolist() == [[-1, 2]]
    assert table["endpoint_match_counts"].tolist() == [[2, 1]]


@pytest.mark.parametrize("symmetry", ["", "1555"])
def test_identity_symmetry_and_insertion_codes_resolve_literal_source_sites(
    symmetry, tmp_path
):
    first = _pdb_atom_line(1, "SG", "CYS", "A", 1, (0, 0, 0), "S", insertion_code="A")
    text = "HEADER    INSERTION CODE\n" + first
    text += _pdb_atom_line(2, "SG", "CYS", "A", 2, (2, 0, 0), "S")
    record = list(_link(symmetry=symmetry))
    record[26] = "A"
    text += "".join(record) + "END\n"
    output = _read(text, "text", tmp_path)
    assert _pairs(output) == [[0, 1]]
    diagnostic, table = _diagnostics(output)
    assert not diagnostic["unresolved"]
    assert table["record_text"][0][26] == "A"
    assert table["symmetry"].tolist() == [["", symmetry]]


def test_public_conversion_report_and_strict_mode_expose_unsupported_declarations():
    text = "HEADER    PUBLIC DIAGNOSIS\n" + _atoms() + _link(symmetry="2555") + "END\n"
    result, report = msm.convert(text, get_missing_bonds=False, return_report=True)
    assert _pairs(result) == []
    assert any(
        issue.attribute == "bonded_atoms" and issue.kind == "adapter_limitation"
        for issue in report.issues
    )
    with pytest.raises(msm.NotCompatibleConversionError):
        msm.convert(text, get_missing_bonds=False, strict=True)
