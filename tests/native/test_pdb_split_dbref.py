"""Preserve valid long-accession DBREF pairs and diagnose malformed pairings."""

import io

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import FileContentError
from molsysmt.native import PDBFileHandler
from molsysmt.native.pdb_file_handler import parse_format33

# Original fixed-column metadata from RCSB 5XJH, with one minimal coordinate
# record to exercise public reading without inferring missing chemistry.
PAIR = (
    "DBREF1 5XJH A   34   290  UNP                  PETH_IDESA                       \n"
    "DBREF2 5XJH A     A0A0K8P6T7                         34         290             \n"
)
ATOM = (
    "ATOM      1  CA  ALA A  34       1.000   2.000   3.000  1.00 20.00           C  \n"
)


def read(text, route, tmp_path):
    if route == "text":
        return parse_format33(text)
    if route == "lines":
        return parse_format33(text.splitlines(keepends=True))
    if route == "stream":
        return PDBFileHandler(io.StringIO(text)).entry
    path = tmp_path / "dbref.pdb"
    path.write_text(text)
    return PDBFileHandler(path).entry


@pytest.mark.parametrize("route", ["text", "lines", "stream", "file"])
def test_split_dbref_retains_declared_chain_accession_and_sequence_ranges(
    route, tmp_path
):
    text = PAIR + ATOM + "END\n"
    entry = read(text, route, tmp_path)
    assert len(entry.primary_structure.dbref1_dbref2) == 1
    record = entry.primary_structure.dbref1_dbref2[0]
    assert record.idCode == "5XJH"
    assert record.chainId == "A"
    assert record.dbAccession == "A0A0K8P6T7"
    assert record.dbIdCode == "PETH_IDESA"
    assert (record.seqBegin, record.seqEnd) == (34, 290)
    assert (record.dbSeqBegin, record.dbSeqEnd) == (34, 290)
    path = tmp_path / "source.pdb"
    path.write_text(text)
    source = msm.convert(path, to_form="molsysmt.MolSys", get_missing_bonds=False)
    assert source.topology.atoms.atom_id.tolist() == ["1"]
    assert source.topology.groups.group_id.tolist() == ["34"]
    assert source.topology.chains.chain_id.tolist() == ["A"]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(source.structures.coordinates, to_unit="nm"),
        [[[0.1, 0.2, 0.3]]],
    )
    assert path.read_text() == text


@pytest.mark.parametrize("route", ["text", "lines", "stream", "file"])
@pytest.mark.parametrize("malformed", ["missing", "chain"])
def test_bad_dbref_pair_raises_format_diagnostic(route, malformed, tmp_path):
    first, second = PAIR.splitlines(keepends=True)
    if malformed == "chain":
        second = second[:12] + "B" + second[13:]
    else:
        second = ""
    with pytest.raises(FileContentError, match="DBREF2"):
        read(first + second + ATOM + "END\n", route, tmp_path)
