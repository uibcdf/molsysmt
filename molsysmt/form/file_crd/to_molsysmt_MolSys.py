from molsysmt._private.digestion import digest

@digest(form='file:crd')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all'):

    from . import to_MDAnalysis_Universe as file_crd_to_MDAnalysis_Universe
    from ..MDAnalysis_Universe import to_molsysmt_MolSys as MDAnalysis_Universe_to_molsysmt_MolSys

    tmp_item = file_crd_to_MDAnalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = MDAnalysis_Universe_to_molsysmt_MolSys(tmp_item)

    return tmp_item
