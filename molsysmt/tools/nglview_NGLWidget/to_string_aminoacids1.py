def to_string_aminoacids1(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.nglview_NGLWidget import is_nglview_NGLWidget
    from molsysmt.basic import convert

    if not is_nglview_NGLWidget(item):
        raise ValueError

    tmp_item = convert(item, to_form='string:aminoacids1', selection=selection,
            structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

