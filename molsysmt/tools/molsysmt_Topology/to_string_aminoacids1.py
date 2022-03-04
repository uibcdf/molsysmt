def to_string_aminoacids1(item, atom_indices='all', check=True):

    if check:
        from molsysmt.tools.molsysmt_Topology import is_molsymst_Topology
        from molsysmt._private_tools.exceptions import WrongFormError
        if not is_molsysmt_Topology(item):
            raise WrongFormError('molsysmt.Topology')

    from molsysmt.tools.string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1
    from molsysmt.tools.molsysmt_Topology import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item = molsysmt_Topology_to_string_aminoacids3(item, atom_indices=atom_indices, check=False)
    tmp_item = string_aminoacids3_to_string_aminoacids1(tmp_item, check=False)

    return tmp_item

