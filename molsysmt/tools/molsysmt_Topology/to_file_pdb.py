
def to_file_pdb(item, coordinates, box, atom_indices='all', output_filename=None, check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    if output_filename is None:
        raise ValueError

    from molsysmt.tools.molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.tools.openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item =  molsysmt_Topology_to_openmm_Topology(item, box, atom_indices=atom_indices)
    tmp_item =  openmm_Topology_to_file_pdb(tmp_item, coordinates, output_filename=output_filename)

    return tmp_item

