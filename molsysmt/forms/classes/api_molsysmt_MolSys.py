from molsysmt._private_tools.exceptions import *
from molsysmt.native.molsys import MolSys as _molsysmt_MolSys
from molsysmt import puw
import numpy as np
from molsysmt.molecular_system import molecular_system_components

form_name='molsysmt.MolSys'

is_form={
    _molsysmt_MolSys : form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'coordinates', 'box']:
    has[ii]=True

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_molsysmt_Trajectory as molsysmt_MolSys_to_molsysmt_Trajectory

    tmp_item =  molsysmt_MolSys_to_molsysmt_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_XYZ(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_XYZ as molsysmt_MolSys_to_XYZ

    tmp_item = molsysmt_MolSys_to_XYZ(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_aminoacids3_seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import to_aminoacids3_seq as molsysmt_topology_to_aminoacids3_seq

    tmp_item = molsysmt_topology_to_aminoacids3_seq(item.topology, molecular_system, atom_indices=atom_indices)

    return tmp_item

def to_aminoacids1_seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import to_aminoacids1_seq as molsysmt_topology_to_aminoacids1_seq

    tmp_item = molsysmt_topology_to_aminoacids1_seq(item.topology, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1_seq import to_biopython_Seq as aminoacids1_to_biopython_Seq

    tmp_item = to_aminoacids1_seq(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_Seq(tmp_item)

    return tmp_item

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1_seq import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord

    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_SeqRecord(tmp_item)

    return tmp_item

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_molsysmt_Topology import to_mdtraj_Topology as molsysmt_Topology_to_mdtraj_Topology

    tmp_item = molsysmt_Topology_to_mdtraj_Topology(item.topology, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller

    tmp_item = molsysmt_MolSys_to_openmm_Modeller(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_openmm_System as molsysmt_MolSys_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_System(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_openmm_Simulation as molsysmt_MolSys_to_openmm_Simulation

    tmp_item = molsysmt_MolSys_to_openmm_Simulation(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.native.io.molsys.files import to_pdb as molsysmt_MolSys_to_pdb

    tmp_item = molsysmt_MolSys_to_pdb(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)

    return tmp_item

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import to_pdbfixer_PDBFixer as molsysmt_MolSys_to_pdbfixer_PDBFixer

    tmp_item = molsysmt_MolSys_to_pdbfixer_PDBFixer(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def select_with_MDTraj(item, selection):

    from .api_molsysmt_Topology import select_with_MDTraj as select_Topology_with_MDTraj
    return select_Topology_with_MDTraj(item.topology, selection)

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_Topology_with_MolSysMT
    return select_Topology_with_MolSysMT(item.topology, selection)

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        return item.extract(atom_indices=atom_indices, frame_indices=frame_indices)

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from nglview import show_molsysmt
    tmp_view = show_molsysmt(item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_view

def copy(item):

    return item.copy()

def add(item, from_item, atom_indices='all', frame_indices='all'):

    item.add(from_item, selection=atom_indices, frame_indices=frame_indices)
    pass

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    item.trajectory.append_frames(step=step, time=time, coordinates=coordinates, box=box)
    pass

###### Get

## atom

def get_index_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_id_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_id_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_name_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_name_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_type_from_atom (item, indices='all', frame_indices='all'):

    return get_atom_type_from_atom(item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_id_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_name_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_type_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_id_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_name_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_type_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_name_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_id_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_type_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_name_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_id_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_type_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_id_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_name_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_type_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_id_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_name_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_type_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_bonded_atoms_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_bond_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_bond_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_inner_bond_index_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_inner_bonded_atoms_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_inner_bonds_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_charge_from_atom as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_atom as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_frame_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_frame_from_atom as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_atom(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_n_frames_from_atom as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

## group

def get_index_from_group (item, indices='all', frame_indices='all'):

    return get_group_index_from_group (item, indices=indices, frame_indices=frame_indices)

def get_id_from_group (item, indices='all', frame_indices='all'):

    return get_group_id_from_group (item, indices=indices, frame_indices=frame_indices)

def get_name_from_group (item, indices='all', frame_indices='all'):

    return get_group_name_from_group (item, indices=indices, frame_indices=frame_indices)

def get_type_from_group (item, indices='all', frame_indices='all'):

    return get_group_type_from_group (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_id_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_name_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_type_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_index_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_index_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_id_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_name_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_type_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_name_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_index_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_id_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_type_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_name_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_index_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_id_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_type_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_index_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_id_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_name_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_type_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_index_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_id_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_name_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_type_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_group (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_charge_from_group as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_group(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_group as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

## component

def get_index_from_component (item, indices='all', frame_indices='all'):

    return get_component_index_from_component (item, indices=indices, frame_indices=frame_indices)

def get_id_from_component (item, indices='all', frame_indices='all'):

    return get_component_id_from_component (item, indices=indices, frame_indices=frame_indices)

def get_name_from_component (item, indices='all', frame_indices='all'):

    return get_component_name_from_component (item, indices=indices, frame_indices=frame_indices)

def get_type_from_component (item, indices='all', frame_indices='all'):

    return get_component_type_from_component (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_id_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_name_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_type_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_index_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_index_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_id_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_id_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_name_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_name_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_type_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_type_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_name_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_index_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_id_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_type_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_name_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_index_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_id_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_type_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_index_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_id_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_name_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_type_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_index_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_id_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_name_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_type_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_component (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_charge_from_component as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_component(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_component as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)


## molecule

def get_index_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_index_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_id_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_id_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_name_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_name_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_type_from_molecule (item, indices='all', frame_indices='all'):

    return get_molecule_type_from_molecule (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_id_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_name_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_type_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_index_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_index_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_id_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_id_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_name_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_name_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_type_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_type_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_name_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_index_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_id_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_type_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_name_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_index_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_id_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_type_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_index_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_id_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_name_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_type_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_index_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_id_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_name_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_type_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_molecule (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_charge_from_molecule as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_molecule(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_molecule as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)


## chain

def get_index_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_index_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_id_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_id_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_name_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_name_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_type_from_chain (item, indices='all', frame_indices='all'):

    return get_chain_type_from_chain (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_id_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_name_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_type_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_index_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_index_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_id_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_id_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_name_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_name_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_type_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_type_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_name_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_index_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_id_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_type_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_name_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_index_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_id_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_type_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_index_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_id_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_name_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_type_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_index_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_id_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_name_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_type_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_chain (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_charge_from_chain as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_chain(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_chain as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

## entity

def get_index_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_index_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_id_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_id_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_name_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_name_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_type_from_entity (item, indices='all', frame_indices='all'):

    return get_entity_type_from_entity (item, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_id_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_id_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_name_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_name_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_type_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_type_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_index_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_index_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_id_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_id_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_name_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_name_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_group_type_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_group_type_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_name_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_index_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_id_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_component_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_component_type_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_name_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_index_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_id_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_chain_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_chain_type_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_index_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_id_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_name_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecule_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_molecule_type_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_index_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_index_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_id_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_name_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_entity_type_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_entity (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_charge_from_entity as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_entity(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_entity as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)


## system

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_bonded_atoms_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_atoms_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_groups_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_components_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_chains_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_molecules_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_entities_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_aminoacids_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_aminoacids_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_nucleotides_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_nucleotides_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_ions_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_waters_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_cosolutes_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_cosolutes_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_small_molecules_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_small_molecules_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_peptides_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_peptides_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_proteins_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_proteins_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_dnas_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_dnas_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_rnas_from_system (item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_dnas_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_mass_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_charge_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_mass_from_system as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_coordinates_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_box_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_box_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_box_shape_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    tmp_box_lengths = item.trajectory.get_box_lengths()
    if tmp_box_lengths is not None and frame_indices is not 'all':
        tmp_box_lengths = tmp_box_lengths[frame_indices,:]
    return tmp_box_lengths

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    tmp_box_angles = item.trajectory.get_box_angles()
    if tmp_box_angles is not None and frame_indices is not 'all':
        tmp_box_angles = tmp_box_angles[frame_indices,:]
    return tmp_box_angles

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_volume_from_box_vectors
    tmp_box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
    return box_volume_from_box_vectors(tmp_box)

def get_time_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_time_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_step_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_step_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_frame_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_frame_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Trajectory import get_n_frames_from_system as _get
    return _get(item.trajectory, indices=indices, frame_indices=frame_indices)

## bond

def get_index_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_index_from_bond(item, indices=indices)

def get_order_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_order_from_bond(item, indices=indices)

def get_type_from_bond(item, indices='all', frame_indices='all'):

    return get_bond_type_from_bond(item, indices=indices)

def get_bond_index_from_bond(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_bond_index_from_bond as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_bond_order_from_bond as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_bond_type_from_bond as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_atom_index_from_bond as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_bonds_from_bond(item, indices='all', frame_indices='all'):

    from .api_molsysmt_Topology import get_n_bonds_from_bond as _get
    return _get(item.topology, indices=indices, frame_indices=frame_indices)

###### Set

## Atom

def set_coordinates_to_atom(item, indices='all', frame_indices='all', value=None):

    value = puw.standardize(value)

    if indices is 'all':
        if item.trajectory.coordinates.shape[1]!=value.shape[1]:
            raise ValueError('New coordinates array has different number of atoms')

    if frame_indices is 'all':
        if item.trajectory.coordinates.shape[0]!=value.shape[0]:
            raise ValueError('New coordinates array has different number of frames')

    if indices is 'all':
        if frame_indices is 'all':
            item.trajectory.coordinates[:,:,:] = value[:,:,:]
        else:
            item.trajectory.coordinates[frame_indices,:,:] = value[:,:,:]
    else:
        if frame_indices is 'all':
            item.trajectory.coordinates[:,indices,:] = value[:,:,:]
        else:
            item.trajectory.coordinates[np.ix_(frame_indices, indices)]=value[:,:,:]

## System

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    item.trajectory.box = value
    pass

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    return set_coordinates_to_atom(item, indices='all', frame_indices=frame_indices, value=value)

