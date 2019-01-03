from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form={}

def to_nglview(item):
    from nglview import show_mdtraj as _nglview_show_mdtraj
    from molsysmt.formats.engines.api_openmm import to_mdtraj as _openmm_to_mdtraj
    return _nglview_show_mdtraj(_openmm_to_mdtraj(item))



