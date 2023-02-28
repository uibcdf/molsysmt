def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.file_prmtop import to_file_pdb as file_prmtop_to_file_pdb

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    return file_prmtop_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates,
                                   output_filename=output_filename)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_mdtraj_Topology as file_prmtop_to_mdtraj_Topology

    return file_prmtop_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_molsysmt_MolSys as file_prmtop_to_molsysmt_MolSys

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    return file_prmtop_to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_molsysmt_Topology as file_prmtop_to_molsysmt_Topology

    return file_prmtop_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_nglview_NGLWidget as file_prmtop_to_nglview_NGLWidget

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return file_prmtop_to_nglview_NGLWidget(item, atom_indices=atom_indices, coordinates=coordinates)


def to_openmm_AmberPrmtopFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_openmm_AmberPrmtopFile as file_prmtop_to_openmm_AmberPrmtopFile

    return file_prmtop_to_nglview_NGLWidget(item, atom_indices=atom_indices)


def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_openmm_Topology as file_prmtop_to_openmm_Topology

    return file_prmtop_to_openmm_Topology(item, atom_indices=atom_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.file_prmtop import to_openmm_Modeller as file_prmtop_to_openmm_Modeller

    from molsysmt.basic import get

    coordinates = get(molecular_system, structure_indices=structure_indices, atom_indices=atom_indices,
                      coordinates=True)
    return file_prmtop_to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates)
