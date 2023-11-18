from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresDict')
def to_molsysmt_TopologyOld(item, atom_indices='all', structure_indices='all'):

    from molsysmt.native.topology_old import TopologyOld
    from . import get_n_atoms_from_system

    n_atoms = get_n_atoms_from_system(item)
    tmp_item = TopologyOld(n_atoms=n_atoms)

    return tmp_item

