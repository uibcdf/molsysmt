from molsysmt._private.digestion import digest

@digest(form='file:mol2')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys
    from . import to_molsysmt_Topology
    from . import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.trajectory = to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices,
                                                    skip_digestion=True)

    return tmp_item
