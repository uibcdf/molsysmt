from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSys')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    return item.topology.extract(atom_indices=atom_indices, skip_digestion=True)

