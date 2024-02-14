from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_parmed_Structure(item, atom_indices='all'):

    from .to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSysOld_to_molsysmt_TopologyOld
    from ..molsysmt_Topology import to_parmed_Structure as molsysmt_TopologyOld_to_parmed_Structure

    tmp_item = molsysmt_MolSysOld_to_molsysmt_TopologyOld(item, atom_indices=atom_indices)
    tmp_item = molsysmt_TopologyOld_to_parmed_Structure(tmp_item)
    return tmp_item

