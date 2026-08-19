"""PDB atom names must occupy columns 13-16 the way the format specifies.

Guard for `uibcdf/molsysmt#174`. The wwPDB v3.3 ATOM record states: "Alignment of
one-letter atom name such as C starts at column 14, while two-letter atom name such
as FE starts at column 13."

The rule keys on the **element symbol**, not on the length of the name, and that is
the part that is easy to get wrong: the alpha carbon `CA` is element `C` and starts
at column 14, while the calcium ion `CA` is element `CA` and starts at column 13.
Writing every name from column 13 is what NGL.js fails to recognise as a backbone,
so a cartoon or ribbon representation renders nothing.

The strongest available assertion is a comparison against the RCSB files MolSysMT
ships: whatever the format says, those are what every consumer was written to read.
"""

import warnings

import pytest

import molsysmt as msm
from molsysmt.form.molsysmt_MolSys.to_string_pdb_text import _atom_name_field


def _atom_records(text):
    return [line for line in text.splitlines() if line.startswith(('ATOM', 'HETATM'))]


@pytest.mark.parametrize(
    ('system', 'filename'),
    [
        ('T4 lysozyme L99A', '181l.pdb'),   # protein, waters, chloride ions
        ('TcTIM', '1tcd.pdb'),              # two chains
        ('1ATP', '1atp.pdb'),               # TPO and SEP, magnesium, ATP
        ('1YCR', '1ycr.pdb'),
    ],
)
def test_atom_name_columns_match_the_rcsb_file(system, filename):
    """Round-tripping an RCSB file must reproduce its columns 13-16 exactly."""
    source = msm.systems[system][filename]
    with open(source) as handle:
        original = _atom_records(handle.read())

    with warnings.catch_warnings():
        warnings.simplefilter('ignore')
        molsys = msm.convert(source, to_form='molsysmt.MolSys')
        produced = _atom_records(msm.convert(molsys, to_form='string:pdb_text'))

    assert len(produced) == len(original)

    mismatched = [
        (index, line_in[12:16], line_out[12:16], line_in[76:78])
        for index, (line_in, line_out) in enumerate(zip(original, produced))
        if line_in[12:16] != line_out[12:16]
    ]
    assert not mismatched, (
        f'{len(mismatched)} atom names are aligned differently from the RCSB file. '
        f'First: index {mismatched[0][0]}, RCSB {mismatched[0][1]!r}, '
        f'produced {mismatched[0][2]!r}, element {mismatched[0][3]!r}.'
    )


@pytest.mark.parametrize(
    ('atom_name', 'element_symbol', 'expected'),
    [
        ('N', 'N', ' N  '),          # one-letter element: starts at column 14
        ('C', 'C', ' C  '),
        ('CA', 'C', ' CA '),         # alpha carbon — element is C, not CA
        ('CB', 'C', ' CB '),
        ('CL', 'CL', 'CL  '),        # chloride — two-letter element, column 13
        ('FE', 'FE', 'FE  '),        # the example the specification itself gives
        ('MG', 'MG', 'MG  '),
        ('HG11', 'H', 'HG11'),       # four characters fill the field
        ('1HB', 'H', ' 1HB'),
        ('O', '', ' O  '),           # no element declared: assume one letter
    ],
)
def test_the_alignment_rule_case_by_case(atom_name, element_symbol, expected):
    """The cases the RCSB round trip does not necessarily contain.

    `CA` against `CL` is the pair that matters: two names of the same length that
    align differently, because one is a carbon and the other a chlorine.
    """
    assert _atom_name_field(atom_name, element_symbol) == expected
    assert len(_atom_name_field(atom_name, element_symbol)) == 4
