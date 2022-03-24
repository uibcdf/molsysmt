from molsysmt._private.exceptions import *
import numpy as np
from .aminoacid import name as aminoacid_names
from .water import name as water_names
from .ion import name as ion_names
from .nucleotide import name as nucleotide_names
from .lipid import name as lipid_names
from .cosolute import name as cosolute_names

types=['water', 'ion', 'cosolute', 'small molecule', 'aminoacid', 'nucleotide', 'lipid']

def name_to_type(name):

    tmp_type = None

    if _name_is_type_water(name):
        tmp_type = 'water'
    elif _name_is_type_ion(name):
        tmp_type = 'ion'
    elif _name_is_type_cosolute(name):
        tmp_type = 'cosolute'
    elif _name_is_type_small_molecule(name):
        tmp_type = 'small molecule'
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
    return (name in cosolute_names)

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

