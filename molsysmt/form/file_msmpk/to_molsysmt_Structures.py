from molsysmt._private.digestion import digest

@digest(form='file:msmpk')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_molsysmt_Structures as molsysmt_MolSys_to_molsysmt_Structures

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_molsysmt_Structures(tmp_item)

    return tmp_item

def _to_molsysmt_Structures(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Structures(item, atom_indices=atom_indices)
