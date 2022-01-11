
def to_file_pdb(item, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt._private_tools.exceptions import ItemWithWrongForm
    from molsysmt.tools.molsysmt_MolSys import is_molsymst_MolSys
    from molsysmt.tools.molsys_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
    from molsysmt.tools.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    if not is_molsysmt_MolSys(item):
        raise ItemWithWrongForm('molsysmt.MolSys')

    if output_filename is None:
        raise ValueError('The value different from None is required for the argument "output_filename"')

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, atom_indices=atom_indices, output_filename=output_filename)

    return tmp_item

