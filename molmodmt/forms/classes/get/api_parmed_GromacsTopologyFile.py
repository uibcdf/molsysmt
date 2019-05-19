
def get(item, atom_indices=None, **kwargs):
    from .parmed_Structure import get as _get
    return _get(item, atom_indices, **kwargs)

