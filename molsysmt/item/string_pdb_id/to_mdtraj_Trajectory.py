from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'mmtf.MMTFDecoder')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import to_molsysmt_MolSys
    from ..molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices)
    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(tmp_item)

    return tmp_item

