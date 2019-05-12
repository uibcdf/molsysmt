
def complementary_atoms_list(item, atoms_list):

    from molmodmt import get as _get

    n_atoms = _get(item, n_atoms=True)
    list_all = list(range(n_atoms))
    list_complementary = list(set(list_all)-set(atoms_list))
    return list_complementary
