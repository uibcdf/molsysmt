import numpy as np
from molsysmt.forms.common_gets import *
from molsysmt._private_tools.exceptions import *
from simtk.openmm.app import Topology as _simtk_openmm_app_Topology
from molsysmt import puw
from molsysmt.molecular_system import molecular_system_components

form_name='openmm.Topology'

is_form={
    _simtk_openmm_app_Topology:form_name,
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds', 'box']:
    has[ii]=True

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_openmm_Topology as molsysmt_Topology_from_openmm_Topology

    tmp_item, tmp_molecular_system = molsysmt_Topology_from_openmm_Topology(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_openmm_Topology as molsysmt_MolSys_from_openmm_Topology

    tmp_item, tmp_molecular_system = molsysmt_MolSys_from_openmm_Topology(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_mdtraj_Topology import to_mdtraj_Topology as mdtraj_Topology_to_mdtraj_Topology
    from mdtraj.core.topology import Topology as mdtraj_Topology

    tmp_item = mdtraj_Topology.from_openmm(item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system = mdtraj_Topology_to_mdtraj_Topology(tmp_item, tmp_molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from parmed.openmm import load_topology

    tmp_item, _ = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item = load_topology(tmp_item)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.multitool import get
    from simtk.openmm.app import Modeller

    tmp_item, _ = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    positions = get(molecular_system, target='atom', coordinates=True)
    positions = puw.convert(positions[0], 'nm', to_form='simtk.unit')
    tmp_item = Modeller(item, positions)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.multitool import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')

    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()
    tmp_item = forcefield.createSystem(item, **system_parameters)

    if molecular_mechanics.use_dispersion_correction or molecular_mechanics.ewald_error_tolerance:
        forces = {ii.__class__.__name__ : ii for ii in tmp_item.getForces()}
    if molecular_mechanics.use_dispersion_correction:
        forces['NonbondedForce'].setUseDispersionCorrection(True)
    if molecular_mechanics.ewald_error_tolerance:
        forces['NonbondedForce'].setEwaldErrorTolerance(molecular_mechanics.ewald_error_tolerance)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item, tmp_molecular_system = to_openmm_System(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_System_to_openmm_Context(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.classes.api_openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    tmp_item, tmp_molecular_system = to_openmm_System(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_System_to_openmm_Simulation(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    tmp_item, _ = to_string_pdb(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    fff.close()

    tmp_item = output_filename

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.multitool import get
    from molsysmt.version import __version__ as msm_version
    from simtk.openmm.app import PDBFile
    #from simtk.openmm.version import short_version
    from simtk.openmm import Platform # the openmm version is taken from this module (see: simtk/openmm/app/pdbfile.py)
    from io import StringIO

    coordinates = get(molecular_system, target="atom", indices=atom_indices, frame_indices=frame_indices, coordinates=True)
    topology, _ = to_openmm_Topology(item, atom_indices=atom_indices)

    tmp_io = StringIO()
    PDBFile.writeFile(topology, puw.convert(coordinates[0], 'nm', to_form='simtk.unit'), tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    #openmm_version = short_version
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    tmp_item = filedata

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile
    from molsysmt._private_tools.files_and_directories import tmp_filename
    from os import remove

    tmp_file = tmp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=tmp_file)
    tmp_item, tmp_molecular_system = file_pdb_to_openmm_PDBFile(tmp_item, molecular_system=tmp_molecular_system)

    remove(tmp_file)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    if molecular_system.trajectory_item is None:
        raise ValueError('To convert a openmm.Topology object to NGLView, a trajectory_item is needed.')
    else:
        from .api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
        tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_item, tmp_molecular_system = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item,
                molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):

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
        tmp_item = new_item

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
        tmp_item = new_item

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError

def append_frames(item, step=None, time=None, coordinates=None, box=None):

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

    from molsysmt.pbc import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.pbc import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, frame_indices=frame_indices)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box_vectors(tmp_box)

    return output

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

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

    value = puw.convert(value, 'nanometers', to_form='simtk.unit')

    n_frames = value.shape[0]

    if n_frames == 1:

        item.setPeriodicBoxVectors(value[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has corresponds to more than a frame")

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotWithThisFormError()

