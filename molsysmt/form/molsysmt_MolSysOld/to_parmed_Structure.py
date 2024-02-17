from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):

    from .to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSysOld_to_molsysmt_TopologyOld
    from ..molsysmt_Topology import to_parmed_Structure as molsysmt_TopologyOld_to_parmed_Structure

    tmp_item = molsysmt_MolSysOld_to_molsysmt_TopologyOld(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_TopologyOld_to_parmed_Structure(tmp_item, skip_digestion=True)
    return tmp_item

