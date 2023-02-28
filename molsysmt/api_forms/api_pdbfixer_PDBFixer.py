def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_string_aminoacids3 as pdbfixer_PDBFixer_to_string_aminoacids3

    return pdbfixer_PDBFixer_to_string_aminoacids3(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_string_aminoacids1 as pdbfixer_PDBFixer_to_string_aminoacids1

    return pdbfixer_PDBFixer_to_string_aminoacids1(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_biopython_Seq as pdbfixer_PDBFixer_to_biopython_Seq

    return pdbfixer_PDBFixer_to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_biopython_Seq as pdbfixer_PDBFixer_to_biopython_Seq

    return pdbfixer_PDBFixer_to_biopython_SeqRecord(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_mdtraj_Topology as pdbfixer_PDBFixer_to_mdtraj_Topology

    return pdbfixer_PDBFixer_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_mdtraj_Trajectory as pdbfixer_PDBFixer_to_mdtraj_Trajectory

    return pdbfixer_PDBFixer_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_openmm_Modeller as pdbfixer_PDBFixer_to_openmm_Modeller

    return pdbfixer_PDBFixer_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_openmm_Topology as pdbfixer_PDBFixer_to_openmm_Topology

    return pdbfixer_PDBFixer_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_molsysmt_Topology as pdbfixer_PDBFixer_to_molsysmt_Topology

    return pdbfixer_PDBFixer_to_molsysmt_Topology(item, atom_indices=atom_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_molsysmt_MolSys as pdbfixer_PDBFixer_to_molsysmt_MolSys

    return pdbfixer_PDBFixer_to_molsysmt_MolSys(item, atom_indices=atom_indices)


def to_parmed_Structure(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_parmed_Structure as pdbfixer_PDBFixer_to_parmed_Structure

    return pdbfixer_PDBFixer_to_parmed_Structure(item, atom_indices=atom_indices)


def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.pdbfixer_PDBFixer import to_file_pdb as pdbfixer_PDBFixer_to_file_pdb

    return pdbfixer_PDBFixer_to_file_pdb(item, atom_indices=atom_indices)


def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_nglview_NGLWidget as pdbfixer_PDBFixer_to_nglview_NGLWidget

    return pdbfixer_PDBFixer_to_nglview_NGLWidget(item, atom_indices=atom_indices)
