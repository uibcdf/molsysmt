def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

    if check:
        from molsysmt.tools.file_pdb.is_file_pdb import _checking_form
        _checking_form(item, check=check)

    from molsysmt.native import MolSys
    from molsysmt.tools.file_pdb import to_molsysmt_Topology as file_pdb_to_molsysmt_Topology
    from molsysmt.tools.file_pdb import to_molsysmt_Structures as file_pdb_to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = file_pdb_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item.trajectory = file_pdb_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

