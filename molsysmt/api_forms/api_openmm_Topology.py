from molsysmt._private_tools.exceptions import *

from molsysmt.tools.openmm_Topology.is_openmm_Topology import is_openmm_Topology as is_form
from molsysmt.tools.openmm_Topology.extract import extract
from molsysmt.tools.openmm_Topology.add import add
from molsysmt.tools.openmm_Topology.merge import merge
from molsysmt.tools.openmm_Topology.append_structures import append_structures
from molsysmt.tools.openmm_Topology.concatenate_structures import concatenate_structures
from molsysmt.tools.openmm_Topology.get import *
from molsysmt.tools.openmm_Topology.set import *

form_name='openmm.Topology'
form_type='class'
form_info=["",""]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : False,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}


def to_molsysmt_Topology(item, molecular_system, atom_indices='all'):

    from molsysmt.tools.openmm_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = openmm_Topology_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.openmm_Topology import to_molsysmt_MolSys as openmm_Topology_to_molsysmt_MolSys
    from molsysmt.basic import get

    coordinates, box = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, box=True)

    tmp_item = openmm_Topology_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                  coordinates=coordinates, box=box, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all'):

    from molsysmt.tools.openmm_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    tmp_item = openmm_Topology_to_mdtraj_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_parmed_Structure(item, molecular_system, atom_indices='all'):

    from molsysmt.tools.openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item = openmm_Topology_to_parmed_Structure(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.openmm_Topology import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True)

    tmp_item = openmm_Topology_to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_openmm_System(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.tools.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System
    from molsysmt.basic import convert

    molecular_mechanics = convert(molecular_system, to_form='molsysmt.MolecularMechanics')

    forcefield = molecular_mechanics.to_openmm_ForceField()
    system_parameters = molecular_mechanics.get_openmm_System_parameters()

    tmp_item = openmm_Topology_to_openmm_System(item, atom_indices=atom_indices,
                                                forcefield=forcefield, parameters=parameters,
                                                check=False)

    return tmp_item

def to_openmm_Context(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_openmm_System import to_openmm_Context as openmm_System_to_openmm_Context

    tmp_item, tmp_molecular_system = to_openmm_System(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = openmm_System_to_openmm_Context(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    tmp_item, tmp_molecular_system = to_openmm_System(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item, tmp_molecular_system = openmm_System_to_openmm_Simulation(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):

    tmp_item, _ = to_string_pdb_text(item, molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)

    with open(output_filename, 'w') as fff:
        fff.write(tmp_item)

    fff.close()

    tmp_item = output_filename

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_pdb_text(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get
    from molsysmt import __version__ as msm_version
    from openmm.app import PDBFile
    from openmm import Platform # the openmm version is taken from this module (see: openmm/app/pdbfile.py)
    from io import StringIO

    coordinates = get(molecular_system, target="atom", indices=atom_indices, structure_indices=structure_indices, coordinates=True)
    topology, _ = to_openmm_Topology(item, atom_indices=atom_indices, copy_if_all=False)

    tmp_io = StringIO()
    PDBFile.writeFile(topology, puw.convert(coordinates[0], 'nm', to_form='openmm.unit'), tmp_io, keepIds=True)
    filedata = tmp_io.getvalue()
    openmm_version = Platform.getOpenMMVersion()
    filedata = filedata.replace('WITH OPENMM '+openmm_version, 'WITH OPENMM '+openmm_version+' BY MOLSYSMT '+msm_version)
    tmp_io.close()
    del(tmp_io)

    tmp_item = filedata

    tmp_molecular_system = molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_openmm_PDBFile(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.api_forms.api_file_pdb import to_openmm_PDBFile as file_pdb_to_openmm_PDBFile
    from molsysmt._private_tools.files_and_directories import temp_filename
    from os import remove

    tmp_file = temp_filename(extension='pdb')
    tmp_item, tmp_molecular_system = to_file_pdb(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, output_filename=tmp_file)
    tmp_item, tmp_molecular_system = file_pdb_to_openmm_PDBFile(tmp_item, molecular_system=tmp_molecular_system)

    remove(tmp_file)

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    if molecular_system.trajectory_item is None:
        raise ValueError('To convert a openmm.Topology object to NGLView, a trajectory_item is needed.')
    else:
        from .api_molsysmt_MolSys import to_nglview_NGLWidget as molsysmt_MolSys_to_nglview_NGLWidget
        tmp_item, tmp_molecular_system = to_molsysmt_MolSys(item, molecular_system=molecular_system, atom_indices=atom_indices, structure_indices=structure_indices)
        tmp_item, tmp_molecular_system = molsysmt_MolSys_to_nglview_NGLWidget(tmp_item,
                molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (structure_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices)

    return tmp_item, tmp_molecular_system

def extract(item, atom_indices='all', structure_indices='all'):

    if (atom_indices is 'all') and (structure_indices is 'all'):

        from openmm.app import Topology
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

        from openmm.app import Topology
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

def merge(item_1, item_2):

    raise NotImplementedError

def add(to_item, item):

    raise NotImplementedError

def append_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

def concatenate_structures(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError

#### Get

## Atom

def get_atom_id_from_atom(item, indices='all', structure_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    atom=list(item.atoms())
    output=[atom[ii].id for ii in tmp_indices]
    output=np.array(output, dtype=int)
    del(atom)
    return output

def get_atom_name_from_atom(item, indices='all', structure_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    output=np.array(output)
    del(atom)
    return output

def get_atom_type_from_atom(item, indices='all', structure_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    output=np.array(output)
    del(atom)
    return output

def get_group_index_from_atom (item, indices='all', structure_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    output=np.array(output)
    del(atom)
    return output

def get_component_index_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import component_index_from_atom as get
    return get(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', structure_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, structure_indices=structure_indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)
    output =np.array(output)
    return output

def get_molecule_index_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import molecule_index_from_atom as _get
    return _get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_bond_index_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_n_bonds_from_atom (item, indices='all', structure_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', structure_indices='all'):

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

def get_n_inner_bonds_from_atom (item, indices='all', structure_indices='all'):

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        inner_bonded_atoms = get_inner_bonded_atoms_from_atom(item, indices=indices,
                structure_indices=structure_indices)
        return inner_bonded_atoms.shape[0]

## group

def get_group_id_from_group(item, indices='all', structure_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].id for ii in indices]
    del(group)
    output = np.array(output, dtype=int)
    return output

def get_group_name_from_group(item, indices='all', structure_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)
    output =np.array(output, dtype=object)
    return output

def get_group_type_from_group(item, indices='all', structure_indices='all'):

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

def get_component_id_from_component (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_index_from_atom as get
    return get(item, indices=indices)

def get_component_name_from_component (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_name_from_atom as get
    return get(item, indices=indices)

def get_component_type_from_component (item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import get_component_type_from_atom as get
    return get(item, indices=indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import molecule_id_from_molecule as get
    return get(item, indices)

def get_molecule_name_from_molecule (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import molecule_name_from_molecule as get
    return get(item, indices)

def get_molecule_type_from_molecule (item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import molecule_type_from_molecule as get
    return get(item, indices)

## chain

def get_chain_id_from_chain (item, indices='all', structure_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = np.array(output)
    return output

def get_chain_name_from_chain (item, indices='all', structure_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

def get_chain_type_from_chain (item, indices='all', structure_indices='all'):

    if indices is 'all':
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

## entity

def get_entity_id_from_entity (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import entity_id_from_entity as get
    return get(item, indices)

def get_entity_name_from_entity (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import entity_name_from_entity as get
    return get(item, indices)

def get_entity_type_from_entity (item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import entity_type_from_entity as get
    return get(item, indices)

## system

def get_n_atoms_from_system(item, indices='all', structure_indices='all'):

    return item.getNumAtoms()

def get_n_groups_from_system(item, indices='all', structure_indices='all'):

    return item.getNumResidues()

def get_n_components_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.elements.component import n_components_from_system as _get
    return _get(item)

def get_n_chains_from_system(item, indices='all', structure_indices='all'):

    return item.getNumChains()

def get_n_molecules_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.elements.molecule import n_molecules_from_system as _get
    return _get(item)

def get_n_entities_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.elements.entity import n_entities_from_system as _get
    return _get(item)

def get_n_bonds_from_system(item, indices='all', structure_indices='all'):

    return item.getNumBonds()

def get_box_from_system(item, indices='all', structure_indices='all'):

    from numpy import array as _array

    box = item.getPeriodicBoxVectors()

    output = None

    if box is not None:
        unit = puw.get_unit(box)
        box = np.array(puw.get_value(box))
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * unit
        output = puw.standardize(box)

    return output

def get_box_shape_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_shape_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = box_shape_from_box_vectors(tmp_box)

    return output

def get_box_lengths_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_lengths_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = box_lengths_from_box_vectors(tmp_box)

    return output

def get_box_angles_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_angles_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    output = box_angles_from_box_vectors(tmp_box)

    return output

def get_box_volume_from_system(item, indices='all', structure_indices='all'):

    from molsysmt.pbc import box_volume_from_box_vectors

    tmp_box = get_box_from_system(item, structure_indices=structure_indices)
    if tmp_box is None:
        output=None
    else:
        output = box_volume_from_box_vectors(tmp_box)

    return output

def get_n_structures_from_system(item, indices='all', structure_indices='all'):

    return None

def get_bonded_atoms_from_system(item, indices='all', structure_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', structure_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, structure_indices=structure_indices)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output

def get_bond_type_from_bond(item, indices='all', structure_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, structure_indices=structure_indices)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output

def get_atom_index_from_bond(item, indices='all', structure_indices='all'):

    if indices is 'all':
        n_bonds = get_n_bonds_from_system(item)
        indices = np.arange(n_bonds)

    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in indices]
    output=np.array(output)
    del(bond)
    return output

###### Set

def set_box_to_system(item, indices='all', structure_indices='all', value=None):

    value = puw.convert(value, 'nanometers', to_form='openmm.unit')

    n_structures = value.shape[0]

    if n_structures == 1:

        item.setPeriodicBoxVectors(value[0])

    else:

        raise ValueError("The box to set in to a openmm.Topology has corresponds to more than a frame")

def set_coordinates_to_system(item, indices='all', structure_indices='all', value=None):

    raise NotWithThisFormError()

