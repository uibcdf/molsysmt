#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np

form='openmm.CharmmCrdFile'


def _select(values, indices):
    values = np.asarray(values)
    return values.tolist() if is_all(indices) else values[indices].tolist()


def _atom_group_indices(item):
    output = []
    previous_key = None
    group_index = -1
    for segment_id, residue_id in zip(item.segid, item.resno):
        key = (segment_id, residue_id)
        if key != previous_key:
            group_index += 1
            previous_key = key
        output.append(group_index)
    return output


def _group_records(item):
    records = []
    previous_key = None
    for segment_id, residue_id, residue_name in zip(item.segid, item.resno, item.resname):
        key = (segment_id, residue_id)
        if key != previous_key:
            records.append((residue_id, residue_name))
            previous_key = key
    return records


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    return _select(np.arange(item.natom, dtype=np.int64), indices)


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    return _select(item.atomno, indices)


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    return _select(item.attype, indices)


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.element.atom import get_atom_type_from_atom_name

    values = [get_atom_type_from_atom_name(name) for name in item.attype]
    return _select(values, indices)


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):
    return _select(_atom_group_indices(item), indices)


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):
    return _select(item.resno, indices)


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):
    return _select(item.resname, indices)


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):
    from molsysmt.element.group import get_group_type_from_group_name

    values = [get_group_type_from_group_name(name, skip_digestion=True) for name in item.resname]
    return _select(values, indices)


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):
    return _select(np.arange(len(_group_records(item)), dtype=np.int64), indices)


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):
    return _select([record[0] for record in _group_records(item)], indices)


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):
    return _select([record[1] for record in _group_records(item)], indices)


@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):
    from molsysmt.element.group import get_group_type_from_group_name

    values = [
        get_group_type_from_group_name(record[1], skip_digestion=True)
        for record in _group_records(item)
    ]
    return _select(values, indices)

# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
