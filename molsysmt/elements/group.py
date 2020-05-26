from molsysmt.utils.exceptions import *

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

    if name_is_type_water(name):
        tmp_type='water'
    elif name_is_type_ion(name):
        tmp_type='ion'
    elif name_is_type_cosolute(name):
        tmp_type='cosolute'
    elif name_is_type_small_molecule(name):
        tmp_type='small_molecule'
    elif name_is_type_aminoacid(name):
        tmp_type='aminoacid'
    elif name_is_type_nucleoatide(name):
        tmp_type='nucleotide'

    return tmp_type

def name_is_type_water(name):
    return (name in water_names)

def name_is_type_ion(name):
    return (name in ion_names)

def name_is_type_cosolute(name):
    #NotImplementedError
    return False

def name_is_type_small_molecule(name):
    #NotImplementedError
    return False

def name_is_type_aminoacid(name):
    return (name in aminoacid_names)

def name_is_type_nucleotide(name):
    return (name in nucleotide_names)

def is_type(item, indices='all', selection=None, syntaxis='MolSysMT'):

    from molsysmt import select, get

    if selection is not None:
        indices = select(item, target='group', selection=selection, syntaxis=syntaxis)

    group_names = get(item, target='group', indices=indices, group_name=True)

    return list(map(name_to_type,group_names))

def name_is_in_molecule_type():

    tmp_type=None

    if name_is_type_water(name):
        tmp_type='water'
    elif name_is_type_ion(name):
        tmp_type='ion'
    elif name_is_type_cosolute(name):
        tmp_type='cosolute'
    elif name_is_type_small_molecule(name):
        tmp_type='small_molecule'
    elif name_is_type_aminoacid(name):
        tmp_type='peptide or protein'
    elif name_is_type_nucleoatide(name):
        if name in rna_names:
            tmp_type='rna'
        elif name in dna_names:
            tmp_type='dna'

    return tmp_type

