from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', digest=True):

    from molsysmt.native import MolSys
    from . import to_molsysmt_Topology
    from . import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, digest=False)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)

    return tmp_item

