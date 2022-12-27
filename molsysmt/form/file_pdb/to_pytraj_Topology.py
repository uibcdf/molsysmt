from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_pytraj_Topology(item, atom_indices='all'):

    try:
        from pytraj import load_topology
    except:
        raise LibraryNotFoundError('pytraj')

    from ..pytraj_Topology import extract as extract_pytraj_Topology

    tmp_item = load_topology(item)
    tmp_item = extract_pytraj_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, copy_if_all=False)

    return tmp_item

