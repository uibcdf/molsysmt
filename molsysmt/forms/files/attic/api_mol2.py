from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np

form_name='mol2'

is_form = {
    'mol2': form_name,
    'MOL2': form_name
    }

info=["",""]
with_topology=True
with_trajectory=True
with_coordinates=True
with_box=False
with_bonds=False
with_parameters=False

def to_parmed_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    from parmed import load_file as _parmed_file_loader

    tmp_item = _parmed_file_loader(item)
    tmp_item = tmp_item.to_structure()

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj import load_mol2 as _mdtraj_load_mol2

    tmp_item = _mdtraj_load_mol2(item)
    del(_mdtraj_load_mol2)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from mdtraj import load_mol2 as _mdtraj_load_mol2

    tmp_item = _mdtraj_load_mol2(item).topology
    del(_mdtraj_load_mol2)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology

    tmp_item = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=atom_indices)
    tmp_item = mdtraj_Topology_to_openmm_Topology(tmp_item)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Trajectory import to_openmm_Modeller as mdtraj_Trajectory_to_openmm_Modeller

    tmp_item = to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=atom_indices)
    tmp_item = mdtraj_Trajectory_to_openmm_Modeller(tmp_item)

    return tmp_item

    #from molsysmt.forms.engines.api_parmed import to_modeller as _parmed_to_modeller
    #tmp_form = to_parmed(item)
    #tmp_form = _parmed_to_modeller(tmp_form)
    #del(_parmed_to_modeller)
    #return tmp_form

def to_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from parmed import load_file as _parmed_file_loader

    tmp_item = _parmed_file_loader(item)
    tmp_item.save(output_filename)

    return output_filename

def view_with_NGLView(item, molecular_system, atom_indices='all', frame_indices='all'):

    from nglview import show_file as nglview_show_file

    tmp_item = nglview_show_file(item)

    return tmp_item

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

