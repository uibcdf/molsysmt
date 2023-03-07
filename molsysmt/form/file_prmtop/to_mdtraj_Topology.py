from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_mdtraj_Topology(item, atom_indices='all'):

    try:
        from mdtraj import load_prmtop
    except:
        raise LibraryNotFoundError()

    tmp_item = load_prmtop(item)

    return tmp_item

def _to_mdtraj_Topology(item, atom_indices='all', structure_indices='all'):
 
    return to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)

