from os.path import basename as _basename
from simtk.openmm.app import PDBFile as _openmm_PDBFile

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_PDBFile : form_name,
    'openmm.PDBFile' : form_name
}

from .get.api_get_openmm_PDBFile import getting
#from .set.api_set_openmm_PDBFile import setting

def get_total_n_atoms(item):
    return item.topology.getNumAtoms()

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview
    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview
    tmp_item = to_mdtraj(item)
    return _mdtraj_to_nglview(tmp_item)

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):
    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    import simtk.unit as _unit
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

    tmp_topology = to_mdtraj_Topology(item)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_topology)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)

    return tmp_item

def to_mdtraj_Topology(item, selection=None, syntaxis='mdtraj'):

    from .api_openmm_Topology import to_mdtraj_Topology as _to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item)
    tmp_item = _to_mdtraj_Topology(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_openmm_Topology(item, selection=None, syntaxis='mdtraj'):

    return item.getTopology()
