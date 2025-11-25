from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.ViewerJSON')
def append_structures(item, items, skip_digestion=False):
    """Append structures from other ViewerJSON items."""

    if not isinstance(items, (list, tuple)):
        items = [items]

    if 'estructures' not in item.data:
        existing_frames = item.data.pop('frames', [])
        item.data['estructures'] = existing_frames if isinstance(existing_frames, list) else []

    for other in items:
        if hasattr(other, "data"):
            other_structures = other.data.get('estructures', other.data.get('frames', []))
            item.data['estructures'].extend(deepcopy(other_structures))

    return item
