from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native.topology import Topology
    from . import get_n_atoms_from_system

    n_atoms = get_n_atoms_from_system(item)
    tmp_item = Topology(n_atoms=n_atoms)

    return tmp_item

