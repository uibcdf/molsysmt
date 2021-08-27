def from_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_file_msmpk import to_molsysmt_MolSys as file_msmpk_to_molsysmt_MolSys
    from molsysmt.forms.classes.api_molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = file_msmpk_to_molsysmt_MolSys(item,
            molecular_system=molecular_system, atom_indices=atom_indices,
            frame_indices=frame_indices)

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

