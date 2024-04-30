from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.Topology')
def remove_bonds(item, bond_indices='all', skip_digestion=False):

    return item.remove_bonds(bond_indices=bond_indices, skip_digestion=True)
