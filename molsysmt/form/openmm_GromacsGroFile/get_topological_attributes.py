#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.GromacsGroFile'


def _build_group_info(item):
    """Return (group_index_per_atom, group_ids, group_names) from consecutive residue grouping."""
    group_index_per_atom = []
    group_ids = []
    group_names = []
    prev = None
    g_idx = -1
    for resid, resname in zip(item.residueIds, item.residueNames):
        curr = (resid, resname)
        if curr != prev:
            g_idx += 1
            group_ids.append(str(resid))
            group_names.append(resname)
            prev = curr
        group_index_per_atom.append(g_idx)
    return np.array(group_index_per_atom), group_ids, group_names


## atom

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    n_atoms = len(item.atomNames)
    output = np.arange(n_atoms)
    if not is_all(indices):
        output = output[indices]
    return output

@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    output = np.array(item.atomNames)
    if not is_all(indices):
        output = output[indices]
    return output.tolist()

@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    group_index_per_atom, _, _ = _build_group_info(item)
    if not is_all(indices):
        group_index_per_atom = group_index_per_atom[indices]
    return group_index_per_atom.tolist()

@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    group_index_per_atom, group_ids, _ = _build_group_info(item)
    if not is_all(indices):
        group_index_per_atom = group_index_per_atom[indices]
    return [group_ids[i] for i in group_index_per_atom]

@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    group_index_per_atom, _, group_names = _build_group_info(item)
    if not is_all(indices):
        group_index_per_atom = group_index_per_atom[indices]
    return [group_names[i] for i in group_index_per_atom]

@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.element.group import get_group_type_from_group_name
    group_index_per_atom, _, group_names = _build_group_info(item)
    if not is_all(indices):
        group_index_per_atom = group_index_per_atom[indices]
    return [get_group_type_from_group_name(group_names[i]) for i in group_index_per_atom]


## group

@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', structure_indices='all', skip_digestion=False):

    _, group_ids, _ = _build_group_info(item)
    if not is_all(indices):
        return [group_ids[i] for i in indices]
    return group_ids

@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', structure_indices='all', skip_digestion=False):

    _, _, group_names = _build_group_info(item)
    if not is_all(indices):
        return [group_names[i] for i in indices]
    return group_names

@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.element.group import get_group_type_from_group_name
    _, _, group_names = _build_group_info(item)
    if not is_all(indices):
        group_names = [group_names[i] for i in indices]
    return [get_group_type_from_group_name(name) for name in group_names]


## system

@arg_digest(form=form)
def get_n_atoms_from_system(item, structure_indices='all', skip_digestion=False):

    return len(item.atomNames)

@arg_digest(form=form)
def get_n_groups_from_system(item, structure_indices='all', skip_digestion=False):

    group_index_per_atom, _, _ = _build_group_info(item)
    return int(group_index_per_atom[-1]) + 1


# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
