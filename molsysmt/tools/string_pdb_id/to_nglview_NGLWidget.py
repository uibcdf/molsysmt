def to_nglview_NGLWidget(item, selection='all', model_indices='all', syntaxis='MolSysMT'):

    from molsysmt.tools.string_pdb_id import is_string_pdb_id
    from molsysmt.basic import convert

    if not is_string_pdb_id(item):
        raise ValueError

    tmp_item = convert(item, to_form='nglview.NGLWidget', selection=selection, frame_indices=model_indices, syntaxis=syntaxis)

    return tmp_item

