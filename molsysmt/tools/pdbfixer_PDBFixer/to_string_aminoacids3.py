def to_string_aminoacids3(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):


    tmp_item, _ = to_openm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_wit_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system




    from molsysmt.tools.pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
    from molsysmt.basic import convert

    if not is_pdbfixer_PDBFixer(item):
        raise ValueError

    tmp_item = convert(item, to_form='string:aminoacids3', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

