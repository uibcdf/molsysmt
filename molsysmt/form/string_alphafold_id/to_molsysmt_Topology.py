from molsysmt._private.digestion import digest

@digest(form='string:alphafold_id')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):


    from . import to_mmcif_PdbxContainers_DataContainer
    from ..mmcif_PdbxContainers_DataContainer import to_molsysmt_Topology as mmcif_PdbxContainers_DataContainer_to_molsysmt_Topology

    tmp_item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = mmcif_PdbxContainers_DataContainer_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

