"""Preserve opaque PDB comments while reading the declared coordinate fields."""

from contextlib import closing
from hashlib import sha256
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw
from molsysmt.native import PDBFileHandler
from molsysmt.native.pdb_file_handler import parse_format33

GHECOM = Path(__file__).with_name("data") / "ghecom_20260817_assigned.pdb"
GHECOM_SHA256 = "6b5684afcfb42cd66738264ffcb6ab69a6934b0424741c1523a4c08ed20096cd"


@pytest.mark.parametrize("length_unit", ["nm", "angstrom"])
def test_ghecom_coordinate_query_preserves_source_and_length_units(
    tmp_path, length_unit
):
    original = GHECOM.read_bytes()
    assert sha256(original).hexdigest() == GHECOM_SHA256
    source = tmp_path / "assigned.pdb"
    source.write_bytes(original)
    expected_angstrom = np.array(
        [
            [
                [1.874, 1.874, 1.874],
                [1.874, -1.874, -1.874],
                [-1.874, 1.874, -1.874],
                [-1.874, -1.874, 1.874],
            ]
        ]
    )
    with puw.context(standard_units=[length_unit, "ps", "radians"]):
        coordinates = msm.get(source, coordinates=True)
        assert coordinates.shape == (1, 4, 3)
        assert puw.get_unit(coordinates) == puw.unit(length_unit)
        np.testing.assert_allclose(
            puw.get_value(coordinates, to_unit="angstrom"),
            expected_angstrom,
            rtol=0,
            atol=1e-14,
        )
    assert source.read_bytes() == original


def test_ghecom_native_comments_keep_the_full_opaque_text():
    original = GHECOM.read_text()
    expected = "".join(
        line[6:].strip() + "\n"
        for line in original.splitlines()
        if line.startswith("REMARK")
    )
    assert len(next(line for line in original.splitlines() if "COMMAND" in line)) > 80
    with closing(PDBFileHandler(original)) as handler:
        remarks = handler.entry.title.remarks
        assert [(remark.remarkNum, remark.message) for remark in remarks] == [
            (None, expected)
        ]
        assert handler.file.getvalue() == original


@pytest.mark.parametrize("line_ending", ["\n", "\r\n"])
def test_numbered_and_opaque_remark_blocks_keep_order(line_ending):
    lines = [
        "REMARK   1 first numbered comment",
        "REMARK   1 continuation",
        "REMARK  COMMENT unnumbered evidence",
        "REMARK    blank-number evidence",
        "REMARK   1 numbered after opaque",
        "REMARK 350 BIOMOLECULE: 1",
        "END",
    ]
    entry = parse_format33(line_ending.join(lines) + line_ending)
    assert [(remark.remarkNum, remark.message) for remark in entry.title.remarks] == [
        (1, "first numbered comment\ncontinuation\n"),
        (None, "COMMENT unnumbered evidence\nblank-number evidence\n"),
        (1, "numbered after opaque\n"),
        (350, "BIOMOLECULE: 1\n"),
    ]


@pytest.mark.parametrize(
    "line,number,message",
    [
        ("REMARK", None, "\n"),
        ("REMARK  COMMENT trailing evidence", None, "COMMENT trailing evidence\n"),
        ("REMARK   1 trailing evidence", 1, "trailing evidence\n"),
    ],
)
def test_remark_at_end_of_file_is_preserved(line, number, message):
    entry = parse_format33([line])
    assert [(remark.remarkNum, remark.message) for remark in entry.title.remarks] == [
        (number, message)
    ]


def test_comments_in_separate_sections_are_retained():
    atom = next(
        line for line in GHECOM.read_text().splitlines() if line.startswith("ATOM")
    )
    entry = parse_format33(
        [
            "REMARK   1 before coordinates",
            atom,
            "REMARK  COMMENT after coordinates",
            "END",
        ]
    )
    assert [(remark.remarkNum, remark.message) for remark in entry.title.remarks] == [
        (1, "before coordinates\n"),
        (None, "COMMENT after coordinates\n"),
    ]
