from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='string:alphafold_id')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from ..molsysmt_MolSys.to_molsysmt_MolSys import to_molsysmt_MolSys
    from ..molsysmt_MolSys.to_mdtraj_Topology import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item


