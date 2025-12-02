from molsysmt._private.digestion import digest
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


@digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):
    n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
    if n_atoms is None:
        return None
    if is_all(indices):
        return np.arange(n_atoms, dtype=int).tolist()
    return np.array(indices, dtype=int).tolist()


@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('atom_id', None)
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('atom_name', None)
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('group_id', atoms.get('group_ig', None))
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('group_name', None)
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('chain_id', None)
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('entity_id', None)
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_formal_charge_from_atom(item, indices='all', skip_digestion=False):
    atoms = _atoms_dict(item)
    values = atoms.get('formal_charge', None)
    if values is None:
        return None
    arr = _normalize_list(values, _n_atoms_from_atoms(atoms))
    if is_all(indices):
        return arr.tolist()
    return arr[np.array(indices, dtype=int)].tolist()


@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    atoms = _atoms_dict(item)
    n_atoms = _n_atoms_from_atoms(atoms)
    if n_atoms is not None:
        return int(n_atoms)
    frames = _structures_list(item)
    if frames:
        for frame in frames:
            positions = frame.get('coordinates', None)
            if positions is not None:
                return int(len(positions))
    return None


@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):
    bonds = _bonds_dict(item)
    atom_pairs = bonds.get('atom_pairs', None)
    if atom_pairs is None:
        return None
    return len(atom_pairs)


@digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):
    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    if n_bonds is None:
        return None
    if is_all(indices):
        return np.arange(n_bonds, dtype=int).tolist()
    return np.array(indices, dtype=int).tolist()


@digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):
    n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    if (n_atoms is None) or (n_bonds is None):
        return None

    bonds = _bonds_dict(item)
    atom_pairs = np.array(bonds.get('atom_pairs', []), dtype=int)

    bonded = [[] for _ in range(n_atoms)]
    for a, b in atom_pairs:
        bonded[a].append(int(b))
        bonded[b].append(int(a))

    if is_all(indices):
        return bonded
    return [bonded[ii] for ii in np.array(indices, dtype=int)]


@digest(form=form)
def get_n_structures_from_system(item, skip_digestion=False):
    frames = _structures_list(item)
    return len(frames) if frames else None


@digest(form=form)
def get_coordinates_from_system(item, structure_indices='all', skip_digestion=False):
    n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
    frames = _structures_list(item)
    coords, available_indices = _reshape_coordinates(frames, n_atoms)
    if coords is None:
        return None

    if is_all(structure_indices):
        selected = coords
    else:
        selected_mask = np.isin(available_indices, structure_indices)
        selected = coords[selected_mask]

    if selected.size == 0:
        return None

    return puw.quantity(selected, 'nanometer')


@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    frames = _structures_list(item)
    if not frames:
        return None

    times = []
    for frame in frames:
        times.append(frame.get('time', None))

    if is_all(structure_indices):
        pass
    else:
        mask = np.array(structure_indices, dtype=int)
        if len(mask) < len(times):
            times = [times[ii] for ii in mask]

    if all(ii is None for ii in times):
        return None

    return puw.quantity(np.array(times, dtype=float), 'picosecond')
