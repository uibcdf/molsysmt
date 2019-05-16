
def complementary_atom_indices(item, atom_indices):

    from molmodmt import get as _get

    n_atoms = _get(item, n_atoms=True)
    list_all = list(range(n_atoms))
    list_complementary = list(set(list_all)-set(atom_indices))
    return list_complementary
