from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.UniversalJSON')
def append_structures(item, items, skip_digestion=False):
    """Append structures from other UniversalJSON items."""

    if not isinstance(items, (list, tuple)):
        items = [items]

    coords_block = item.data.setdefault('coordinates', {})
    collections = coords_block.setdefault('collections', [])
    if not collections:
        collections.append({"label": "default"})
    coll0 = collections[0]
    # migrate legacy keys
    if 'estructures' in coll0:
        coll0['structures'] = coll0.pop('estructures')
    if 'frames' in coll0:
        coll0['structures'] = coll0.pop('frames')
    frames_holder = coll0.setdefault('structures', [])

    for other in items:
        if hasattr(other, "data"):
            other_coords = other.data.get('coordinates', {}) or {}
            other_collections = other_coords.get('collections', [])
            if other_collections:
                other_coll0 = other_collections[0] or {}
                if 'estructures' in other_coll0:
                    other_coll0 = {**other_coll0, "structures": other_coll0.get('estructures')}
                if 'frames' in other_coll0:
                    other_coll0 = {**other_coll0, "structures": other_coll0.get('frames')}
                other_frames = other_coll0.get('structures', [])
                frames_holder.extend(deepcopy(other_frames))

    return item
