import numpy as np
from molsysmt.forms.common_gets import *
from molsysmt._private_tools.exceptions import *
from simtk.openmm.app import Topology as _simtk_openmm_app_Topology

form_name='openmm.Topology'

is_form={
    _simtk_openmm_app_Topology:form_name,
}

info=["",""]
with_topology=True
with_trajectory=False
with_coordinates=False
with_box=True
with_bonds=True
with_parameters=False

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_Topology as molsysmt_Topology_from_openmm_Topology

    tmp_item = molsysmt_Topology_from_openmm_Topology(item, molecular_system, atom_indices=atom_indices)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_openmm_Topology as molsysmt_MolSys_from_openmm_Topology

    tmp_item = molsysmt_MolSys_from_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import extract as extract_mdtraj_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology

    tmp_item = mdtraj_Topology.from_openmm(item, molecular_system)
    tmp_item = extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    from parmed.openmm import load_topology as openmm_Topology_to_parmed_Structure

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)

    return tmp_item

def to_yank_Topography(item, molecular_system, atom_indices='all', frame_indices='all'):

    from yank import Topography as yank_Topography

    tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = yank_Topography(tmp_item)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.multitool import get
    from simtk.openmm.app import Modeller

    positions = get(trajectory_item, target='atom', indices=atom_indices,
                    frame_indices=frame_indices, coordinates=True)
    tmp_item = Modeller(item, positions[0])

    return tmp_item

def to_openmm_System(item, molecular_system, atom_indices='all', frame_indices='all',
                     forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                     rigid_water=True, remove_cm_motion=False, hydrogen_mass=None, switch_distance=None,
                     flexible_constraints=False, use_dispersion_correction=False, ewald_error_tolerance=0.0001,
                     water_model=None, implicit_solvent=None, implicit_solvent_salt_conc='0.0 mol/L',
                     implicit_solvent_kappa='0.0 1/nm', solute_dielectric=1.0, solvent_dielectric=78.5):

    from molsysmt._private_tools.forcefields import digest as digest_forcefields
    from molsysmt._private_tools.simulation_parameters import digest as digest_simulation_parameters
    from simtk.openmm.app import ForceField

    if forcefield is None:
        raise ValueError('This conversion needs the input argument "forcefield".')

    forcefield_omm_parameters=digest_forcefields(forcefield, 'OpenMM',
                                                 implicit_solvent=implicit_solvent,
                                                 water_model=water_model)

    system_omm_parameters=digest_simulation_parameters(engine='OpenMM', non_bonded_method=non_bonded_method,
            non_bonded_cutoff=non_bonded_cutoff, constraints=constraints, rigid_water=rigid_water,
            remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass,
            switch_distance=switch_distance, flexible_constraints=flexible_constraints,
            use_dispersion_correction=use_dispersion_correction, ewald_error_tolerance=ewald_error_tolerance,
            implicit_solvent=implicit_solvent,
            implicit_solvent_salt_conc=implicit_solvent_salt_conc, implicit_solvent_kappa=implicit_solvent_kappa,
            solute_dielectric=solute_dielectric, solvent_dielectric=solvent_dielectric)


    forcefield_generator = ForceField(*forcefield_omm_parameters)
    tmp_item = forcefield_generator.createSystem(item, **system_omm_parameters)

    if use_dispersion_correction or ewald_error_tolerance:
        forces = {ii.__class__.__name__ : ii for ii in tmp_item.getForces()}
        if use_dispersion_correction:
            forces['NonbondedForce'].setUseDispersionCorrection(True)
        if ewald_error_tolerance:
            forces['NonbondedForce'].setEwaldErrorTolerance(ewald_error_tolerance)

    return tmp_item

def to_openmm_Simulation(item, molecular_system, atom_indices='all', frame_indices='all',
                         forcefield=None, non_bonded_method='no_cutoff', non_bonded_cutoff=None, constraints=None,
                         rigid_water=True, remove_cm_motion=True, hydrogen_mass=None, switch_distance=None,
                         flexible_constraints=False, use_dispersion_correction=False, ewald_error_tolerance=0.0001,
                         water_model=None, implicit_solvent=None, implicit_solvent_kappa='0.0 1/nm',
                         solute_dielectric=1.0, solvent_dielectric=78.5, integrator='Langevin',
                         temperature='300.0 K', collisions_rate='1.0 1/ps', integration_timestep='2.0 fs', platform='CUDA',
                         constraint_tolerance=None):

    from .api_openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation
    from molsysmt import convert, get

    topology = item
    positions = get(trajectory_item, target='atom', selection=atom_indices, frame_indices=frame_indices, coordinates=True)

    system = to_openmm_System(item, atom_indices=atom_indices, frame_indices=frame_indices,
        forcefield=forcefield, non_bonded_method=non_bonded_method, non_bonded_cutoff=non_bonded_cutoff, constraints=constraints,
        rigid_water=rigid_water, remove_cm_motion=remove_cm_motion, hydrogen_mass=hydrogen_mass, switch_distance=switch_distance,
        flexible_constraints=flexible_constraints,
        use_dispersion_correction=use_dispersion_correction, ewald_error_tolerance=ewald_error_tolerance,
        water_model=water_model, implicit_solvent=implicit_solvent,
        implicit_solvent_kappa=implicit_solvent_kappa, solute_dielectric=solute_dielectric, solvent_dielectric=solvent_dielectric,
        **kwargs)

    tmp_item = openmm_System_to_openmm_Simulation(system, topology_item=topology,
            trajectory_item=positions, atom_indices='all', frame_indices=0,
            integrator=integrator, temperature=temperature, collisions_rate=collisions_rate,
            integration_timestep=integration_timestep, platform=platform, constraint_tolerance=constraint_tolerance)

    return tmp_item

def to_pdb(item, molecular_system, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.multitool import get as _get
    from molsysmt.multitool import __version__ as msm_version
    from simtk.openmm.app import PDBFile
    #from simtk.openmm.version import short_version
    from simtk.openmm import Platform # the openmm version is taken from this module (see: simtk/openmm/app/pdbfile.py)
    from io import StringIO

    coordinates = _get(trajectory_item, target="atom", indices=atom_indices, frame_indices=frame_indices, coordinates=True)

    if atom_indices is 'all':
        tmp_item = item
    else:
        tmp_item = extract(item, atom_indices=atom_indices)

    tmp_io = StringIO()
    PDBFile.writeFile(tmp_item, coordinates[0], tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    #openmm_version = short_version
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    if output_filename=='.pdb':
        return filedata
    else:
        with open(output_filename, 'w') as file:
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
        del(newAtoms)
        new_item.setPeriodicBoxVectors(item.getPeriodicBoxVectors())
        return new_item

def copy(item):

    from simtk.openmm.app import Topology
    new_item = Topology()
    newAtoms = {}
    for chain in item.chains():
        newChain = new_item.addChain(chain.id)
        for residue in chain.residues():
            newResidue = new_item.addResidue(residue.name, newChain, residue.id, residue.insertionCode)
            for atom in residue.atoms():
                newAtom = new_item.addAtom(atom.name, atom.element, newResidue, atom.id)
                newAtoms[atom] = newAtom
    for bond in item.bonds():
        new_item.addBond(newAtoms[bond[0]], newAtoms[bond[1]])
    del(newAtoms)
    new_item.setPeriodicBoxVectors(item.getPeriodicBoxVectors())
    return new_item

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

def to_nglview_NGLView(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    return view_with_NGLView(item, trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)

def view_with_NGLView(item, trajectory_item=None, atom_indices='all', frame_indices='all'):

    if trajectory_item is None:
        raise ValueError('To convert a openmm.Topology object to NGLView, a trajectory_item is needed.')
    else:
        from .api_molsysmt_MolSys import to_nglview_NGLView as molsysmt_MolSys_to_nglview_NGLView
        tmp_item = to_molsysmt_MolSys(item, trajectory_item=trajectory_item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item = molsysmt_MolSys_to_nglview_NGLView(tmp_item)
        return tmp_item

def merge(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def concatenate(list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def add(item, list_items, list_atom_indices, list_frame_indices):

    raise NotImplementedError

def append(item, list_items, list_atom_indices, list_frame_indices):

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

    from molsysmt.elements.entity import entity_id_from_entity as get
    return get(item, indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_name_from_entity as get
    return get(item, indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_type_from_entity as get
    return get(item, indices)

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

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_volume_from_box_vectors(tmp_box)

    return output

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

def get_has_topology_from_system(item, indices='all', frame_indices='all'):

    return with_topology

def get_has_parameters_from_system(item, indices='all', frame_indices='all'):

    return with_parameters

def get_has_coordinates_from_system(item, indices='all', frame_indices='all'):

    return with_coordinates

def get_has_box_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_box:
        tmp_box = get_box_from_system(item, indices=indices, frame_indices=frame_indices)
        if tmp_box[0] is not None:
            output = True

    return output

def get_has_bonds_from_system(item, indices='all', frame_indices='all'):

    output = False

    if with_topology:
        if get_n_bonds_from_system(item, indices=indices, frame_indices=frame_indices):
            output = True

    return output

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

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    n_frames = value.shape[0]

    if n_frames == 1:

        item.setPeriodicBoxVectors(value[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has corresponds to more than a frame")

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotWithThisFormError(NotWithThisFormMessage)

