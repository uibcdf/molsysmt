from os.path import basename as _basename
from simtk.openmm.app import Topology as _simtk_openmm_app_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'openmm.topology':form_name,
    'openmm.Topology':form_name,
    'simtk.openmm.app.topology.Topology':form_name,
    _simtk_openmm_app_Topology:form_name
}

def to_molmod_Topology(item):

    from molmodmt.native.io_topology import from_openmm_Topology as _from_openmm_Topology
    return _from_openmm_Topology(item)

def to_mdtraj_Topology(item):

    from mdtraj.core.topology import Topology as _mdtraj_Topology
    tmp_form = _mdtraj_Topology.from_openmm(item)
    del(_mdtraj_Topology)
    return tmp_form

def to_mdtraj(item):

    return to_mdtraj_Topology(item)

def to_parmed_Structure(item):

    from parmed.openmm import load_topology as _openmm_Topology_to_parmed_Estructure

    tmp_form = _openmm_Topology_to_parmed_Estructure(item)
    del(_openmm_Topology_to_parmed_Estructure)
    return tmp_form

def to_yank_Topography(item):

    from yank import Topography as _yank_Topography
    tmp_form = _yank_Topography(item)
    del(_yank_Topography)
    return tmp_form
