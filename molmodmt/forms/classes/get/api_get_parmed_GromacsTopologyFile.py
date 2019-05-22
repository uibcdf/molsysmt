
def getting(item, atom_indices=None, **kwargs):
    from .api_get_parmed_Structure import getting as _get
    return _get(item, atom_indices, **kwargs)

