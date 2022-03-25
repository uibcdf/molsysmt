from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_Topology import is_molsysmt_Topology

def to_string_aminoacids3(item, group_indices='all', check=True):

    if check:

        try:
            is_molsysmt_Topology(item)
        except:
            raise WrongFormError('molsysmt.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from . import get_group_name_from_group

    group_names = get_group_name_from_group(item, indices=group_indices, check=False)
    tmp_item = ''.join([ii.title() for ii in group_names])

    return tmp_item

