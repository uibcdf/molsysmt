from molsysmt._private.digestion import digest

@digest(form='file:prmtop')
def to_molsysmt_MolSys(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native import MolSys, Structures
    from .to_molsysmt_Topology import to_molsysmt_Topology
    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices)
    tmp_item.structures = Structures()

    return tmp_item

