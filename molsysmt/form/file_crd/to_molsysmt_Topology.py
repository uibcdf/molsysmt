def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_file_crd import to_mdanalysis_Universe as file_crd_to_mdanalysis_Universe
    from molsysmt.api_forms.api_mdanalysis_Universe import to_molsysmt_Topology as mdanalysis_Universe_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = file_crd_to_mdanalysis_Universe(item,
            molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = mdanalysis_Universe_to_molsysmt_Topology(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system
