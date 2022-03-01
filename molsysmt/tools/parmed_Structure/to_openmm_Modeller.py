def to_openmm_Modeller(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.parmed_Structure import is_parmed_Structure
    from molsysmt.basic import convert

    if not is_parmed_Structure(item):
        raise ValueError

    tmp_item = convert(item, to_form='openmm_Modeller', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

