from os.path import basename as _basename
from simtk.openmm.app.modeller import Modeller as _openmm_modeller_Modeller

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_modeller_Modeller : form_name,
    'simtk.openmm.app.modeller.Modeller' : form_name
}

def to_nglview(item):

    from nglview import show_mdtraj as _nglview_show_mdtraj
    from molsysmt.formats.engines.api_modeller import to_mdtraj as _modeller_to_mdtraj
    tmp_view = _nglview_show_mdtraj(_modeller_to_mdtraj(item))
    #if item.topology.getNumAtoms() < 2000:
    #    view.add_ball_and_stick('all')
    #tmp_view.center_view(zoom=True)
    return tmp_view

# def to_native(item):
# 
#     from molsysmt import Native as _molsysmt_native
#     tmp_form = _molsysmt_native(item)
#     del(_molsysmt_native)
#     return tmp_form
#

def to_mdtraj(item):
    from molsysmt.formats.engines.api_modeller import to_mdtraj as _modeller_to_mdtraj
    return __modeller_to_mdtraj(item)

def to_mdtraj_Topology(item):

    from mdtraj.Topology import from_openmm as _mdtraj_Topology_from_openmm
    tmp_form = _mdtraj_Topology_from_openmm(item.Topology)
    del(_mdtraj_Topology_from_openmm)
    return tmp_form

def to_parmed_Structure(item):

    from parmed.openmm import load_topology as _openmm_Topology_to_parmed_Estructure

    tmp_form = _openmm_Topology_to_parmed_Estructure(item.topology)
    del(_openmm_Topology_to_parmed_Estructure)
    return tmp_form

# def to_yank_Topography(item):
# 
#     from yank import Topography as _yank_Topography
#     tmp_form = _yank_Topography(item)
#     del(_yank_Topography)
#     return tmp_form
