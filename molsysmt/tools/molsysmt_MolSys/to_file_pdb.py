
def to_file_pdb(item, atom_indices='all', structure_indices='all', output_filename=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_MolSys import is_molsysmt_MolSys
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_MolSys(item):
            raise WrongFormError('molsysmt.MolSys')

    if output_filename is None:
        raise ValueError('The value different from None is required for the argument "output_filename"')

    from molsysmt.tools.molsys_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, check_form=False)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, atom_indices=atom_indices, output_filename=output_filename, check_form=False)

    return tmp_item

