def to_nglview_NGLWidget(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_prmtop import is_file_prmtop
    from molsysmt.basic import convert

    if not is_file_prmtop(item):
        raise ValueError

    tmp_item = convert(item, 'nglview.NGLWidget', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

