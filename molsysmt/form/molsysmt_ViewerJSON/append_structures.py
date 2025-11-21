from molsysmt._private.digestion import digest
from copy import deepcopy


@digest(form='molsysmt.ViewerJSON')
def append_structures(item, items, skip_digestion=False):
    """Append frames from other ViewerJSON items."""

    if not isinstance(items, (list, tuple)):
        items = [items]

    if 'frames' not in item.data:
        item.data['frames'] = []

    for other in items:
        if hasattr(other, "data"):
            item.data['frames'].extend(deepcopy(other.data.get('frames', [])))

    return item
