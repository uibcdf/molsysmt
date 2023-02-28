def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_string_aminoacids3 as mdtraj_Topology_to_string_aminoacids3

    from molsysmt.form.mdtraj_Topology import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    return mdtraj_Topology_to_string_aminoacids3(item, group_indices=group_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_string_aminoacids1 as mdtraj_Topology_to_string_aminoacids1

    from molsysmt.form.mdtraj_Topology import get_group_index_from_atom

    group_indices = get_group_index_from_atom(item, indices=atom_indices)
    return mdtraj_Topology_to_string_aminoacids1(item, group_indices=group_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_molsysmt_Topology as mdtraj_Topology_to_molsysmt_Topology

    return mdtraj_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    return mdtraj_Topology_to_openmm_Topology(item, atom_indices=atom_indices)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_parmed_Structure as mdtraj_Topology_to_parmed_Structure

    return mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices)


def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_parmed_Structure as mdtraj_Topology_to_parmed_Structure

    return mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices)


def to_file_top(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mdtraj_Topology import to_file_top as mdtraj_Topology_to_file_top

    return mdtraj_Topology_to_parmed_Structure(item, atom_indices=atom_indices, output_filename=output_filename)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdtraj_Topology import to_mdtraj_Trajectory as mdtraj_Topology_to_mdtraj_Trajectory

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
    return mdtraj_Topology_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                                coordinates=coordinates, box=box)
