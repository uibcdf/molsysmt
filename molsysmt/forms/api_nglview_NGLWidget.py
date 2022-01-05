from molsysmt._private_tools.exceptions import *
from molsysmt.forms.common_gets import *
import numpy as np
import importlib
import sys
from molsysmt.native.molecular_system import molecular_system_components
from molsysmt import puw

form_name='nglview.NGLWidget'

is_form = {
    'nglview.NGLWidget': form_name
    }

info=["NGLView visualization native object","http://nglviewer.org/nglview/latest/_modules/nglview/widget.html"]

has = molecular_system_components.copy()
for ii in ['elements', 'coordinates', 'box']:
    has[ii]=True

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology import from_nglview_NGLWidget as nglview_NGLWidget_to_molsysmt_Topology

    tmp_item, tmp_molecular_system = nglview_NGLWidget_to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices='all')

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory import from_nglview_NGLWidget as nglview_NGLWidget_to_molsysmt_Trajectory

    tmp_item, tmp_molecular_system = nglview_NGLWidget_to_molsysmt_Trajectory(item,
            molecular_system=molecular_system, atom_indices=atom_indices,
            frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import from_nglview_NGLWidget as nglview_NGLWidget_to_molsysmt_MolSys

    tmp_item, tmp_molecular_system = nglview_NGLWidget_to_molsysmt_MolSys(item,
            molecular_system=molecular_system, atom_indices=atom_indices,
            frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_string_pdb_text import to_openmm_Topology as string_pdb_to_openmm_Topology
    from molsysmt.forms.api_openmm_Topology import to_openmm_Topology as openmm_Topology_to_openmm_Topology

    try:
        tmp_item = item.component_0.get_structure_string()
    except:
        tmp_item = item.get_state()['_ngl_msg_archive'][0]['args'][0]['data']

    tmp_item, _ = string_pdb_to_openmm_Topology(tmp_item)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    tmp_item, tmp_molecular_system = openmm_Topology_to_openmm_Topology(tmp_item,
            molecular_system=tmp_molecular_system, atom_indices=atom_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_string_pdb_text(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system,
            atom_indices=atom_indices, frame_indices=frame_indices)

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_string_pdb_text(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1

    tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system,
            atom_indices=atom_indices, frame_indices=frame_indices)

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_string_aminoacids1(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            if tmp_molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if tmp_molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if tmp_molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        from copy import copy
        return copy(item)
    else:
        from molsysmt.forms.api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
        tmp_item, _ = to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item, _ = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)
        return tmp_item

    return tmp_item

def merge(item_1, item_2):

    from molsysmt.forms.api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    from molsysmt.forms.api_molsysmt_MolSys import merge as merge_molsysmt_MolSys
    tmp_item_1, _ = to_molsysmt_MolSys(item_1)
    tmp_item_2, _ = to_molsysmt_MolSys(item_2)
    tmp_item = merge_molsysmt_MolSys(tmp_item_1, tmp_item_2)
    tmp_item, _ = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)
    return tmp_item

def add(to_item, item):

    raise NotWithThisForm()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotWithThisForm()

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    from molsysmt.forms.api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
    from molsysmt.forms.api_molsysmt_MolSys import append_frames as append_frames_molsysmt_MolSys
    tmp_item, _ = to_molsysmt_MolSys(item)
    append_frames_molsysmt_MolSys(tmp_item, step=step, time=time, coordinates=coordinates, box=box)
    tmp_item, _ = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item)
    return tmp_item

###### Get

def aux_get(item, indices='all', frame_indices='all'):

    from molsysmt.forms import forms

    method_name = sys._getframe(1).f_code.co_name

    if 'openmm.Topology' in forms:

        tmp_item, _ = to_openmm_Topology(item, frame_indices=frame_indices)
        module = importlib.import_module('molsysmt.forms.api_openmm_Topology')
        _get = getattr(module, method_name)
        output = _get(tmp_item, indices=indices)

    else:

        raise NotImplementedError

    return output

## Atom

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        n_frames = get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    coordinates = []

    for ii in frame_indices:
        if indices is 'all':
            coordinates.append(item.component_0.get_coordinates(ii))
        else:
            coordinates.append(item.component_0.get_coordinates(ii)[indices,:])

    coordinates = np.array(coordinates)
    coordinates = puw.quantity(coordinates, unit='angstroms')
    coordinates = puw.standardize(coordinates)

    return coordinates

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    coordinates = get_coordinates_from_atom(item, indices=indices, frame_indices=frame_indices)
    box = get_box_from_system(item, frame_indices=frame_indices)
    step = get_step_from_system(item, frame_indices=frame_indices)
    time = get_time_from_system(item, frame_indices=frame_indices)

    return step, time, coordinates, box

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        n_frames = get_n_frames_from_system(item)
        frame_indices = np.arange(n_frames)

    coordinates = []

    for ii in frame_indices:
        coordinates.append(item.component_0.get_coordinates(ii))

    coordinates = np.array(coordinates)
    coordinates = puw.quantity(coordinates, unit='angstroms')
    coordinates = puw.standardize(coordinates)

    return

def get_box_from_system(item, indices='all', frame_indices='all'):

    # We can only get the box from frame 0

    from molsysmt.forms.api_openmm_Topology import get_box_from_system as get_box_from_system_openmm_Topology

    if frame_indices is 'all':
        n_frames = get_n_frames_from_system(item)
    else:
        n_frames = frame_indices.shape[0]

    openmm_Topology, _ = to_openmm_Topology(item, atom_indices='all', frame_indices=0)

    aux_box = get_box_from_system_openmm_Topology(openmm_Topology)

    if aux_box is not None:
        aux_box_value_frame_0 = puw.get_value(aux_box[0])
        aux_box_unit = puw.get_unit(aux_box)

        box = [aux_box_value_frame_0 for ii in range(n_frames)]
        box = np.array(box)
        box = puw.quantity(box, unit=aux_box_unit)
        box = puw.standardize(box)
    else:
        box = None

    return box

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_time_from_system(item, indices='all', frame_indices='all'):

    return None

def get_step_from_system(item, indices='all', frame_indices='all'):

    return None

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    if frame_indices is 'all':
        n_frames = item.component_0.n_frames
    else:
        n_frames = frame_indices.shape[0]

    return n_frames

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    return aux_get(item, indices=indices, frame_indices=frame_indices)

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

