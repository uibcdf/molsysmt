from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_Topology(item, atom_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = to_molsysmt_MolSys(item)
    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices)

    return tmp_item

