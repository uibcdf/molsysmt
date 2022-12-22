#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='mdtraj.HDF5TrajectoryFile'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_atom_id_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_atom_name_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_atom_type_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_group_index_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_group_index_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_component_index_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_component_index_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_chain_index_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_chain_index_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_molecule_index_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_molecule_index_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_entity_index_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_entity_index_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_inner_bonded_atoms_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_inner_bonded_atoms_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_n_inner_bonds_from_atom (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_inner_bonds_from_atom as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, structure_indices=structure_indices, digest=False)

    return output

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', digest=True):

    if (indices is None) or (structure_indices is None):
        return None

    from molsysmt._private.math import serie_to_chunks

    if is_all(structure_indices):
        structure_indices = np.arange(get_n_structures_from_system(item, digest=False))
    if is_all(indices):
        indices = np.arange(get_n_atoms_from_system(item, digest=False))

    starts_serie_frames, size_serie_frames = serie_to_chunks(structure_indices)

    xyz_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        frame_hdf5 = item.read(n_frames=size, atom_indices=indices)
        xyz = frame_hdf5.coordinates
        xyz_list.append(xyz)

    xyz = np.concatenate(xyz_list)
    del(xyz_list)

    xyz = xyz.astype('float64')

    xyz = xyz*puw.unit('nm')
    xyz = puw.standardize(xyz)

    return xyz


## group

@digest(form=form)
def get_group_id_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_group_id_from_group as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_group_name_from_group as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_group_type_from_group as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output


## component

@digest(form=form)
def get_component_id_from_component (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_component_id_from_component as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_component_name_from_component (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_component_name_from_component as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_component_type_from_component (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_component_type_from_component as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output


## molecule

@digest(form=form)
def get_molecule_id_from_molecule (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_molecule_id_from_molecule as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_molecule_name_from_molecule (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_molecule_name_from_molecule as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_molecule_type_from_molecule (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_molecule_type_from_molecule as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output


## chain

@digest(form=form)
def get_chain_id_from_chain (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_chain_id_from_chain as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_chain_name_from_chain (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_chain_name_from_chain as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_chain_type_from_chain (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_chain_type_from_chain as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output


## entity

@digest(form=form)
def get_entity_id_from_entity (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_entity_id_from_entity as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_entity_name_from_entity (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_entity_name_from_entity as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output

@digest(form=form)
def get_entity_type_from_entity (item, indices='all', digest=True):

    if indices is None:
        return None

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_entity_type_from_entity as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, indices=indices, digest=False)

    return output


## system

@digest(form=form)
def get_n_atoms_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_atoms_from_system as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_n_groups_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_groups_from_system as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_n_components_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_components_from_system as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_n_chains_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_chains_from_system as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_n_molecules_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_molecules_from_system as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_n_entities_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_entities_from_system as aux_get
    tmp_item = to_mdtraj_Topology(item, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_n_structures_from_system(item, digest=True):

    return item._handle.root.coordinates.shape[0]

@digest(form=form)
def get_n_bonds_from_system(item, digest=True):

    from . import to_mdtraj_Topology
    from ..mdtraj_Topology import get_n_bonds_from_system as aux_get

    tmp_item = to_mdtraj_Topology(item, digest=True, digest=False)
    output = aux_get(tmp_item, digest=False)

    return output

@digest(form=form)
def get_box_from_system(item, structure_indices='all', digest=True):

    if structure_indices is None:
        return None

    from molsysmt._private.math import serie_to_chunks
    from molsysmt.pbc import box_from_box_lengths_and_angles

    if is_all(structure_indices):
        structure_indices = np.arange(get_n_structures_from_system(item))

    starts_serie_frames, size_serie_frames = serie_to_chunks(structure_indices)

    box_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        frame_hdf5 = item.read(n_frames=size)
        cell_lengths = frame_hdf5.cell_lengths
        cell_angles = frame_hdf5.cell_angles
        box = box_from_box_lengths_and_angles(cell_lengths*puw.unit('nm'), cell_angles*puw.unit('degrees'), digest=False)
        box_list.append(puw.get_value(box))

    box = np.concatenate(box_list)
    del(box_list)

    box = box.astype('float64')

    box = box*puw.unit('nm')
    box = puw.standardize(box)

    return box

@digest(form=form)
def get_time_from_system(item, structure_indices='all', digest=True):

    if structure_indices is None:
        return None

    from molsysmt._private.math import serie_to_chunks

    if is_all(structure_indices):
        structure_indices = np.arange(get_n_structures_from_system(item))

    starts_serie_frames, size_serie_frames = serie_to_chunks(structure_indices)

    time_list = []

    for start, size in zip(starts_serie_frames, size_serie_frames):
        item.seek(start)
        frame_hdf5 = item.read(n_frames=size)
        time = frame_hdf5.time
        time_list.append(time)

    time = np.concatenate(time_list)
    del(time_list)

    time = time.astype('float64')

    time = time*puw.unit('ps')
    time = puw.standardize(time)

    return time

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', digest=True):

    if structure_indices is None:
        return None

    return None


## bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all', digest=True):

    if indices is None:
        return None

    raise NotImplementedMethodError()

@digest(form=form)
def get_bond_type_from_bond(item, indices='all', digest=True):

    if indices is None:
        return None

    raise NotImplementedMethodError()

@digest(form=form)
def get_atom_index_from_bond(item, indices='all', digest=True):

    if indices is None:
        return None

    raise NotImplementedMethodError()

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

