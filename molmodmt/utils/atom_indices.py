
def complementary_atom_indices(item, atom_indices):

    from numpy import ones
    from numpy import where
    from molmodmt import get

    n_atoms = get(item, element='system', n_atoms=True)

    mask = ones(n_atoms,dtype=bool)
    mask[atom_indices]=False
    return list(where(mask)[0])

def atom_indices_to_AmberMask(item, atom_indices):

    from numpy import zeros
    from molmodmt import get

    n_atoms = get(item, element='system', n_atoms=True)
    mask = zeros(n_atoms,dtype=int)
    mask[atom_indices]=1
    return list(mask)

def digest(item, atom_indices):

    from numpy import arange, array
    from molmodmt.multitool import get

    if atom_indices is 'all':
        from numpy import arange
        n_atoms = get(item, target='system', n_atoms=True)
        atom_indices = arange(n_atoms, dtype='int64')
    elif type(frame_indices)==int:
        atom_indices = array([atom_indices], dtype='int64')
    elif type(frame_indices) in [tuple, list]:
        atom_indices = array(atom_indices, dtype='int64')

    return atom_indices

