from molsysmt._private.digestion import digest
from molsysmt.native import MolSys, Topology, Structures
from molsysmt import pyunitwizard as puw
from molsysmt.pbc import get_box_from_lengths_and_angles
import numpy as np
import pandas as pd


def _safe_array(values, length, dtype=object):
    arr = np.array(values if values is not None else [], dtype=dtype)
    if length is None:
        return arr
    if arr.shape[0] < length:
        pad_width = [(0, length - arr.shape[0])]
        arr = np.pad(arr, pad_width, constant_values=None)
    elif arr.shape[0] > length:
        arr = arr[:length]
    return arr


def _group_indices_from_ids(ids):
    ids_clean = [ii for ii in ids if ii is not None]
    if not ids_clean:
        return [0] * len(ids), [None]
    unique_ids = list(pd.unique(ids_clean))
    mapping = {gid: idx for idx, gid in enumerate(unique_ids)}
    return [mapping.get(ii, 0) for ii in ids], unique_ids


def _chain_indices_from_ids(ids):
    ids_clean = [ii for ii in ids if ii is not None]
    if not ids_clean:
        return [0] * len(ids), [None]
    unique_ids = list(pd.unique(ids_clean))
    mapping = {cid: idx for idx, cid in enumerate(unique_ids)}
    return [mapping.get(ii, 0) for ii in ids], unique_ids


def _box_dict_to_array(box_dict):
    """Convert box dictionary to 3x3 numpy array."""
    if box_dict is None:
        return None
    if all(key in box_dict for key in ('v0', 'v1', 'v2')):
        return np.array([box_dict['v0'], box_dict['v1'], box_dict['v2']], dtype=float)
    if all(key in box_dict for key in ('length_v0', 'length_v1', 'length_v2', 'angle_v1_v2', 'angle_v0_v2', 'angle_v0_v1')):
        lengths = puw.quantity(np.array([box_dict['length_v0'], box_dict['length_v1'], box_dict['length_v2']], dtype=float), 'nanometer')
        angles = puw.quantity(np.array([box_dict['angle_v1_v2'], box_dict['angle_v0_v2'], box_dict['angle_v0_v1']], dtype=float), 'radian')
        box = get_box_from_lengths_and_angles(lengths, angles, skip_digestion=True)
        return np.asarray(puw.get_value(box, to_unit='nanometer'))
    return None


def _collect_coordinates(frames, n_atoms):
    if not frames:
        return None, None, None
    coords = []
    times = []
    boxes = []
    for frame in frames:
        positions = frame.get('coordinates', None)
        if positions is None:
            continue
        arr = np.array(positions, dtype=float)
        if n_atoms is not None:
            if arr.shape[0] < n_atoms:
                pad = np.full((n_atoms - arr.shape[0], 3), np.nan, dtype=float)
                arr = np.vstack((arr, pad))
            elif arr.shape[0] > n_atoms:
                arr = arr[:n_atoms]
        coords.append(arr)
        times.append(frame.get('time', None))
        boxes.append(_box_dict_to_array(frame.get('box', None)))
    if not coords:
        return None, None, None
    coords = np.stack(coords)
    times = np.array(times, dtype=float)
    box_array = None
    if boxes and all(box is not None for box in boxes):
        box_array = np.stack(boxes)
    return (
        puw.quantity(coords, 'nanometer'),
        puw.quantity(times, 'picosecond'),
        puw.quantity(box_array, 'nanometer') if box_array is not None else None,
    )


@digest(form='molsysmt.ViewerJSON')
def to_molsysmt_MolSys(item, skip_digestion=False):
    """Convert a ViewerJSON object into a native MolSys."""

    atoms = item.data.get('atoms', {}) or {}
    frames = item.data.get('structures', item.data.get('estructures', item.data.get('frames', []))) or []
    bonds = item.data.get('bonds', {}) or {}

    # Atom-level fields
    atom_id = _safe_array(atoms.get('atom_id', None), None, dtype=object)
    atom_name = _safe_array(atoms.get('atom_name', None), len(atom_id) or None, dtype=object)
    group_id_raw = _safe_array(atoms.get('group_id', atoms.get('group_ig', None)), len(atom_name) or None, dtype=object)
    group_name = _safe_array(atoms.get('group_name', None), len(atom_name) or None, dtype=object)
    chain_id_raw = _safe_array(atoms.get('chain_id', None), len(atom_name) or None, dtype=object)
    entity_id_raw = _safe_array(atoms.get('entity_id', None), len(atom_name) or None, dtype=object)
    formal_charge = _safe_array(atoms.get('formal_charge', None), len(atom_name) or None, dtype=object)

    n_atoms = len(atom_name) if atom_name is not None else len(atom_id)
    if n_atoms is None:
        n_atoms = 0

    group_indices, unique_group_ids = _group_indices_from_ids(group_id_raw.tolist())
    chain_indices, unique_chain_ids = _chain_indices_from_ids(chain_id_raw.tolist())

    topo = Topology(
        n_atoms=n_atoms,
        n_groups=max(len(unique_group_ids), 1),
        n_components=max(len(unique_group_ids), 1),
        n_molecules=max(len(unique_group_ids), 1),
        n_entities=max(len(entity_id_raw) if entity_id_raw is not None else 1, 1),
        n_chains=max(len(unique_chain_ids), 1),
        n_bonds=len(bonds.get('atom_pairs', [])) if bonds else 0,
        skip_digestion=True,
    )

    topo.atoms['atom_id'] = pd.Series(atom_id, dtype='Int64')
    topo.atoms['atom_name'] = pd.Series(atom_name, dtype=str)
    topo.atoms['group_index'] = pd.Series(group_indices, dtype='Int64')
    topo.atoms['component_index'] = pd.Series(group_indices, dtype='Int64')
    topo.atoms['chain_index'] = pd.Series(chain_indices, dtype='Int64')

    topo.groups['group_id'] = pd.Series(unique_group_ids, dtype='Int64')
    topo.groups['group_name'] = pd.Series(group_name[:len(unique_group_ids)], dtype=str)
    topo.groups['group_type'] = pd.Series([''] * len(unique_group_ids), dtype=str)
    topo.groups['molecule_index'] = pd.Series(np.zeros(len(unique_group_ids), dtype=int), dtype='Int64')

    topo.components['component_id'] = pd.Series(unique_group_ids, dtype='Int64')
    topo.components['component_name'] = pd.Series(group_name[:len(unique_group_ids)], dtype=str)
    topo.components['component_type'] = pd.Series([''] * len(unique_group_ids), dtype=str)

    topo.molecules['molecule_id'] = pd.Series(np.arange(len(unique_group_ids)), dtype='Int64')
    topo.molecules['molecule_name'] = pd.Series([''] * len(unique_group_ids), dtype=str)
    topo.molecules['molecule_type'] = pd.Series([''] * len(unique_group_ids), dtype=str)
    topo.molecules['entity_index'] = pd.Series(np.zeros(len(unique_group_ids), dtype=int), dtype='Int64')

    topo.entities['entity_id'] = pd.Series(entity_id_raw, dtype='Int64')
    topo.entities['entity_name'] = pd.Series([''] * len(topo.entities), dtype=str)
    topo.entities['entity_type'] = pd.Series([''] * len(topo.entities), dtype=str)

    topo.chains['chain_id'] = pd.Series(unique_chain_ids, dtype='Int64')
    topo.chains['chain_name'] = pd.Series([''] * len(unique_chain_ids), dtype=str)
    topo.chains['chain_type'] = pd.Series([''] * len(unique_chain_ids), dtype=str)

    if bonds:
        atom_pairs = bonds.get('atom_pairs', [])
        atom1_index = [pair[0] for pair in atom_pairs]
        atom2_index = [pair[1] for pair in atom_pairs]
        topo.bonds['atom1_index'] = pd.Series(atom1_index, dtype='Int64')
        topo.bonds['atom2_index'] = pd.Series(atom2_index, dtype='Int64')
        topo.bonds['order'] = pd.Series(bonds.get('order', []), dtype=str)

    coordinates, times, boxes = _collect_coordinates(frames, n_atoms if n_atoms > 0 else None)
    structures = Structures(
        coordinates=coordinates,
        time=times,
        box=boxes,
        skip_digestion=True,
    )

    molsys = MolSys(skip_digestion=True)
    molsys.topology = topo
    molsys.structures = structures
    molsys.molecular_mechanics = molsys.molecular_mechanics.copy()

    return molsys
