from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.UniversalJSON')
def append_structures(item, items, skip_digestion=False):
    """Append structures from other UniversalJSON items."""

    if not isinstance(items, (list, tuple)):
        items = [items]

    frames_holder = None
    if 'estructures' in item.data or 'frames' in item.data:
        existing = item.data.pop('frames', [])
        frames_holder = item.data.setdefault('estructures', existing if isinstance(existing, list) else [])
    else:
        coords_block = item.data.setdefault('coordinates', {})
        collections = coords_block.setdefault('collections', [])
        if not collections:
            collections.append({})
        coll0 = collections[0]
        if 'estructures' not in coll0 and 'frames' in coll0:
            coll0['estructures'] = coll0.pop('frames')
        frames_holder = coll0.setdefault('estructures', [])

    for other in items:
        if hasattr(other, "data"):
            other_frames = []
            if 'estructures' in other.data or 'frames' in other.data:
                other_frames = other.data.get('estructures', other.data.get('frames', []))
            else:
                coords_block = other.data.get('coordinates', {}) or {}
                if 'collections' in coords_block and coords_block.get('collections'):
                    coll0 = coords_block['collections'][0] or {}
                    other_frames = coll0.get('estructures', coll0.get('frames', []))
            frames_holder.extend(deepcopy(other_frames))

    return item
