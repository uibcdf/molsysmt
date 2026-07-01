from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form = 'molsysmt.ViewerJSON'


def _atoms_dict(item):
    return item.data.get('atoms', {}) or {}


def _bonds_dict(item):
    bonds = item.data.get('bonds', {}) or {}
    if isinstance(bonds, dict) and 'sets' in bonds:
        sets = bonds.get('sets', [])
        if sets:
            return sets[0] or {}
    return bonds


def _structures_list(item):
    frames = item.data.get('structures', item.data.get('estructures', item.data.get('frames', None)))
    if frames is None:
        return []
    return frames


def _n_atoms_from_atoms(atoms):
    for key in ('atom_id', 'atom_name', 'group_id', 'group_ig', 'group_name', 'chain_id', 'entity_id'):
        values = atoms.get(key, None)
        if values is not None:
            return len(values)
    return None


def _normalize_list(values, length):
    arr = np.array(values if values is not None else [], dtype=object)
    if length is None:
        length = arr.shape[0]
    if arr.shape[0] < length:
        arr = np.pad(arr, (0, length - arr.shape[0]), constant_values=None)
    elif arr.shape[0] > length:
        arr = arr[:length]
    return arr


def _reshape_coordinates(frames, n_atoms):
    coords = []
    structure_indices = []
    for idx, frame in enumerate(frames):
        positions = frame.get('coordinates', None)
        if positions is None:
            continue
        arr = np.array(positions, dtype=float)
        if n_atoms is None:
            n_atoms = arr.shape[0] if arr.ndim >= 2 else None
        if n_atoms is None:
            continue
        if arr.shape[0] < n_atoms:
            pad = np.full((n_atoms - arr.shape[0], 3), np.nan, dtype=float)
            arr = np.vstack((arr, pad))
        elif arr.shape[0] > n_atoms:
            arr = arr[:n_atoms]
        coords.append(arr)
        structure_indices.append(idx)
    if not coords:
        return None, None
    return np.stack(coords), structure_indices


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return _n_atoms_from_atoms(_atoms_dict(item)) or 0


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    bonds = _bonds_dict(item)
    pairs = bonds.get('atom_pairs', None)
    if pairs is not None:
        return len(pairs)
    index_a = bonds.get('indexA', None)
    if index_a is not None:
        return len(index_a)
    return 0


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices='all', skip_digestion=False):

    atoms = _atoms_dict(item)
    values = _normalize_list(atoms.get('formal_charge', None), get_n_atoms_from_system(item, skip_digestion=True))
    if is_all(indices):
        return values.tolist()
    return values[indices].tolist()


@arg_digest(form=form)
def get_partial_charge_from_atom(item, indices='all', skip_digestion=False):

    atoms = _atoms_dict(item)
    values = atoms.get('partial_charge', None)
    if values is None:
        return None
    values = _normalize_list(values, get_n_atoms_from_system(item, skip_digestion=True))
    if is_all(indices):
        return values.tolist()
    return values[indices].tolist()


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    if is_all(indices):
        return np.arange(n_bonds)
    return indices


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    bonds = _bonds_dict(item)
    values = _normalize_list(bonds.get('order', None), get_n_bonds_from_system(item, skip_digestion=True))
    if is_all(indices):
        return values.tolist()
    return values[indices].tolist()


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    bonds = _bonds_dict(item)
    values = bonds.get('type', None)
    if values is None:
        return None
    values = _normalize_list(values, get_n_bonds_from_system(item, skip_digestion=True))
    if is_all(indices):
        return values.tolist()
    return values[indices].tolist()


# List of functions to be imported
import types
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
