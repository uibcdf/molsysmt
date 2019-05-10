from os.path import basename as _basename
from simtk.openmm.app import Topology as _simtk_openmm_app_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'openmm.topology':form_name,
    'openmm.Topology':form_name,
    'simtk.openmm.app.topology.Topology':form_name,
    _simtk_openmm_app_Topology:form_name
}

def to_molmod_Topology(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_topology import from_openmm_Topology as _from_openmm_Topology
    return _from_openmm_Topology(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Topology(item, selection=None, syntaxis='mdtraj'):
    from molmodmt import extract as _extract
    from mdtraj.core.topology import Topology as _mdtraj_Topology
    tmp_item = _mdtraj_Topology.from_openmm(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    del(_mdtraj_Topology)
    return tmp_item

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    return to_mdtraj_Topology(item, selection=selection, syntaxis=syntaxis)

def to_parmed_Structure(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from parmed.openmm import load_topology as _openmm_Topology_to_parmed_Estructure
    tmp_item = _openmm_Topology_to_parmed_Estructure(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    del(_openmm_Topology_to_parmed_Estructure)
    return tmp_item

def to_yank_Topography(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from yank import Topography as _yank_Topography
    tmp_item = _yank_Topography(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    del(_yank_Topography)
    return tmp_item

def extract_atoms_list(item, atoms_list):
    from .api_mdtraj_Topology import extract_atoms_list as _mdtraj_Topology_extract
    from .api_mdtraj_Topology import to_openmm_Topology as _mdtraj_to_openmm
    tmp_item=to_mdtraj_Topology(item)
    tmp_item=_mdtraj_Topology_extract(tmp_item,atoms_list)
    tmp_item=_mdtraj_to_openmm(tmp_item)
    return tmp_item

def select_with_mdtraj(item, selection):

    tmp_item = to_mdtraj_Topology(item)
    return tmp_item.select(selection)

