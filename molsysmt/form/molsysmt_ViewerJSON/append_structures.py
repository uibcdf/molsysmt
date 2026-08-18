from molsysmt._private.argdigest import arg_digest
from copy import deepcopy


@arg_digest(form='molsysmt.ViewerJSON')
def append_structures(item, items, skip_digestion=False):
    """
    Appending coordinate structures to an item of form molsysmt.ViewerJSON.

    Parameters
    ----------
    item : molsysmt.ViewerJSON
        Source item in molsysmt.ViewerJSON form.
    items : list of object
        List of items to merge.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Resulting object in molsysmt.ViewerJSON form.

    .. versionadded:: 1.0.0
    """

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
