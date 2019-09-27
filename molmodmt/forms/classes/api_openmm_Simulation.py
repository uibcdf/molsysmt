from os.path import basename as _basename
from simtk.openmm.app import Simulation as _openmm_Simulation

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Simulation : form_name,
    'openmm.Simulation' : form_name,
}

def to_openmm_Topology(item, selection=None, frame_indices=None, syntaxis="MDTraj"):

    return item.topology

def to_openmm_Modeller(item, selection=None, syntaxis="MDTraj"):

    from simtk.openmm.app import Modeller as _Modeller

    topology = to_openmm_Topology(item, selection=selection, frame_indices=None, syntaxis=syntaxis)
    state = item.context.getState(getPositions=True)
    positions = state.getPositions()
    tmp_item =_Modeller(topology, positions)
    return tmp_item

def to_pdbfixer_PDBFixer (item, selection=None, frame_indices=None, syntaxis="MDTraj"):

    from molmodmt.utils.miscellanea import tmp_filename as _tmp_filename
    from os import remove as _remove
    from molmodmt import convert as _convert

    tmp_pdbfile = _tmp_filename('.pdb')
    to_pdb(item, tmp_pdbfile)
    tmp_item = _convert(tmp_pdbfile, 'pdbfixer.PDBFixer')
    _remove(tmp_pdbfile)
    return tmp_item

def to_pdb (item, filename = None, selection=None, frame_indices=None, syntaxis="MDTraj"):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    topology = to_openmm_Topology(item, selection=selection, syntaxis=syntaxis)
    state = item.context.getState(getPositions=True)
    positions = state.getPositions()
    periodicBoxVectors = state.getPeriodicBoxVectors()
    topology.setPeriodicBoxVectors(periodicBoxVectors)
    return _openmm_app_PDBFILE.writeFile(topology, positions, open(filename, 'w'))


