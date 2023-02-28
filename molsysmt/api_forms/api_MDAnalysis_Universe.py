def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.MDAnalysis_Universe import to_nglview_NGLWidget as MDAnalysis_Universe_to_nglview_NGLWidget

    return MDAnalysis_Universe_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.MDAnalysis_Universe import to_file_pdb as MDAnalysis_Universe_to_file_pdb

    return MDAnalysis_Universe_to_file_pdb(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices, output_filename=output_filename)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.MDAnalysis_Universe import to_mdtraj_Trajectory as MDAnalysis_Universe_to_mdtraj_Trajectory

    return MDAnalysis_Universe_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.MDAnalysis_Universe import to_molsysmt_MolSys as MDAnalysis_Universe_to_molsysmt_MolSys

    return MDAnalysis_Universe_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.MDAnalysis_Universe import to_molsysmt_MolSys as MDAnalysis_Universe_to_molsysmt_Structures

    return MDAnalysis_Universe_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.MDAnalysis_Universe import to_molsysmt_Topology as MDAnalysis_Universe_to_molsysmt_Topology

    return MDAnalysis_Universe_to_molsysmt_Topology(item, atom_indices=atom_indices)
