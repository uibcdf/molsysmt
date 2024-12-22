from molsysmt._private.digestion import digest
from .water import is_water
from .ion import is_ion
from .small_molecule import is_small_molecule, small_molecule_is_amino_acid
from .amino_acid import is_amino_acid
from .terminal_capping import is_terminal_capping
from .nucleotide import is_nucleotide
from .lipid import is_lipid
from .saccharide import is_saccharide
import numpy as np


@digest()
def get_group_type(molecular_system, element='atom', selection='all', redefine_types=False, syntax='MolSysMT',
                   skip_digestion=False):

    from molsysmt.basic import get

    if redefine_types:

        if element == 'atom':

            group_names_from_atom = get(molecular_system, element='atom', selection=selection,
                                        syntax=syntax, group_name=True)
            unique_group_names = np.unique(group_names_from_atom)
            aux_dict = {}
            for name in unique_group_names:
                tmp_group_type = get_group_type_from_group_name(name)
                if tmp_group_type == 'small molecule':
                    if _small_molecule_is_amino_acid(molecular_system, name):
                        tmp_group_type = 'amino acid'
                aux_dict[name] = tmp_group_type

            output = [aux_dict[ii] for ii in group_names_from_atom]

        elif element == 'group':

            group_names_from_group = get(molecular_system, element='group', selection=selection, syntax=syntax,
                                        group_name=True)
            unique_group_names = np.unique(group_names_from_group)
            aux_dict = {}
            for name in unique_group_names:
                tmp_group_type = get_group_type_from_group_name(name)
                if tmp_group_type == 'small molecule':
                    if _small_molecule_is_amino_acid(molecular_system, group_index):
                        tmp_group_type = 'amino acid'
                aux_dict[name] = get_group_type_from_group_name(name)

            output = [aux_dict[ii] for ii in group_names_from_group]

        elif element == 'component':

            raise NotImplementedError

        else:

            raise NotImplementedError

    else:


        output = get(molecular_system, element=element, selection=selection, syntax=syntax,
                     group_type=True)

    return output


def get_group_type_from_group_name(group_name, skip_digestion=False):

    output = None

    if is_water(group_name):
        output = 'water'
    elif is_ion(group_name):
        output = 'ion'
    elif is_amino_acid(group_name):
        output = 'amino acid'
    elif is_terminal_capping(group_name):
        output = 'terminal capping'
    elif is_nucleotide(group_name):
        output = 'nucleotide'
    elif is_small_molecule(group_name):
        output = 'small molecule'
    elif is_lipid(group_name):
        output = 'lipid'
    elif is_saccharide(group_name):
        output = 'saccharide'

    return output

