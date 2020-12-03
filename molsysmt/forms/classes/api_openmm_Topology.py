from os.path import basename as _basename
from simtk.openmm.app import Topology as _simtk_openmm_app_Topology
import numpy as np
import simtk.unit as unit
from molsysmt.forms.common_gets import *

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    'openmm.Topology':form_name,
    _simtk_openmm_app_Topology:form_name
}

info=["",""]
with_topology=True
with_coordinates=False
with_box=False
with_parameters=False

def to_molsysmt_Topology(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_Topology as molsysmt_Topology_from_openmm_Topology
    return molsysmt_Topology_from_openmm_Topology(item, atom_indices=atom_indices)

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_openmm_Topology as molsysmt_MolSys_from_openmm_Topology
    return molsysmt_MolSys_from_openmm_Topology(item, atom_indices=atom_indices)

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import extract as extract_mdtraj_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology
    tmp_item = mdtraj_Topology.from_openmm(item)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from parmed.openmm import load_topology as openmm_Topology_to_parmed_Structure
    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from yank import Topography as yank_Topography
    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = yank_Topography(tmp_item)
    return tmp_item

def to_openmm_Modeller(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    from molsysmt import get
    from simtk.openmm.app import Modeller

    positions = get(trajectory_item, target='atom', indices=atom_indices,
                    frame_indices=frame_indices, coordinates=True)
    tmp_item = Modeller(item, positions[0])
    return tmp_item

def to_openmm_System(item, trajectory_item=None, atom_indices='all', frame_indices='all',
        forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
        rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
        flexible_constraints=False, **kwargs):

    from molsysmt.utils.forcefields import digest as digest_forcefields
    from molsysmt.utils.simulation_parameters import digest as digest_simulation_parameters
    from simtk.openmm.app import ForceField

    if forcefield is None:
        raise ValueError('This conversion needs the input argument "forcefield".')

    forcefield_omm_parameters=digest_forcefields(forcefield, 'openmm')
    system_omm_parameters=digest_simulation_parameters( engine='openmm', non_bonded_method=non_bonded_method,
            non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
            remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
            switch_distance=switch_distance, flexible_constraints=flexible_constraints)

    forcefield_generator = ForceField(*forcefield_omm_parameters)
    tmp_item = forcefield_generator.createSystem(item, **system_omm_parameters)

    return tmp_item

def to_openmm_Simulation(item, topology_item=None, trajectory_item=None, atom_indices='all', frame_indices='all',
        forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
        rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
        flexible_constraints=False, integrator='Langevin', temperature=300.0*unit.kelvin,
        friction=1.0/unit.picoseconds, integration_time_step=2.0*unit.femtoseconds, platform='CUDA',
        **kwargs):

    from .api_openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation
    from molsysmt import convert, get

    topology = item
    positions = get(trajectory_item, target='atom', selection=atom_indices, frame_indices=frame_indices, coordinates=True)

    system = to_openmm_System(item, atom_indices=atom_indices, frame_indices=frame_indices,
        forcefield=forcefield, non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
        rigid_water=rigid_water, remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
        flexible_constraints=flexible_constraints, **kwargs)

    tmp_item = openmm_System_to_openmm_Simulation(system, topology_item=topology,
            trajectory_item=positions, atom_indices='all', frame_indices=0,
            integrator=integrator, temperature=temperature, friction=friction,
            integration_time_step=integration_time_step, platform=platform)

    return tmp_item

def to_pdb(item, output_filepath=None, trajectory_item=None, atom_indices='all',
           frame_indices='all'):

    from molsysmt import get as _get
    from simtk.openmm.app import PDBFile
    from simtk.openmm.version import short_version
    from io import StringIO

    coordinates = _get(trajectory_item, target="atom", indices=atom_indices, frame_indices=frame_indices, coordinates=True)

    if atom_indices is 'all':
        tmp_item = item
    else:
        tmp_item = extract(item, atom_indices=atom_indices)

    tmp_io = StringIO()
    PDBFile.writeFile(tmp_item, coordinates[0], tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    filedata = filedata.replace('WITH OPENMM '+short_version, 'WITH OPENMM '+short_version+' BY MOLSYSMT')
    tmp_io.close()
    del(tmp_io)

    if output_filepath=='.pdb':
        return filedata
    else:
        with open(output_filepath, 'w') as file:
            file.write(filedata)
        pass


def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:

        from simtk.openmm.app import Topology
        new_item = Topology()
        atom_indices_to_be_kept = atom_indices
        newAtoms = {}
        set_atom_indices = set(atom_indices_to_be_kept)
        for chain in item.chains():
            needNewChain = True
            for residue in chain.residues():
                needNewResidue = True
                for atom in residue.atoms():
                    if atom.index in set_atom_indices:
                        if needNewChain:
                            newChain = new_item.addChain(chain.id)
                            needNewChain = False;
                        if needNewResidue:
                            newResidue = new_item.addResidue(residue.name, newChain, residue.id, residue.insertionCode)
                            needNewResidue = False;
                        newAtom = new_item.addAtom(atom.name, atom.element, newResidue, atom.id)
                        newAtoms[atom] = newAtom
        for bond in item.bonds():
            if bond[0].index in set_atom_indices and bond[1].index in set_atom_indices:
                new_item.addBond(newAtoms[bond[0]], newAtoms[bond[1]])
        return new_item

def copy(item):

    from copy import deepcopy
    return deepcopy(item)

def merge_two_items(item1, item2):

    raise NotImplementedError

def select_with_Amber(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MDTraj(item, selection):

    tmp_item = to_mdtraj_Topology(item, selection='all', syntaxis='MDTraj')
    return tmp_item.select(selection)

def select_with_MolSysMT(item, selection):

    from .api_molsysmt_Topology import select_with_MolSysMT as select_molsysmt_Topology_with_MolSysMT
    tmp_item = to_molsysmt_Topology(item)
    return select_molsysmt_Topology_with_MolSysMT(tmp_item, selection)

def to_NGLView(item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

#### Get

## Atom

def get_atom_id_from_atom(item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output=[atom[ii].id for ii in tmp_indices]
    output=np.array(output, dtype=int)
    del(atom)
    return output

def get_atom_name_from_atom(item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    output=np.array(output)
    del(atom)
    return output

def get_atom_type_from_atom(item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    output=np.array(output)
    del(atom)
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    output=np.array(output)
    del(atom)
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import component_index_from_atom as get
    return get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)
    output =np.array(output)
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_index_from_atom as _get
    return _get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    output=[]

    if indices is 'all':

        for bond in item.bonds():
            output.append([bond.atom1.index, bond.atom2.index])

    else:

        set_indices = set(indices)

        for bond in item.bonds():
            if bond.atom1.index in set_indices:
                if bond.atom2.index in set_indices:
                    output.append([bond.atom1.index, bond.atom2.index])

    output = np.array(output, dtype=int)

    return(output)

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## group

def get_group_id_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].id for ii in indices]
    del(group)
    output = np.array(output, dtype=int)
    return output

def get_group_name_from_group(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)
    output =np.array(output, dtype=object)
    return output

def get_group_type_from_group(item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import name_to_type

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [name_to_type(group[ii].name) for ii in indices]
    del(group)
    output = np.array(output, dtype=object)
    return output

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as get
    return get(item, indices=indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_name_from_atom as get
    return get(item, indices=indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import get_component_type_from_atom as get
    return get(item, indices=indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_id_from_molecule as get
    return get(item, indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_name_from_molecule as get
    return get(item, indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_type_from_molecule as get
    return get(item, indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = np.array(output)
    return output

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_type_from_entity as get
    return get(item, indices)

    #atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    #entity_id_from_atom = get_entity_id_from_atom (item, indices='all', frame_indices=frame_indices)

    #output = []
    #for atom_indices in atom_index_from_entity:
    #    output.append(entity_id_from_atom[atom_indices[0]])

    #output = np.array(output)
    #return output

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_name_from_entity as get
    return get(item, indices)

    #atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    #entity_name_from_atom = get_entity_name_from_atom (item, indices='all', frame_indices=frame_indices)

    #output = []
    #for atom_indices in atom_index_from_entity:
    #    output.append(entity_name_from_atom[atom_indices[0]])

    #output = _array(output)
    #return output

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import get_entity_type_from_entity as get
    return get(item, indices)

    #atom_index_from_entity = get_atom_index_from_entity (item, indices=indices, frame_indices=frame_indices)
    #entity_type_from_atom = get_entity_type_from_atom (item, indices='all', frame_indices=frame_indices)

    #output = []
    #for atom_indices in atom_index_from_entity:
    #    output.append(entity_type_from_atom[atom_indices[0]])

    #output = np.array(output)
    #return output


## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.getNumAtoms()

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.getNumResidues()

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import n_components_from_system as _get
    return _get(item)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.getNumChains()

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import n_molecules_from_system as _get
    return _get(item)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import n_entities_from_system as _get
    return _get(item)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return item.getNumBonds()

def get_box_from_system(item, indices='all', frame_indices='all'):

    from numpy import array as _array

    box = item.getPeriodicBoxVectors()

    if box is not None:
        box_unit = box.unit
        box = np.array(box._value)
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * box_unit

    output=None

    if box is not None:
        if frame_indices is 'all':
            output=box
        else:
            output=box[frame_indices,:,:]

    return output

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_bonds = get_n_bonds_from_system(item)
        indices = np.arange(n_bonds)

    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in indices]
    output=np.array(output)
    del(bond)
    return output

