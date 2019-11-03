from molmodmt.utils.exceptions import *

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

def name_to_molecule_type(name):

    tmp_type='unknown'

    if name in water_residues:
        tmp_type='water'
    elif name in protein_residues:
        tmp_type='protein'
    elif name in ion_residues:
        tmp_type='ion'
    elif name in dna_residues:
        tmp_type='dna'
    elif name in rna_residues:
        tmp_type='rna'

    return tmp_type


def name_is_water(name):
    return (name in water_residues)

def name_is_ion(name):
    return (name in ion_residues)

def name_is_aminoacid(name):
    return (name in protein_residues)

def name_is_nucleotide(name):
    return ((name in dna_residues) or (name in rna_residues))

def MMTFDecoder_group_to_group_class(mmtf_group):

    molecule_type = name_to_molecule_type(mmtf_group['groupName'])
    if molecule_type == 'protein':
        return 'AminoAcid'
    elif molecule_type == 'dna':
        return 'Nucleotide'
    elif molecule_type == 'rna':
        return 'Nucleotide'
    elif molecule_type == 'ion':
        return 'Ion'
    elif molecule_type == 'water':
        return 'Water'
    else:
        return None

    pass
