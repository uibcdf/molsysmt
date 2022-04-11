from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_mdtraj_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:prmtop')
        atom_indices = digest_atom_indices(atom_indices)

    try:
        from mdtraj import load_prmtop
    except:
        raise LibreryNotFoundError()

    tmp_item = load_prmtop(item)

    return tmp_item

