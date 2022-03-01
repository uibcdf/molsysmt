def to_nglview_NGLWidget(item, selection='all', structure_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.file_h5 import is_file_h5
    from molsysmt.basic import convert

    if not is_file_h5(item):
        raise ValueError

    tmp_item = convert(item, 'nglview.NGLWidget', selection=selection, structure_indices=structure_indices, syntaxis=syntaxis)

    return tmp_item

