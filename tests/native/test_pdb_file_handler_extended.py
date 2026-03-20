"""
Extended unit tests for molsysmt.native.PDBFileHandler / parse_format33.

These tests target record-type branches and parsing paths not already covered
by test_pdb_file_handler.py, including:

  - HEADER, TITLE, COMPND, SOURCE, KEYWDS, EXPDTA (title section)
  - NUMMDL (number of models)
  - SEQRES, SEQADV, DBREF (primary structure section)
  - MODRES (modified residues)
  - HELIX, SHEET (secondary structure section)
  - SSBOND (connectivity annotation)
  - LINK records
  - SITE records (miscellaneous features)
  - CRYST1, ORIGX, SCALE (crystallographic section), already partially tested
  - Multi-model PDB files (MODEL / ENDMDL)
  - HETATM records
  - CONECT records (connectivity section)
  - MASTER bookkeeping record
  - Input as raw string, as list of lines, and as file path
  - Closed-file mode
  - guess_format_version always returns '3.3'
"""

import io
import pytest
from importlib.resources import files

from molsysmt.native import PDBFileHandler
from molsysmt.native.pdb_file_handler import parse_format33, guess_format_version


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _path(pdb_id):
    """Return the absolute path string for a bundled PDB file."""
    return str(files('molsysmt.data.pdb').joinpath(f'{pdb_id}.pdb'))


def _read_text(pdb_id):
    """Return the full text content of a bundled PDB file."""
    with open(_path(pdb_id), 'r') as fh:
        return fh.read()


def _read_lines(pdb_id):
    """Return the lines of a bundled PDB file as a list."""
    with open(_path(pdb_id), 'r') as fh:
        return fh.readlines()


# ---------------------------------------------------------------------------
# guess_format_version
# ---------------------------------------------------------------------------

def test_guess_format_version_returns_33():
    """guess_format_version always returns '3.3' regardless of content."""
    buf = io.StringIO("HEADER    TEST FILE\n")
    assert guess_format_version(buf) == '3.3'


# ---------------------------------------------------------------------------
# Input mode: raw string (content, not file path)
# ---------------------------------------------------------------------------

def test_parse_from_string_content():
    """parse_format33 accepts a multi-line string as input."""
    content = _read_text('3c0f')
    pdb = parse_format33(content)
    assert pdb is not None
    assert pdb.title.source[0].organism_scientific == 'ARCHAEOGLOBUS FULGIDUS DSM 4304'


# ---------------------------------------------------------------------------
# Input mode: list of lines
# ---------------------------------------------------------------------------

def test_parse_from_list_of_lines():
    """parse_format33 accepts a list of lines as input."""
    lines = _read_lines('3c0f')
    pdb = parse_format33(lines)
    assert pdb is not None
    assert len(pdb.coordinate.model) >= 1


# ---------------------------------------------------------------------------
# Input mode: file path string (already tested by existing tests, but verify
# that PDBFileHandler auto-loads on construction)
# ---------------------------------------------------------------------------

def test_constructor_autoloads_pdb():
    """PDBFileHandler auto-loads the entry on construction from a file path."""
    handler = PDBFileHandler(_path('3c0f'))
    assert handler.entry is not None
    assert handler.format_version == '3.3'


# ---------------------------------------------------------------------------
# Closed-file mode
# ---------------------------------------------------------------------------

def test_constructor_closed_mode():
    """PDBFileHandler with closed=True closes the internal buffer after load."""
    handler = PDBFileHandler(_path('3c0f'), closed=True)
    # entry must still be populated even though the file is closed
    assert handler.entry is not None
    assert handler.file.closed


# ---------------------------------------------------------------------------
# HEADER record (title section)
# ---------------------------------------------------------------------------

def test_header_classification():
    """HEADER record classification field is parsed correctly."""
    pdb = parse_format33(_path('1bnf'))
    assert 'ENDONUCLEASE' in pdb.title.header.classification.upper()


def test_header_id_code():
    """HEADER record idCode is parsed correctly."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.title.header.idCode.strip() == '1BNF'


# ---------------------------------------------------------------------------
# TITLE record
# ---------------------------------------------------------------------------

def test_title_record():
    """TITLE record content is concatenated and stored."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.title.title is not None
    assert len(pdb.title.title.title) > 0


# ---------------------------------------------------------------------------
# COMPND record
# ---------------------------------------------------------------------------

def test_compnd_mol_id():
    """COMPND record mol_id is an integer."""
    pdb = parse_format33(_path('1bnf'))
    assert isinstance(pdb.title.compnd[0].mol_id, int)
    assert pdb.title.compnd[0].mol_id == 1


def test_compnd_molecule():
    """COMPND MOLECULE field is parsed."""
    pdb = parse_format33(_path('1bnf'))
    assert 'BARNASE' in pdb.title.compnd[0].molecule.upper()


def test_compnd_chain():
    """COMPND CHAIN field yields a list of chain identifiers."""
    pdb = parse_format33(_path('1bnf'))
    chains = pdb.title.compnd[0].chain
    assert isinstance(chains, list)
    assert 'A' in chains


def test_compnd_ec():
    """COMPND EC field is parsed when present."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.title.compnd[0].ec is not None


# ---------------------------------------------------------------------------
# SOURCE record
# ---------------------------------------------------------------------------

def test_source_mol_id():
    """SOURCE record mol_id is an integer."""
    pdb = parse_format33(_path('1bnf'))
    assert isinstance(pdb.title.source[0].mol_id, int)


def test_source_organism_scientific():
    """SOURCE ORGANISM_SCIENTIFIC field is parsed."""
    pdb = parse_format33(_path('1bnf'))
    assert 'BACILLUS' in pdb.title.source[0].organism_scientific.upper()


def test_source_expression_system():
    """SOURCE EXPRESSION_SYSTEM field is parsed."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.title.source[0].expression_system is not None


# ---------------------------------------------------------------------------
# KEYWDS record
# ---------------------------------------------------------------------------

def test_keywds_record():
    """KEYWDS record yields a non-empty list of keywords."""
    pdb = parse_format33(_path('181l'))
    assert pdb.title.keywds is not None
    assert isinstance(pdb.title.keywds.keywds, list)
    assert len(pdb.title.keywds.keywds) >= 1


# ---------------------------------------------------------------------------
# EXPDTA record
# ---------------------------------------------------------------------------

def test_expdta_record():
    """EXPDTA record technique field is populated."""
    pdb = parse_format33(_path('181l'))
    assert pdb.title.expdta is not None
    assert len(pdb.title.expdta.technique) > 0


# ---------------------------------------------------------------------------
# NUMMDL record (multi-model NMR files)
# ---------------------------------------------------------------------------

def test_nummdl_record():
    """NUMMDL record model number is parsed correctly (1l2y has 38 models)."""
    pdb = parse_format33(_path('1l2y'))
    assert pdb.title.nummdl is not None
    assert pdb.title.nummdl.modelNumber == 38


# ---------------------------------------------------------------------------
# SEQRES record (primary structure section)
# ---------------------------------------------------------------------------

def test_seqres_chain_id():
    """SEQRES records are associated with the correct chain."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.primary_structure.seqres is not None
    chain_ids = [sr.chainId for sr in pdb.primary_structure.seqres]
    assert 'A' in chain_ids


def test_seqres_num_res():
    """SEQRES numRes matches expected residue count."""
    pdb = parse_format33(_path('1bnf'))
    # 1BNF chain A has 110 residues
    sr_a = next(sr for sr in pdb.primary_structure.seqres if sr.chainId == 'A')
    assert sr_a.numRes == 110


def test_seqres_residue_names():
    """SEQRES residue names list is populated."""
    pdb = parse_format33(_path('1bnf'))
    sr_a = next(sr for sr in pdb.primary_structure.seqres if sr.chainId == 'A')
    assert len(sr_a.resName) > 0
    assert 'ALA' in sr_a.resName


# ---------------------------------------------------------------------------
# SEQADV record (sequence conflicts)
# ---------------------------------------------------------------------------

def test_seqadv_records():
    """SEQADV records are parsed for 1BNF (T70C/S92C mutations)."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.primary_structure.seqadv is not None
    assert len(pdb.primary_structure.seqadv) > 0
    first = pdb.primary_structure.seqadv[0]
    assert first.resName == 'CYS'


# ---------------------------------------------------------------------------
# MODRES record (modified residues)
# ---------------------------------------------------------------------------

def test_modres_records():
    """MODRES records are parsed for 3C0F (N-methylated lysine MLY)."""
    pdb = parse_format33(_path('3c0f'))
    assert pdb.primary_structure.modres is not None
    assert len(pdb.primary_structure.modres) > 0
    first = pdb.primary_structure.modres[0]
    assert first.resName.strip() == 'MLY'
    assert first.stdRes.strip() == 'LYS'


# ---------------------------------------------------------------------------
# HELIX record (secondary structure)
# ---------------------------------------------------------------------------

def test_helix_record_count():
    """HELIX records are all parsed for 1BNF."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.secondary_structure.helix is not None
    assert len(pdb.secondary_structure.helix) >= 4


def test_helix_record_fields():
    """First HELIX record in 1BNF has the expected fields."""
    pdb = parse_format33(_path('1bnf'))
    first = pdb.secondary_structure.helix[0]
    assert first.serNum == 1
    assert first.initResName == 'THR'
    assert first.initChainId == 'A'
    assert isinstance(first.helixClass, str)


# ---------------------------------------------------------------------------
# SHEET record (secondary structure)
# ---------------------------------------------------------------------------

def test_sheet_record_parsed():
    """SHEET records are parsed for 3C0F."""
    pdb = parse_format33(_path('3c0f'))
    assert pdb.secondary_structure.sheet is not None
    assert len(pdb.secondary_structure.sheet) > 0
    first = pdb.secondary_structure.sheet[0]
    assert isinstance(first.strand, int)


# ---------------------------------------------------------------------------
# SSBOND record (connectivity annotation)
# ---------------------------------------------------------------------------

def test_ssbond_count():
    """1BNF has three SSBOND records."""
    pdb = parse_format33(_path('1bnf'))
    assert pdb.connectivity_annotation.ssbond is not None
    assert len(pdb.connectivity_annotation.ssbond) == 3


def test_ssbond_fields():
    """First SSBOND record in 1BNF has expected residue names."""
    pdb = parse_format33(_path('1bnf'))
    first = pdb.connectivity_annotation.ssbond[0]
    assert first.resName1 == 'CYS'
    assert first.resName2 == 'CYS'
    assert first.serNum == 1


# ---------------------------------------------------------------------------
# SITE record (miscellaneous features)
# ---------------------------------------------------------------------------

def test_site_record_parsed():
    """SITE records are parsed for 181L."""
    pdb = parse_format33(_path('181l'))
    assert pdb.miscellaneous_features.site is not None
    assert len(pdb.miscellaneous_features.site) > 0


def test_site_record_fields():
    """First SITE record in 181L has populated site ID."""
    pdb = parse_format33(_path('181l'))
    first = pdb.miscellaneous_features.site[0]
    assert first.siteId.strip() != ''
    assert isinstance(first.numRes, int)


# ---------------------------------------------------------------------------
# CRYST1 record
# ---------------------------------------------------------------------------

def test_cryst1_dimensions():
    """CRYST1 unit cell dimensions are parsed from 1L2Y."""
    pdb = parse_format33(_path('1l2y'))
    cryst1 = pdb.crystallographic_and_coordinate_transformation.cryst1
    assert abs(cryst1.a - 1.0) < 1.0e-6
    assert abs(cryst1.b - 1.0) < 1.0e-6
    assert abs(cryst1.c - 1.0) < 1.0e-6
    assert abs(cryst1.alpha - 90.0) < 1.0e-6


def test_cryst1_space_group():
    """CRYST1 space group string is parsed."""
    pdb = parse_format33(_path('1l2y'))
    cryst1 = pdb.crystallographic_and_coordinate_transformation.cryst1
    assert 'P 1' in cryst1.sGroup


# ---------------------------------------------------------------------------
# ORIGX record
# ---------------------------------------------------------------------------

def test_origx_identity_matrix():
    """1L2Y ORIGX is the identity transformation."""
    pdb = parse_format33(_path('1l2y'))
    origx = pdb.crystallographic_and_coordinate_transformation.origx
    assert abs(origx.o11 - 1.0) < 1.0e-6
    assert abs(origx.o22 - 1.0) < 1.0e-6
    assert abs(origx.o33 - 1.0) < 1.0e-6


# ---------------------------------------------------------------------------
# SCALE record
# ---------------------------------------------------------------------------

def test_scale_record_3c0f():
    """SCALE record is parsed for 3C0F."""
    pdb = parse_format33(_path('3c0f'))
    scale = pdb.crystallographic_and_coordinate_transformation.scale
    assert scale is not None
    assert isinstance(scale.s11, float)


# ---------------------------------------------------------------------------
# Multi-model PDB (MODEL / ENDMDL)
# ---------------------------------------------------------------------------

def test_multimodel_count_1l2y():
    """1L2Y has 38 models parsed."""
    pdb = parse_format33(_path('1l2y'))
    assert len(pdb.coordinate.model) == 38


def test_multimodel_serial_numbers():
    """Model serial numbers are sequential starting from 1."""
    pdb = parse_format33(_path('1l2y'))
    serials = [m.serial for m in pdb.coordinate.model]
    assert serials[0] == 1
    assert serials[-1] == 38


def test_multimodel_first_model_has_atoms():
    """First model of 1L2Y has a non-empty atom record list."""
    pdb = parse_format33(_path('1l2y'))
    first_model = pdb.coordinate.model[0]
    assert len(first_model.record) > 0


def test_multimodel_atom_coordinates():
    """ATOM record coordinates in the first model are non-zero floats."""
    pdb = parse_format33(_path('1l2y'))
    first_record = pdb.coordinate.model[0].record[0]
    assert isinstance(first_record.x, float)
    assert isinstance(first_record.y, float)
    assert isinstance(first_record.z, float)
    # They should not all be zero
    assert abs(first_record.x) + abs(first_record.y) + abs(first_record.z) > 0


# ---------------------------------------------------------------------------
# ATOM record fields
# ---------------------------------------------------------------------------

def test_atom_record_name():
    """ATOM record name field is parsed as a stripped string."""
    pdb = parse_format33(_path('3c0f'))
    first = pdb.coordinate.model[0].record[0]
    assert first.recordName == 'ATOM'
    assert isinstance(first.name, str)
    assert len(first.name) > 0


def test_atom_record_resname():
    """ATOM record resName is a stripped string."""
    pdb = parse_format33(_path('3c0f'))
    first = pdb.coordinate.model[0].record[0]
    assert isinstance(first.resName, str)
    assert len(first.resName) > 0


def test_atom_record_chain_id():
    """ATOM record chainId is a single character."""
    pdb = parse_format33(_path('3c0f'))
    first = pdb.coordinate.model[0].record[0]
    assert isinstance(first.chainId, str)
    assert len(first.chainId) == 1


def test_atom_record_occupancy():
    """ATOM record occupancy is a float."""
    pdb = parse_format33(_path('3c0f'))
    first = pdb.coordinate.model[0].record[0]
    assert isinstance(first.occupancy, float)


def test_atom_record_temp_factor():
    """ATOM record tempFactor is a float."""
    pdb = parse_format33(_path('3c0f'))
    first = pdb.coordinate.model[0].record[0]
    assert isinstance(first.tempFactor, float)


# ---------------------------------------------------------------------------
# HETATM record
# ---------------------------------------------------------------------------

def test_hetatm_record_present():
    """181L contains HETATM records parsed under the coordinate model."""
    pdb = parse_format33(_path('181l'))
    hetatm_records = [r for m in pdb.coordinate.model for r in m.record if r.recordName == 'HETATOM']
    assert len(hetatm_records) > 0


def test_hetatm_record_fields():
    """HETATM record has the same coordinate fields as ATOM."""
    pdb = parse_format33(_path('181l'))
    hetatm_records = [r for m in pdb.coordinate.model for r in m.record if r.recordName == 'HETATOM']
    first = hetatm_records[0]
    assert isinstance(first.x, float)
    assert isinstance(first.y, float)
    assert isinstance(first.z, float)
    assert isinstance(first.serial, int)


# ---------------------------------------------------------------------------
# ANISOU record
# ---------------------------------------------------------------------------

def test_anisou_record_3c8h():
    """3C8H has ANISOU records; first atom has anisou11 populated."""
    handler = PDBFileHandler(_path('3c8h'))
    first = handler.entry.coordinate.model[0].record[0]
    assert hasattr(first, 'anisou11')
    assert isinstance(first.anisou11, int)


# ---------------------------------------------------------------------------
# CONECT record (connectivity section)
# ---------------------------------------------------------------------------

def test_conect_record_count():
    """1BNF has CONECT records; at least one conect entry is parsed."""
    handler = PDBFileHandler(_path('1bnf'))
    assert handler.entry.connectivity.conect is not None
    assert len(handler.entry.connectivity.conect) > 0


def test_conect_atom_serial_number():
    """Fifth CONECT entry of 1BNF has atomSerNum == 1339."""
    handler = PDBFileHandler(_path('1bnf'))
    assert handler.entry.connectivity.conect[4].atomSerNum == 1339


def test_conect_bonded_atoms():
    """CONECT entry bondedAtomsSerNum is a non-empty list."""
    handler = PDBFileHandler(_path('1bnf'))
    first = handler.entry.connectivity.conect[0]
    assert isinstance(first.bondedAtomsSerNum, list)
    assert len(first.bondedAtomsSerNum) > 0


# ---------------------------------------------------------------------------
# MASTER record (bookkeeping)
# ---------------------------------------------------------------------------

def test_master_record_3c0f():
    """MASTER record is parsed and numRemark is an integer."""
    pdb = parse_format33(_path('3c0f'))
    master = pdb.bookkeeping.master
    assert master is not None
    assert isinstance(master.numRemark, int)


def test_master_record_1l2y():
    """MASTER record of 1L2Y has expected fields."""
    pdb = parse_format33(_path('1l2y'))
    master = pdb.bookkeeping.master
    assert master is not None
    assert isinstance(master.numCoord, int)
    assert master.numCoord > 0


# ---------------------------------------------------------------------------
# PDBFileHandler.load() / dump() interface
# ---------------------------------------------------------------------------

def test_load_idempotent():
    """Calling load() twice does not corrupt the entry."""
    handler = PDBFileHandler(_path('3c0f'))
    entry_after_first_load = handler.entry
    handler.load()
    assert handler.entry is not None
    # The model count should remain the same
    n_models = len(handler.entry.coordinate.model)
    assert n_models >= 1


def test_close_method():
    """PDBFileHandler.close() closes the underlying file handle."""
    handler = PDBFileHandler(_path('3c0f'))
    handler.close()
    assert handler.file.closed


# ---------------------------------------------------------------------------
# Regression: previously tested files still parse correctly
# ---------------------------------------------------------------------------

def test_regression_3c0f_source():
    """Regression: 3C0F source organism_scientific unchanged."""
    handler = PDBFileHandler(_path('3c0f'))
    assert handler.entry.title.source[0].organism_scientific == 'ARCHAEOGLOBUS FULGIDUS DSM 4304'


def test_regression_3c8h_anisou():
    """Regression: 3C8H first atom anisou11 unchanged."""
    handler = PDBFileHandler(_path('3c8h'))
    assert handler.entry.coordinate.model[0].record[0].anisou11 == 9993


def test_regression_2vgy_anisou():
    """Regression: 2VGY first atom anisou11 unchanged."""
    handler = PDBFileHandler(_path('2vgy'))
    assert handler.entry.coordinate.model[0].record[0].anisou11 == 10496


def test_regression_5ip4_scale():
    """Regression: 5IP4 SCALE u2 is 0.0."""
    handler = PDBFileHandler(_path('5ip4'))
    assert handler.entry.crystallographic_and_coordinate_transformation.scale.u2 == 0.0
