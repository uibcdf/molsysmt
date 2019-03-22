from os.path import basename as _basename
from simtk.openmm.app.modeller import Modeller as _openmm_modeller_Modeller

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_modeller_Modeller : form_name,
    'simtk.openmm.app.modeller.Modeller' : form_name
}

def to_nglview(item):

    from nglview import show_mdtraj as _nglview_show_mdtraj
    from molmodmt.formats.engines.api_modeller import to_mdtraj as _modeller_to_mdtraj
    tmp_view = _nglview_show_mdtraj(_modeller_to_mdtraj(item))
    #if item.topology.getNumAtoms() < 2000:
    #    view.add_ball_and_stick('all')
    #tmp_view.center_view(zoom=True)
    return tmp_view

def to_mdtraj(item):
    from molmodmt.formats.engines.api_modeller import to_mdtraj as _modeller_to_mdtraj
    return _modeller_to_mdtraj(item)

def to_mdtraj_Topology(item):

    from mdtraj.core.topology import Topology as _mdtraj_Topology
    tmp_form = _mdtraj_Topology.from_openmm(item.Topology)
    del(_mdtraj_Topology_from_openmm)
    return tmp_form

def to_parmed_Structure(item):

    from parmed.openmm import load_topology as _openmm_Topology_to_parmed_Estructure

    tmp_form = _openmm_Topology_to_parmed_Estructure(item.topology)
    del(_openmm_Topology_to_parmed_Estructure)
    return tmp_form

def to_pdb(item,output_file):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    return _openmm_app_PDBFILE.writeFile(item.topology, item.positions, open(output_file, 'w'))

# def to_yank_Topography(item):
# 
#     from yank import Topography as _yank_Topography
#     tmp_form = _yank_Topography(item)
#     del(_yank_Topography)
#     return tmp_form
