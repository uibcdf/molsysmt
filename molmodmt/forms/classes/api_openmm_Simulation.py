from os.path import basename as _basename
from simtk.openmm.app import Simulation as _openmm_Simulation

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _openmm_Simulation : form_name,
    'openmm.Simulation' : form_name,
}

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):

    return item.topology

def to_openmm_Modeller(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app import Modeller as _Modeller

    topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=None)
    state = item.context.getState(getPositions=True)
    positions = state.getPositions()
    tmp_item =_Modeller(topology, positions)
    return tmp_item

def to_pdbfixer_PDBFixer (item, atom_indices=None, frame_indices=None):

    from molmodmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from molmodmt.utils.miscellanea import tmp_filename as _tmp_filename
    from os import remove as _remove

    tmp_pdbfile = _tmp_filename('.pdb')
    to_pdb(item, output_file_path=tmp_pdbfile, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = pdb_to_pdbfixer_PDBFixer(tmp_pdbfile)
    _remove(tmp_pdbfile)
    return tmp_item

def to_pdb (item, output_file_path=None, atom_indices=None, frame_indices=None):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    topology = to_openmm_Topology(item, atom_indices=atom_indices)
    state = item.context.getState(getPositions=True)
    positions = state.getPositions()
    periodicBoxVectors = state.getPeriodicBoxVectors()
    topology.setPeriodicBoxVectors(periodicBoxVectors)
    return _openmm_app_PDBFILE.writeFile(topology, positions, open(output_file_path, 'w'))

###### Get

## system

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

