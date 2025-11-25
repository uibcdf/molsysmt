from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from copy import deepcopy
import numpy as np


@digest(form='molsysmt.UniversalJSON')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """Extract a subset of atoms/estructures from a UniversalJSON."""

    if is_all(atom_indices) and is_all(structure_indices):
        return deepcopy(item) if copy_if_all else item

    new_item = deepcopy(item)
    _migrate_frames_key(new_item)
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

        frames = _estructures_list(new_item)
        sliced_frames = []
        for frame in frames:
            new_frame = deepcopy(frame)
            positions = new_frame.get('positions', new_frame.get('coordinates', None))
            if positions is not None:
                arr = np.array(positions)
                if arr.ndim > 1:
                    arr = arr[idx]
                new_frame['positions'] = arr.tolist()
            sliced_frames.append(new_frame)
        _set_estructures(new_item, sliced_frames)

    if not is_all(structure_indices):
        idx = set(structure_indices)
        frames = _estructures_list(new_item)
        kept_frames = [ff for ii, ff in enumerate(frames) if ii in idx]
        _set_estructures(new_item, kept_frames)

    return new_item


def _estructures_list(item):
    if 'estructures' in item.data or 'frames' in item.data:
        return item.data.get('estructures', item.data.get('frames', [])) or []
    coords_block = item.data.get('coordinates', {}) or {}
    if 'collections' in coords_block:
        collections = coords_block.get('collections', [])
        if collections:
            coll0 = collections[0] or {}
            return coll0.get('estructures', coll0.get('frames', [])) or []
    return []


def _set_estructures(item, frames):
    if 'estructures' in item.data or 'frames' in item.data:
        item.data.pop('frames', None)
        item.data['estructures'] = frames
    else:
        coords_block = item.data.setdefault('coordinates', {})
        collections = coords_block.setdefault('collections', [])
        if not collections:
            collections.append({})
        coll0 = collections[0]
        coll0.pop('frames', None)
        coll0['estructures'] = frames


def _migrate_frames_key(item):
    if 'estructures' not in item.data and 'frames' in item.data:
        item.data['estructures'] = item.data.pop('frames')
    coords_block = item.data.get('coordinates', {})
    if isinstance(coords_block, dict) and 'collections' in coords_block:
        collections = coords_block.get('collections', [])
        if collections:
            coll0 = collections[0]
            if isinstance(coll0, dict) and 'estructures' not in coll0 and 'frames' in coll0:
                coll0['estructures'] = coll0.pop('frames')
