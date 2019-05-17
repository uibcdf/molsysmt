from .utils.exceptions import *

from mdtraj.core.residue_names import _AMINO_ACID_CODES
from mdtraj.core.residue_names import _WATER_RESIDUES
from mdtraj.core.residue_names import _SOLVENT_TYPES

amino_acid_codes = _AMINO_ACID_CODES
protein_residues = frozenset(_AMINO_ACID_CODES.keys())
rna_residues = frozenset(['A', 'G', 'C', 'U', 'I'])
dna_residues = frozenset(['DA', 'DG', 'DC', 'DT', 'DI'])
water_residues = _WATER_RESIDUES
solvent_residues = _SOLVENT_TYPES
ion_residues = frozenset([ii for ii in solvent_residues if ii not in water_residues])

def residue_name_to_molecule_type(residue_name):

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


def is_water(residue_name):
    return (residue_name in water_residues)

def is_ion(residue_name):
    return (residue_name in ion_residues)

def is_aminoacid(residue_name):
    return (residue_name in protein_residues)

def is_nucleotide(residue_name):
    return ((residue_name in dna_residues) or (residue_name in rna_residues))

