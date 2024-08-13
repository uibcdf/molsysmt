from molsysmt._private.digestion import digest

@digest(form='file:bcif')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from . import to_mmcif_PdbxContainers_DataContainer
    from ..mmcif_PdbxContainers_DataContainer import to_molsysmt_MolSys as mmcif_PdbxContainers_DataContainer_to_molsysmt_MolSys

    tmp_item = to_mmcif_PdbxContainers_DataContainer(item, skip_digestion=True)
    tmp_item = mmcif_PdbxContainers_DataContainer_to_molsysmt_MolSys(tmp_item, atom_indices=atom_indices,
                                                   structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

