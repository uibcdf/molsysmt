from mdtraj.core.residue_names import _AMINO_ACID_CODES
from mdtraj.core.residue_names import _WATER_RESIDUES
from mdtraj.core.residue_names import _SOLVENT_TYPES

_amino_acid_codes = _AMINO_ACID_CODES
_protein_residues = frozenset(_AMINO_ACID_CODES.keys())
_rna_residues = frozenset(['A', 'G', 'C', 'U', 'I'])
_dna_residues = frozenset(['DA', 'DG', 'DC', 'DT', 'DI'])
_water_residues = _WATER_RESIDUES
_ion_residues = _SOLVENT_TYPES

def residue2molecule_types(residue_name):

    tmp_type='unknown'

    if residue_name in _water_residues:
        tmp_type='water'
    elif residue_name in _protein_residues:
        tmp_type='protein'
    elif residue_name in _ion_residues:
        tmp_type='ion'
    elif residue_name in _dna_residues:
        tmp_type='dna'
    elif residue_name in _rna_residues:
        tmp_type='rna'

    return tmp_type
