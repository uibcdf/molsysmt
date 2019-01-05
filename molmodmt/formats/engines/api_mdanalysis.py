from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form={
    'mdanalysis':form_name,
    'MDAnalysis':form_name
}

def to_nglview(item):
    from nglview import show_mdtraj as _nglview_show_mdanalysis
    return _nglview_show_mdanalysis(item)



