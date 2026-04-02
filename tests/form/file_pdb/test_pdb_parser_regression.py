"""
Regression tests for PDB format-3.3 parser bugs fixed in March 2026.

Each test corresponds to a real PDB entry that previously caused a parse error:

  - 1ATP / 1CEN  AttributeError: 'HetnamRecord' object has no attribute 'hetSynonyms'
      Root cause: HETSYN loop used ``hetnam`` variable instead of ``hetsyn``;
                  HETNAM loop appended to ``pdb.heterogen.het`` instead of
                  ``pdb.heterogen.hetnam``.
  - 1YCR  ValueError: invalid literal for int() with base 10: ''
      Root cause: SOURCE/COMPND token parsing used ``.strip()[:-1]`` to strip the
                  trailing semicolon, but the last token in a SOURCE record can
                  lack a semicolon, leaving an empty string for ``int()``.
  - 2HGR  TypeError: 'NoneType' object is not callable
      Root cause: ``SplitRecord.idCode`` and ``ObslteRecord.rIdCode`` were
                  initialised to ``None``; the parser tried to call them as
                  functions instead of using ``.append()``.

1ATP, 1CEN, and 1YCR also have bcif.gz counterparts in molsysmt/data/bcif_gz/.
The PDB vs bcif.gz comparison tests verify that both parsers agree on atom and
group counts (chain counts can legitimately differ: the PDB format uses simpler
single-character chain IDs while mmCIF/bcif assigns separate chains to each
molecule instance).

2HGR is an obsolete entry (superseded by 4V4Z on 10-DEC-14) and has no
corresponding bcif.gz on RCSB; only the PDB regression test is provided.
"""

import pytest
import molsysmt as msm


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def molsys_1atp_pdb():
    return msm.convert(msm.systems['1ATP']['1atp.pdb'])


@pytest.fixture(scope='module')
def molsys_1atp_bcif():
    return msm.convert(msm.systems['1ATP']['1atp.bcif.gz'])


@pytest.fixture(scope='module')
def molsys_1cen_pdb():
    return msm.convert(msm.systems['1CEN']['1cen.pdb'])


@pytest.fixture(scope='module')
def molsys_1cen_bcif():
    return msm.convert(msm.systems['1CEN']['1cen.bcif.gz'])


@pytest.fixture(scope='module')
def molsys_1ycr_pdb():
    return msm.convert(msm.systems['1YCR']['1ycr.pdb'])


@pytest.fixture(scope='module')
def molsys_1ycr_bcif():
    return msm.convert(msm.systems['1YCR']['1ycr.bcif.gz'])


@pytest.fixture(scope='module')
def molsys_2hgr_pdb():
    return msm.convert(msm.systems['2HGR']['2hgr.pdb'])


# ---------------------------------------------------------------------------
# Regression: parse must not raise
# ---------------------------------------------------------------------------

def test_parse_1atp_no_error(molsys_1atp_pdb):
    """1ATP parses without AttributeError on HETSYN records."""
    assert molsys_1atp_pdb is not None


def test_parse_1cen_no_error(molsys_1cen_pdb):
    """1CEN parses without AttributeError on HETSYN records."""
    assert molsys_1cen_pdb is not None


def test_parse_1ycr_no_error(molsys_1ycr_pdb):
    """1YCR parses without ValueError on SOURCE MOL_ID without trailing semicolon."""
    assert molsys_1ycr_pdb is not None


def test_parse_2hgr_no_error(molsys_2hgr_pdb):
    """2HGR parses without TypeError on OBSLTE/SPLIT idCode fields."""
    assert molsys_2hgr_pdb is not None


# ---------------------------------------------------------------------------
# PDB vs bcif.gz parity: atom and group counts must match
# ---------------------------------------------------------------------------

def test_1atp_pdb_bcif_atom_count(molsys_1atp_pdb, molsys_1atp_bcif):
    """1ATP: PDB and bcif.gz parsers report the same number of atoms."""
    assert msm.get(molsys_1atp_pdb, element='system', n_atoms=True) == \
           msm.get(molsys_1atp_bcif, element='system', n_atoms=True)


def test_1atp_pdb_bcif_group_count(molsys_1atp_pdb, molsys_1atp_bcif):
    """1ATP: PDB and bcif.gz parsers report the same number of groups."""
    assert msm.get(molsys_1atp_pdb, element='system', n_groups=True) == \
           msm.get(molsys_1atp_bcif, element='system', n_groups=True)


def test_1cen_pdb_bcif_atom_count(molsys_1cen_pdb, molsys_1cen_bcif):
    """1CEN: PDB and bcif.gz parsers report the same number of atoms."""
    assert msm.get(molsys_1cen_pdb, element='system', n_atoms=True) == \
           msm.get(molsys_1cen_bcif, element='system', n_atoms=True)


def test_1cen_pdb_bcif_group_count(molsys_1cen_pdb, molsys_1cen_bcif):
    """1CEN: PDB and bcif.gz parsers report the same number of groups."""
    assert msm.get(molsys_1cen_pdb, element='system', n_groups=True) == \
           msm.get(molsys_1cen_bcif, element='system', n_groups=True)


def test_1ycr_pdb_bcif_atom_count(molsys_1ycr_pdb, molsys_1ycr_bcif):
    """1YCR: PDB and bcif.gz parsers report the same number of atoms."""
    assert msm.get(molsys_1ycr_pdb, element='system', n_atoms=True) == \
           msm.get(molsys_1ycr_bcif, element='system', n_atoms=True)


def test_1ycr_pdb_bcif_group_count(molsys_1ycr_pdb, molsys_1ycr_bcif):
    """1YCR: PDB and bcif.gz parsers report the same number of groups."""
    assert msm.get(molsys_1ycr_pdb, element='system', n_groups=True) == \
           msm.get(molsys_1ycr_bcif, element='system', n_groups=True)


# ---------------------------------------------------------------------------
# Sanity: absolute counts (guard against future regressions)
# ---------------------------------------------------------------------------

def test_1atp_pdb_absolute_counts(molsys_1atp_pdb):
    assert msm.get(molsys_1atp_pdb, element='system', n_atoms=True) == 3070
    assert msm.get(molsys_1atp_pdb, element='system', n_groups=True) == 462


def test_1cen_pdb_absolute_counts(molsys_1cen_pdb):
    assert msm.get(molsys_1cen_pdb, element='system', n_atoms=True) == 3048
    assert msm.get(molsys_1cen_pdb, element='system', n_groups=True) == 557


def test_1ycr_pdb_absolute_counts(molsys_1ycr_pdb):
    assert msm.get(molsys_1ycr_pdb, element='system', n_atoms=True) == 818
    assert msm.get(molsys_1ycr_pdb, element='system', n_groups=True) == 98


def test_2hgr_pdb_absolute_counts(molsys_2hgr_pdb):
    assert msm.get(molsys_2hgr_pdb, element='system', n_atoms=True) == 55628
    assert msm.get(molsys_2hgr_pdb, element='system', n_groups=True) == 4090


# ---------------------------------------------------------------------------
# 4V4Z: supersedes 2HGR; 149 640 atoms — exceeds PDB decimal serial limit.
# OpenMM writes serial > 99 999 as uppercase hex overflow (VMD-style).
# MolSysMT must decode hex serials via _parse_serial().
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def molsys_4v4z_bcif():
    return msm.convert(msm.systems['4V4Z']['4v4z.bcif.gz'])


@pytest.fixture(scope='module')
def molsys_4v4z_pdb():
    return msm.convert(msm.systems['4V4Z']['4v4z_openmm.pdb'])


def test_4v4z_bcif_loads(molsys_4v4z_bcif):
    """4V4Z bcif.gz loads correctly (large ribosome)."""
    assert molsys_4v4z_bcif is not None
    assert msm.get(molsys_4v4z_bcif, element='system', n_atoms=True) == 149640
    assert msm.get(molsys_4v4z_bcif, element='system', n_groups=True) == 10794


def test_4v4z_pdb_loads(molsys_4v4z_pdb):
    """4V4Z OpenMM PDB (hex-overflow serials) parses without error."""
    assert molsys_4v4z_pdb is not None
    assert msm.get(molsys_4v4z_pdb, element='system', n_atoms=True) == 149640
    assert msm.get(molsys_4v4z_pdb, element='system', n_groups=True) == 10794


def test_4v4z_pdb_bcif_atom_count(molsys_4v4z_pdb, molsys_4v4z_bcif):
    """4V4Z: PDB (hex serials) and bcif.gz parsers report the same atom count."""
    assert msm.get(molsys_4v4z_pdb, element='system', n_atoms=True) == \
           msm.get(molsys_4v4z_bcif, element='system', n_atoms=True)


def test_4v4z_pdb_bcif_group_count(molsys_4v4z_pdb, molsys_4v4z_bcif):
    """4V4Z: PDB (hex serials) and bcif.gz parsers report the same group count."""
    assert msm.get(molsys_4v4z_pdb, element='system', n_groups=True) == \
           msm.get(molsys_4v4z_bcif, element='system', n_groups=True)


# ---------------------------------------------------------------------------
# Regression: atom_type must be inferred from atom_name when PDB columns
# 76-78 (element symbol) are absent.  Files generated by AMBER/ptraj and
# similar tools omit this field; previously atom_type was left as None for
# every atom, breaking any flow that filters by atom_type.
# ---------------------------------------------------------------------------

@pytest.fixture(scope='module')
def molsys_md_1u19_pdb():
    """md_1u19.pdb is an AMBER-generated PDB without element symbols (cols 76-78)."""
    from pathlib import Path
    import molsysmt as msm
    p = Path(msm.__file__).parent / 'data' / 'pdb' / 'md_1u19.pdb'
    return msm.convert(str(p))


def test_atom_type_not_none_when_element_column_absent(molsys_md_1u19_pdb):
    """atom_type must be populated even when PDB element columns 76-78 are empty."""
    import numpy as np
    atom_types = np.array(msm.get(molsys_md_1u19_pdb, element='atom', atom_type=True), dtype=object)
    assert not any(t is None for t in atom_types), (
        "atom_type is None for some atoms in a PDB without element symbols; "
        "inference from atom_name is expected."
    )


def test_atom_type_matches_names_dict(molsys_md_1u19_pdb):
    """atom_type must match the names.py dictionary for every recognised atom_name."""
    import numpy as np
    from molsysmt.element.atom.names import atom as _names_dict
    atom_types = np.array(msm.get(molsys_md_1u19_pdb, element='atom', atom_type=True), dtype=object)
    atom_names = np.array(msm.get(molsys_md_1u19_pdb, element='atom', atom_name=True), dtype=object)
    mismatches = [
        (name, got, _names_dict[name])
        for name, got in zip(atom_names, atom_types)
        if name in _names_dict and got != _names_dict[name]
    ]
    assert not mismatches, (
        f"atom_type mismatch for {len(mismatches)} atoms: {mismatches[:10]}"
    )


# ---------------------------------------------------------------------------
# Regression: CAVEAT record with comment initialised as None caused
#   TypeError: unsupported operand type(s) for +=: 'NoneType' and 'str'
# Root cause: CaveatRecord.comment was initialised to None; the parser does
#   caveat.comment += line[10:80] which fails on the very first CAVEAT line.
# Fix: CaveatRecord.__init__ now sets self.comment = ''.
# Reproducer: 1byb.pdb (dogfooding session, 2026-04-02).
# ---------------------------------------------------------------------------

_MINIMAL_PDB_WITH_CAVEAT = """\
HEADER    HYDROLASE                               20-JAN-99   1BYB
CAVEAT     1BYB    GLC B 1 HAS WRONG CHIRALITY AT ATOM C1
ATOM      1  N   ALA A   1       1.000   1.000   1.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.520   1.000   1.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.000   2.000   1.000  1.00  0.00           C
ATOM      4  O   ALA A   1       1.500   3.100   1.000  1.00  0.00           O
ATOM      5  CB  ALA A   1       1.520   0.500   2.400  1.00  0.00           C
END
"""


def test_caveat_record_does_not_raise(tmp_path):
    """PDB files with a CAVEAT record must parse without TypeError."""
    pdb_file = tmp_path / "caveat_regression.pdb"
    pdb_file.write_text(_MINIMAL_PDB_WITH_CAVEAT)
    mol = msm.convert(str(pdb_file), to_form='molsysmt.MolSys')
    assert mol is not None
    assert msm.get(mol, element='system', n_atoms=True) == 5
