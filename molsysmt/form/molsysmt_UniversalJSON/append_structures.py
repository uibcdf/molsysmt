from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.UniversalJSON')
def append_structures(item, items, skip_digestion=False):
    """Append frames from other UniversalJSON items."""

    if not isinstance(items, (list, tuple)):
        items = [items]

    frames_holder = None
    if 'frames' in item.data:
        frames_holder = item.data.setdefault('frames', [])
    else:
        coords_block = item.data.setdefault('coordinates', {})
        collections = coords_block.setdefault('collections', [])
        if not collections:
            collections.append({})
        frames_holder = collections[0].setdefault('frames', [])

    for other in items:
        if hasattr(other, "data"):
            other_frames = []
            if 'frames' in other.data:
                other_frames = other.data.get('frames', [])
            else:
                coords_block = other.data.get('coordinates', {}) or {}
                if 'collections' in coords_block and coords_block.get('collections'):
                    other_frames = coords_block['collections'][0].get('frames', [])
            frames_holder.extend(deepcopy(other_frames))

    return item
