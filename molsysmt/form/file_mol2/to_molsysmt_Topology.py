from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='file:mol2')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from ..molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(tmp_item, skip_digestion=True)

    return tmp_item

