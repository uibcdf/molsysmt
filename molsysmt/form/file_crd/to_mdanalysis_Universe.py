def to_mdanalysis_Universe(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_mdanalysis_Universe import to_mdanalysis_Universe as mdanalysis_Universe_to_mdanalysis_Universe
    from MDAnalysis import Universe

    tmp_item = Universe(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mdanalysis_Universe_to_mdanalysis_Universe(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

