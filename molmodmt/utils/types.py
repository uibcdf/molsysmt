from mdtraj.core.residue_names import _AMINO_ACID_CODES
from mdtraj.core.residue_names import _WATER_RESIDUES
from mdtraj.core.residue_names import _SOLVENT_TYPES

amino_acid_codes = _AMINO_ACID_CODES
protein_residues = frozenset(_AMINO_ACID_CODES.keys())
rna_residues = frozenset(['A', 'G', 'C', 'U', 'I'])
dna_residues = frozenset(['DA', 'DG', 'DC', 'DT', 'DI'])
water_residues = _WATER_RESIDUES
ion_residues = _SOLVENT_TYPES

def residue2molecule_types(residue_name):

    tmp_type='unknown'

    if residue_name in water_residues:
        tmp_type='water'
    elif residue_name in protein_residues:
        tmp_type='protein'
    elif residue_name in ion_residues:
        tmp_type='ion'
    elif residue_name in dna_residues:
        tmp_type='dna'
    elif residue_name in rna_residues:
        tmp_type='rna'

    return tmp_type
