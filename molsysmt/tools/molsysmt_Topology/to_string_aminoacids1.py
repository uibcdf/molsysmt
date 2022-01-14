def to_string_aminoacids1(item, atom_indices='all', check_form=True):

    if check_form:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import ItemWithWrongForm
        if not is_molsysmt_Topology(item):
            raise ItemWithWrongForm('molsysmt.Topology')

    from molsysmt.tools.string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1
    from molsysmt.tools.molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = molsysmt_Topology_to_string_aminoacids3(item, atom_indices=atom_indices, check_form=False)
    tmp_item = string_aminoacids3_to_string_aminoacids1(tmp_item, check_form=False)

    return tmp_item

