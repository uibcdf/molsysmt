from os.path import basename as _basename
from simtk.openmm.app import Simulation as _openmm_Simulation

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Simulation : form_name,
    'openmm.Simulation' : form_name,
}

def to_openmm_Topology(item, selection=None, syntaxis="mdtraj"):

    return item.topology

def to_openmm_Modeller(item, selection=None, syntaxis="mdtraj"):

    from simtk.openmm.app import Modeller as _Modeller

    topology = to_openmm_Topology(item, selection=selection, syntaxis=syntaxis)
    state = item.context.getState(getPositions=True)
    positions = state.getPositions()
    tmp_item =_Modeller(topology, positions)
    return tmp_item

