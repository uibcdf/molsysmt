from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.Topology')
def remove_bonds(item, bond_indices='all', skip_digestion=False):

    return item.remove_bonds(bond_indices=bond_indices, skip_digestion=True)
