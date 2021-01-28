from molsysmt._private_tools.exceptions import *
import numpy as np

from mdtraj.core.residue_names import _AMINO_ACID_CODES as _aminoacid_group_names_mdtraj
from mdtraj.core.residue_names import _WATER_RESIDUES as _water_group_names_mdtraj
from mdtraj.core.residue_names import _SOLVENT_TYPES as _solvent_group_names_mdtraj

types=['water', 'ion', 'cosolute', 'small molecule', 'aminoacid', 'nucleotide', 'lipid']

aminoacid_names = list(_aminoacid_group_names_mdtraj)
water_names = list(_water_group_names_mdtraj)
ion_names = [ii for ii in _solvent_group_names_mdtraj if ii not in water_names]
rna_names = ['A', 'G', 'C', 'U', 'I']
dna_names = ['DA', 'DG', 'DC', 'DT', 'DI']
lipid_names = ['POPC', 'DOPC', 'DSPC', 'DMPC']
nucleotide_names = dna_names + rna_names

def name_to_type(name):

    tmp_type = None

    if _name_is_type_water(name):
        tmp_type = 'water'
    elif _name_is_type_ion(name):
        tmp_type = 'ion'
    elif _name_is_type_cosolute(name):
        tmp_type = 'cosolute'
    elif _name_is_type_small_molecule(name):
        tmp_type = 'small_molecule'
    elif _name_is_type_aminoacid(name):
        tmp_type = 'aminoacid'
    elif _name_is_type_nucleotide(name):
        tmp_type ='nucleotide'
    elif _name_is_type_lipid(name):
        tmp_type = 'lipid'
    else:
        tmp_type = 'small molecule'

    return tmp_type

def _name_is_type_water(name):
    return (name in water_names)

def _name_is_type_ion(name):
    return (name in ion_names)

def _name_is_type_cosolute(name):
    return False

def _name_is_type_small_molecule(name):
    return False

def _name_is_type_aminoacid(name):
    return (name in aminoacid_names)

def _name_is_type_nucleotide(name):
    return (name in nucleotide_names)

def _name_is_type_lipid(name):
    return (name in lipid_names)

def group_type_from_group(item, indices='all'):

    from molsysmt import get
    group_names = get(item, target='group', indices=indices, group_name=True)
    output= np.vectorize(name_to_type)(group_names).astype('object')
    return output

