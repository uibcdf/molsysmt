def to_string_pdb_text(item, coordinates, box, atom_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    from molsysmt.tools.molsysmt_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.tools.openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item =  molsysmt_Topology_to_openmm_Topology(item, box, atom_indices=atom_indices, check_form=False)
    tmp_item =  openmm_Topology_to_string_pdb_text(tmp_item, coordinates, check_form=False)

    return tmp_item

