from molmodmt.utils.exceptions import *

from mdtraj.core.residue_names import _AMINO_ACID_CODES as _aminoacid_group_names_mdtraj
from mdtraj.core.residue_names import _WATER_RESIDUES as _water_group_names_mdtraj
from mdtraj.core.residue_names import _SOLVENT_TYPES as _solvent_group_names_mdtraj

types=['water', 'ion', 'cosolute', 'small_molecule', 'aminoacid', 'nucleotide']

aminoacid_names = list(_aminoacid_group_names_mdtraj)
water_names = list(_water_group_names_mdtraj)
ion_names = [ii for ii in _solvent_group_names_mdtraj if ii not in water_names]
rna_names = ['A', 'G', 'C', 'U', 'I']
dna_names = ['DA', 'DG', 'DC', 'DT', 'DI']
nucleotide_names = dna_names + rna_names

def name_to_type(name):

    tmp_type=None

    if name in water_names:
        tmp_type='water'
    elif name in aminoacid_names:
        tmp_type='aminoacid'
    elif name in ion_names:
        tmp_type='ion'
    elif name in nucleotide_names:
        tmp_type='nucleotide'

    return tmp_type

def is_water(name):
    return (name in water_names)

def is_ion(name):
    return (name in ion_names)

def is_cosolute(name):
    raise NotImplementedError

def is_small_molecule(name):
    raise NotImplementedError

def is_aminoacid(name):
    return (name in aminoacid_names)

def is_nucleotide(name):
    return (name in nucleotide_names)


