
def complementary_atom_indices(item, atom_indices):

    from molmodmt import select

    list_all = select(item, selection="all")
    list_complementary = list(set(list_all)-set(atom_indices))
    return list_complementary
