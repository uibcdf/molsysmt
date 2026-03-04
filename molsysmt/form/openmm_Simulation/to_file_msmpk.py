from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openmm.Simulation')
def to_file_msmpk(item, atom_indices='all', structure_indices='all', output_filename=None, skip_digestion=False):

    from molsysmt.form.molsysmt_MolSys import to_molsysmt_MolSys as openmm_Simulation_to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item = openmm_Simulation_to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    tmp_item = molsysmt_MolSys_to_file_msmpk(tmp_item, output_filename=output_filename, skip_digestion=True)

    return tmp_item

