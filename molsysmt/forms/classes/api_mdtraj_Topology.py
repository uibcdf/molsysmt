from molsysmt._private_tools.exceptions import *
from mdtraj.core.topology import Topology as _mdtraj_Topology
import numpy as np
from molsysmt.forms.common_gets import *
from molsysmt.molecular_system import molecular_system_components

form_name='mdtraj.Topology'

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

info=["",""]

has = molecular_system_components.copy()
for ii in ['elements', 'bonds']:
    has[ii]=True

## To other form

def to_string_aminoacids3(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item, tmp_molecular_system = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item = ''.join([ r.name.title() for r in item.residues ])
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_string_aminoacids1(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_string_aminoacids3 import to_string_aminoacids1 as aminoacids3_to_aminoacids1

    tmp_item, tmp_molecular_system = to_string_aminoacids3(item, molecular_system)
    tmp_item, tmp_molecular_system = aminoacids3_to_aminoacids1(tmp_item, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.topology.classes import from_mdtraj_Topology as molsysmt_Topology_from_mdtraj_Topology

    tmp_item, tmp_molecular_system = molsysmt_Topology_from_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system, atom_indices='all', frame_indices='all'):

    tmp_item, tmp_molecular_system = to_mdtraj_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices, copy_if_all=False)
    tmp_item = tmp_item.to_openmm()
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_parmed_Structure(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure

    tmp_item, tmp_molecular_system = to_openmm_Topology(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = openmm_Topology_to_parmed_Structure(tmp_form, tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', frame_indices='all'):

    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile

    tmp_item, tmp_molecular_system = to_parmed_Structure(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = GromacsTopologyFile.from_structure(tmp_item)
    tmp_molecular_system = tmp_molecular_system.combine_with_items(tmp_item)

    return tmp_item, tmp_molecular_system

def to_file_top(item, molecular_system, atom_indices='all', frame_indices='all'):

    from .api_parmed_GromacsTopologyFile import to_file_top as parmed_GromacsTopologyFile_to_file_top

    tmp_item, tmp_molecular_system = to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = parmed_GromacsTopologyFile_to_file_top(tmp_item, tmp_molecular_system, output_filename=output_filename)

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', frame_indices='all', copy_if_all=True):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract_item(item)
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            tmp_molecular_system = molecular_system
    else:
        tmp_item = extract_item(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def extract_item(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):

        tmp_item = item.copy()

    else:

        from mdtraj.core.topology import Topology
        from mdtraj.utils import ilen

        atom_indices_to_be_kept = set(atom_indices)
        newTopology = Topology()
        old_atom_to_new_atom = {}

        for chain in item._chains:
            newChain = newTopology.add_chain()
            for group in chain._groups:
                resSeq = getattr(group, 'resSeq', None) or group.index
                newResidue = newTopology.add_group(group.name, newChain,
                                                     resSeq, group.segment_id)
                for atom in group._atoms:
                    if atom.index in atom_indices_to_be_kept:
                        try:  # OpenMM Topology objects don't have serial attributes, so we have to check first.
                            serial = atom.serial
                        except AttributeError:
                            serial = None
                        newAtom = newTopology.add_atom(atom.name, atom.element,
                                                       newResidue, serial=serial)
                        old_atom_to_new_atom[atom] = newAtom

        bondsiter = item.bonds
        if not hasattr(bondsiter, '__iter__'):
            bondsiter = bondsiter()

        for bond in bondsiter:
            try:
                atom1, atom2 = bond
                newTopology.add_bond(old_atom_to_new_atom[atom1],
                                     old_atom_to_new_atom[atom2],
                                     type=bond.type,
                                     order=bond.order)
            except KeyError:
                pass
                # we only put bonds into the new topology if both of their partners
                # were indexed and thus HAVE a new atom

        # Delete empty groups
        newTopology._groups = [r for r in newTopology._groups if len(r._atoms) > 0]
        for chain in newTopology._chains:
            chain._groups = [r for r in chain._groups if len(r._atoms) > 0]

        # Delete empty chains
        newTopology._chains = [c for c in newTopology._chains
                               if len(c._groups) > 0]
        # Re-set the numAtoms and numResidues
        newTopology._numAtoms = ilen(newTopology.atoms)
        newTopology._numResidues = ilen(newTopology.groups)

        tmp_item = newTopology

    return tmp_item

def add(item, from_item, atom_indices='all', frame_indices='all'):

    raise NotImplementedError()

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    raise NotImplementedError()

########################
### Get
########################

## Atom

def get_atom_id_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output=[item.atom(ii).serial for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

def get_atom_name_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output=[item.atom(ii).name for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output

def get_atom_type_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output=[item.atom(ii).element.symbol for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output

def get_group_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output=[item.atom(ii).residue.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

def get_component_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import component_index_from_atom

    return component_index_from_atom(item, indices=indices)

def get_chain_index_from_atom (item, indices='all', frame_indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices, frame_indices=frame_indices)
    output=[item.atom(ii).residue.chain.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

def get_molecule_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_index_from_atom as get
    return get(item, indices=indices)

def get_entity_index_from_atom (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_index_from_atom as get
    return get(item, indices=indices)

def get_inner_bond_index_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_inner_bonded_atoms_from_atom (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_inner_bonds_from_atom (item, indices='all', frame_indices='all'):

    if indices is 'all':
        return get_n_inner_bonds_from_system (item)
    else:
        raise NotImplementedError

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## group

def get_group_id_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = np.arange(n_indices)

    output = [item.residue(ii).resSeq for ii in indices]
    output = np.array(output, dtype=int)
    return output

def get_group_name_from_group (item, indices='all', frame_indices='all'):

    if indices is 'all':
        n_indices = get_n_groups_from_system(item)
        indices = np.arange(n_indices)

    output = [item.residue(ii).name for ii in indices]
    output = np.array(output, dtype=object)
    return output

def get_group_type_from_group (item, indices='all', frame_indices='all'):

    from molsysmt.elements.group import group_type_from_group
    return group_type_from_group(item, indices=indices)

## component

def get_component_id_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import component_id_from_component
    return component_id_from_component(item, indices=indices)

def get_component_name_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import component_name_from_component
    return component_name_from_component(item, indices=indices)

def get_component_type_from_component (item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import component_type_from_component
    return component_type_from_component(item, indices=indices)

## molecule

def get_molecule_id_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_id_from_molecule
    return molecule_id_from_molecule(item, indices=indices)

def get_molecule_name_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_name_from_molecule
    return molecule_name_from_molecule(item, indices=indices)

def get_molecule_type_from_molecule (item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import molecule_type_from_molecule
    return molecule_type_from_molecule(item, indices=indices)

## chain

def get_chain_id_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_name_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_chain_type_from_chain (item, indices='all', frame_indices='all'):

    raise NotImplementedError

## entity

def get_entity_id_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_id_from_entity
    return entity_id_from_entity(item, indices=indices)

def get_entity_name_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_name_from_entity
    return entity_name_from_entity(item, indices=indices)

def get_entity_type_from_entity (item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import entity_type_from_entity
    return entity_type_from_entity(item, indices=indices)

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    return item.n_atoms

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    return item.n_residues

def get_n_components_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.component import n_components_from_system as get
    return get(item)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    return item.n_chains

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.molecule import n_molecules_from_system as get
    return get(item)

def get_n_entities_from_system(item, indices='all', frame_indices='all'):

    from molsysmt.elements.entity import n_entities_from_system as get
    return get(item)

def get_n_bonds_from_system(item, indices='all', frame_indices='all'):

    return item.n_bonds

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_shape_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_lengths_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_angles_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_box_volume_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_time_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_step_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return 0

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    raise NotImplementedError

## bond

def get_bond_order_from_bond(item, indices='all', frame_indices='all'):

#    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
#    bond = list(item.bonds())
#    output=[bond[ii].order for ii in tmp_indices]
#    output=_array(output)
#    del(bond)
#    return output

    pass

def get_bond_type_from_bond(item, indices='all', frame_indices='all'):

#    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
#    bond = list(item.bonds())
#    output=[bond[ii].type for ii in tmp_indices]
#    output=_array(output)
#    del(bond)
#    return output

    pass

def get_atom_index_from_bond(item, indices='all', frame_indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices, frame_indices=frame_indices)
    bond = list(item.bonds)
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in tmp_indices]
    output=np.array(output)
    del(bond)
    return output

###### Set

def set_box_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

def set_coordinates_to_system(item, indices='all', frame_indices='all', value=None):

    raise NotImplementedError

