from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:cif.gz')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from ..mmcif_PdbxContainers_DataContainer.to_mmcif_PdbxContainers_DataContainer import to_mmcif_PdbxContainers_DataContainer
    from ..mmcif_PdbxContainers_DataContainer.to_molsysmt_Topology import to_molsysmt_Topology as mmcif_PdbxContainers_DataContainer_to_molsysmt_Topology

    tmp_item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = mmcif_PdbxContainers_DataContainer_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices,
                                                                       skip_digestion=True)

    return tmp_item

