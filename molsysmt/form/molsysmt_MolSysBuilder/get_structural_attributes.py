from molsysmt._private.arg_digestion import arg_digest
import numpy as np
import types

form = "molsysmt.MolSysBuilder"


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return item.topology.n_atoms


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    if structure_indices == "all":
        return item.n_structures
    return len(structure_indices)


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    values = item.structures.structure_id
    if values is None:
        return []
    values = np.asarray(values)
    if structure_indices == "all":
        return values.tolist()
    return values[structure_indices].tolist()


@arg_digest(form=form)
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    values = item.structures.time
    if values is None:
        return None
    if structure_indices == "all":
        return values
    return values[structure_indices]


@arg_digest(form=form)
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    values = item.structures.box
    if values is None:
        return None
    if structure_indices == "all":
        return values
    return values[structure_indices]


@arg_digest(form=form)
def get_coordinates_from_system(item, structure_indices="all", skip_digestion=False):
    values = item.structures.coordinates
    if values is None:
        return None
    if structure_indices == "all":
        return values
    return values[structure_indices]


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith("get_")]
