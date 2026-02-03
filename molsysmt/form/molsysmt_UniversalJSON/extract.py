from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from copy import deepcopy
import numpy as np


@arg_digest(form='molsysmt.UniversalJSON')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """Extract a subset of atoms/structures from a UniversalJSON."""

    if is_all(atom_indices) and is_all(structure_indices):
        return deepcopy(item) if copy_if_all else item

    new_item = deepcopy(item)
    _migrate_structures_key(new_item)
    topology = new_item.data.get('topology', {})
    atoms_block = topology.get('atoms', new_item.data.get('atoms', {}))

    if not is_all(atom_indices):
        idx = np.array(atom_indices, dtype=int)
        for key, values in list(atoms_block.items()):
            try:
                atoms_block[key] = list(np.array(values)[idx])
            except Exception:
                pass
        if 'atoms' in topology:
            new_item.data['topology']['atoms'] = atoms_block
        else:
            new_item.data['atoms'] = atoms_block

        frames = _structures_list(new_item)
        sliced_frames = []
        for frame in frames:
            new_frame = deepcopy(frame)
            coords = new_frame.get('coordinates', new_frame.get('positions', None))
            if coords is not None:
                arr = np.array(coords)
                if arr.ndim > 1:
                    arr = arr[idx]
                new_frame['coordinates'] = arr.tolist()
                new_frame.pop('positions', None)
            sliced_frames.append(new_frame)
        _set_structures(new_item, sliced_frames)

    if not is_all(structure_indices):
        idx = set(structure_indices)
        frames = _structures_list(new_item)
        kept_frames = [ff for ii, ff in enumerate(frames) if ii in idx]
        _set_structures(new_item, kept_frames)

    return new_item


def _structures_list(item):
    coords_block = item.data.get('coordinates', {}) or {}
    if 'collections' in coords_block:
        collections = coords_block.get('collections', [])
        if collections:
            coll0 = collections[0] or {}
            return coll0.get('structures', coll0.get('estructures', coll0.get('frames', []))) or []
    return []


def _set_structures(item, frames):
    coords_block = item.data.setdefault('coordinates', {})
    collections = coords_block.setdefault('collections', [])
    if not collections:
        collections.append({"label": "default"})
    coll0 = collections[0]
    coll0.pop('frames', None)
    coll0.pop('estructures', None)
    coll0['structures'] = frames


def _migrate_structures_key(item):
    coords_block = item.data.get('coordinates', {})
    if isinstance(coords_block, dict) and 'collections' in coords_block:
        collections = coords_block.get('collections', [])
        if collections:
            coll0 = collections[0]
            if isinstance(coll0, dict):
                if 'structures' not in coll0 and 'estructures' in coll0:
                    coll0['structures'] = coll0.pop('estructures')
                if 'structures' not in coll0 and 'frames' in coll0:
                    coll0['structures'] = coll0.pop('frames')
