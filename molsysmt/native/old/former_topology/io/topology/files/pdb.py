def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all',
           frame_indices='all'):

    from molsysmt.native.io.topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.forms.api_openmm_Topology import to_pdb as openmm_Topology_to_pdb

    tmp_item = molsysmt_Topology_to_openmm_Topology(item)

    return openmm_Topology_to_pdb(tmp_item, output_filepath=output_filepath,
                                  trajectory_item=trajectory_item,
                                  atom_indices=atom_indices, frame_indices=frame_indices)


def from_pdb(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_pdb import to_openmm_PDBFile as pdb_to_openmm_PDBFile
    from molsysmt.native.io.topology import from_openmm_PDBFile as openmm_PDBFile_to_molsysmt_Topology

    tmp_item = pdb_to_openmm_PDBFile(item)
    tmp_item = openmm_PDBFile_to_molsysmt_Topology(tmp_item)

    return tmp_item

