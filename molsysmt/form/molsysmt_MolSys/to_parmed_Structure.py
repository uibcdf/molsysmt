from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSys')
def to_parmed_Structure(item, atom_indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from ..molsysmt_Topology import to_parmed_Structure as molsysmt_Topology_to_parmed_Structure

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item = molsysmt_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

