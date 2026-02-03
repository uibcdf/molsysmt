from molsysmt._private.arg_digestion import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.ViewerJSON')
def append_structures(item, items, skip_digestion=False):
    """Append structures from other ViewerJSON items."""

    if not isinstance(items, (list, tuple)):
        items = [items]

    if 'structures' not in item.data:
        if 'estructures' in item.data:
            item.data['structures'] = item.data.pop('estructures')
        else:
            existing_frames = item.data.pop('frames', [])
            item.data['structures'] = existing_frames if isinstance(existing_frames, list) else []

    for other in items:
        if hasattr(other, "data"):
            other_structures = other.data.get('structures', other.data.get('estructures', other.data.get('frames', [])))
            item.data['structures'].extend(deepcopy(other_structures))

    return item
