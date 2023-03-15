def file_prmtop_and_file_inpcrd_to_molsysmt_MolSys(molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get_form
    from molsysmt.form.file_prmtop import to_molsysmt_Topology as file_prmtop_to_molsysmt_Topology
    from molsysmt.form.file_inpcrd import to_molsysmt_Structures as file_inpcrd_to_molsysmt_Structures
    from molsysmt.native import MolSys

    forms = get_form(molecular_system)

    item_prmtop = None
    item_incrd = None

    for form, item in zip(forms, molecular_system):
        if form=='file:prmtop':
            item_prmtop = item
        else:
            item_inpcrd = item

    output_item = MolSys()

    output_item.topology = file_prmtop_to_molsysmt_Topology(item_prmtop, atom_indices=atom_indices)
    output_item.structures = file_inpcrd_to_molsysmt_Structures(item_inpcrd, atom_indices=atom_indices, structure_indices=structure_indices)

    return output_item

