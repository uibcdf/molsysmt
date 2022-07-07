#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotWithThisFormError as _NotWithThisFormError
from molsysmt._private.exceptions import NotImplementedMethodError as _NotImplementedMethodError
from molsysmt._private.digestion import digest_item as _digest_item
from molsysmt._private.digestion import digest_indices as _digest_indices
from molsysmt._private.digestion import digest_structure_indices as _digest_structure_indices
from molsysmt import puw as _puw
import numpy as _np
from networkx import Graph as _Graph

_form='openmm.Topology'

## From atom

def get_atom_id_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output=[atom[ii].id for ii in tmp_indices]
    output=_np.array(output, dtype=int)
    del(atom)

    return output

def get_atom_name_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    output=_np.array(output)
    del(atom)

    return output

def get_atom_type_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    output=_np.array(output)
    del(atom)

    return output

def get_group_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    output=_np.array(output)
    del(atom)

    return output

def get_component_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.lib import bonds as _libbonds

    n_atoms = get_n_atoms_from_system(item)
    n_bonds = get_n_bonds_from_system(item)

    if n_bonds==0:

        output = _np.full(n_atoms, None, dtype=object)

    else:

        atom_indices = get_atom_index_from_bond(item)

        output = _libbonds.component_indices(atom_indices, n_atoms, n_bonds)
        output = _np.ascontiguousarray(output, dtype=int)

    if indices is not 'all':
        output = output[indices]

    return output

def get_chain_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_atom_index_from_atom(item, indices=indices, check=False)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)
    output = _np.array(output)

    return output

def get_molecule_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_component_index_from_atom(item, indices=indices, check=False)

    return output


def get_entity_index_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.entity import get_entity_index_from_atom as _get
    return _get(item, indices=indices)

def get_inner_bonded_atoms_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

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

    output = _np.array(output, dtype=int)

    return(output)

def get_n_inner_bonds_from_atom(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        return get_n_bonds_from_system (item)
    else:
        inner_bonded_atoms = get_inner_bonded_atoms_from_atom(item, indices=indices)
        return inner_bonded_atoms.shape[0]


def get_coordinates_from_atom(item, indices='all', structure_indices='all', check=True):

    raise _NotWithThisFormError()

## From group

def get_group_id_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].id for ii in indices]
    del(group)
    output = _np.array(output, dtype=int)

    return output

def get_group_name_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)
    output = _np.array(output, dtype=object)

    return output

def get_group_type_from_group(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.group import get_group_type_from_group_name

    if indices is 'all':
        n_indices = get_n_groups_from_system(item, check=False)
        indices = range(n_indices)

    group=list(item.residues())
    output = [get_group_type_from_group_name(group[ii].name) for ii in indices]
    del(group)
    output = _np.array(output, dtype=object)

    return output

## From component

def get_component_id_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_component_index_from_component(item, indices=indices, check=False)

    return output

def get_component_name_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    output = get_component_index_from_component(item, indices=indices, check=False)

    return output

def get_component_type_from_component(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.component import get_component_type_from_group_names

    output = []
    group_names_from_component = get_group_name_from_component(item, indices=indices, check=False)
    for group_name in group_names_from_component:
        output.append(get_component_type_from_group_names(aux))
    output = _np.array(output, dtype=object)
    return output

## From molecule

def get_molecule_id_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        output = _np.full(n_molecules, None, dtype=object)
    else:
        output = _np.full(indices.shape[0], None, dtype=object)

    return output

def get_molecule_name_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_molecules = get_n_molecules_from_system(item)
        output = _np.full(n_molecules, None, dtype=object)
    else:
        output = _np.full(indices.shape[0], None, dtype=object)

    return output

def get_molecule_type_from_molecule(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.molecule import get_molecule_type_from_group_names

    group_names_from_molecule = get_group_name_from_molecule(item, indices=indices, check=False)

    output = []

    for group_names in group_names_from_molecule:
        molecule_type = get_molecule_type_from_group_names(group_names)
        output.append(molecule_type)

    output = _np.array(output, dtype=object)

    return output

## From chain

def get_chain_id_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = _np.array(output)

    return output

def get_chain_name_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = _np.array(output)
    return output

def get_chain_type_from_chain(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_indices = get_n_chains_from_system(item, check=False)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = _np.array(output)
    return output

## From entity

def get_entity_id_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.entity import get_entity_id_from_entity as _get
    return _get(item, indices, check=False)

def get_entity_name_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.entity import get_entity_name_from_entity as _get
    return _get(item, indices)

def get_entity_type_from_entity(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    from molsysmt.element.entity import get_entity_type_from_entity as _get
    return _get(item, indices)

## From system

def get_n_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.getNumAtoms()

def get_n_groups_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.getNumResidues()

def get_n_components_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    component_index_from_atom = get_component_index_from_atom(item, indices='all')

    if component_index_from_atom[0] is None:
        n_components = 0
    else:
        output = _np.unique(component_index_from_atom)
        n_components = output.shape[0]

    return n_components

def get_n_chains_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.getNumChains()

def get_n_molecules_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    molecule_index_from_atom = get_molecule_index_from_atom(item, check=False)
    if molecule_index_from_atom[0] is None:
        n_molecules = 0
    else:
        output = _np.unique(molecule_index_from_atom)
        n_molecules = output.shape[0]
    return n_molecules

def get_n_entities_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    entity_index_from_atom = get_entity_index_from_atom(item, check=False)
    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = _np.unique(entity_index_from_atom)
        n_entities = output.shape[0]
    return n_entities

def get_n_bonds_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return item.getNumBonds()

def get_box_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)


    box = item.getPeriodicBoxVectors()

    output = None

    if box is not None:
        unit = _puw.get_unit(box)
        box = _np.array(_puw.get_value(box))
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * unit
        output = _puw.standardize(box)

    return output

def get_time_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    return None

def get_step_from_system(item, structure_indices='all', check=True):

    if check:

        _digest_item(item, _form)
        structure_indices = _digest_structure_indices(structure_indices)

    return None

def get_n_structures_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    return 0

def get_bonded_atoms_from_system(item, check=True):

    if check:

        _digest_item(item, _form)

    raise _NotImplementedMethodError

## From bond

def get_bond_order_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_bond_index_from_bond(item, indices=indices, check=False)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=_np.array(output)
    del(bond)

    return output

def get_bond_type_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    tmp_indices = get_bond_index_from_bond(item, indices=indices, check=False)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=_np.array(output)
    del(bond)

    return output

def get_atom_index_from_bond(item, indices='all', check=True):

    if check:

        _digest_item(item, _form)
        indices = _digest_indices(indices)

    if indices is 'all':
        n_bonds = get_n_bonds_from_system(item, check=False)
        indices = _np.arange(n_bonds)

    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in indices]
    output=_np.array(output)
    del(bond)

    return output

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

#######################################################################################
############## REMOVE COMMON GET METHODS NOT DEFINED FOR THIS FORM ####################
#######################################################################################

del(

    # From atom
    #get_atom_index_from_atom,
    #get_group_id_from_atom,
    #get_group_name_from_atom,
    #get_group_type_from_atom,
    #get_component_id_from_atom,
    #get_component_name_from_atom,
    #get_component_type_from_atom,
    #get_chain_id_from_atom,
    #get_chain_name_from_atom,
    #get_chain_type_from_atom,
    #get_molecule_id_from_atom,
    #get_molecule_name_from_atom,
    #get_molecule_type_from_atom,
    #get_entity_id_from_atom,
    #get_entity_name_from_atom,
    #get_entity_type_from_atom,
    #get_n_atoms_from_atom,
    #get_n_groups_from_atom,
    #get_n_components_from_atom,
    #get_n_molecules_from_atom,
    #get_n_chains_from_atom,
    #get_n_entities_from_atom,
    #get_bonded_atoms_from_atom,
    #get_bond_index_from_atom,
    #get_n_bonds_from_atom,
    #get_inner_bond_index_from_atom,

    # From group
    #get_atom_index_from_group,
    #get_atom_id_from_group,
    #get_atom_name_from_group,
    #get_atom_type_from_group,
    #get_group_index_from_group,
    #get_component_index_from_group,
    #get_component_id_from_group,
    #get_component_name_from_group,
    #get_component_type_from_group,
    #get_chain_index_from_group,
    #get_chain_id_from_group,
    #get_chain_name_from_group,
    #get_chain_type_from_group,
    #get_molecule_index_from_group,
    #get_molecule_id_from_group,
    #get_molecule_name_from_group,
    #get_molecule_type_from_group,
    #get_entity_index_from_group,
    #get_entity_id_from_group,
    #get_entity_name_from_group,
    #get_entity_type_from_group,
    #get_n_atoms_from_group,
    #get_n_groups_from_group,
    #get_n_components_from_group,
    #get_n_molecules_from_group,
    #get_n_chains_from_group,
    #get_n_entities_from_group,

    # From component
    #get_atom_index_from_component,
    #get_atom_id_from_component,
    #get_atom_name_from_component,
    #get_atom_type_from_component,
    #get_group_index_from_component,
    #get_group_id_from_component,
    #get_group_name_from_component,
    #get_group_type_from_component,
    #get_component_index_from_component,
    #get_chain_index_from_component,
    #get_chain_id_from_component,
    #get_chain_name_from_component,
    #get_chain_type_from_component,
    #get_molecule_index_from_component,
    #get_molecule_id_from_component,
    #get_molecule_name_from_component,
    #get_molecule_type_from_component,
    #get_entity_index_from_component,
    #get_entity_id_from_component,
    #get_entity_name_from_component,
    #get_entity_type_from_component,
    #get_n_atoms_from_component,
    #get_n_groups_from_component,
    #get_n_components_from_component,
    #get_n_molecules_from_component,
    #get_n_chains_from_component,
    #get_n_entities_from_component,

    # From molecule
    #get_atom_index_from_molecule,
    #get_atom_id_from_molecule,
    #get_atom_name_from_molecule,
    #get_atom_type_from_molecule,
    #get_group_index_from_molecule,
    #get_group_id_from_molecule,
    #get_group_name_from_molecule,
    #get_group_type_from_molecule,
    #get_component_index_from_molecule,
    #get_component_id_from_molecule,
    #get_component_name_from_molecule,
    #get_component_type_from_molecule,
    #get_chain_index_from_molecule,
    #get_chain_id_from_molecule,
    #get_chain_name_from_molecule,
    #get_chain_type_from_molecule,
    #get_molecule_index_from_molecule,
    #get_entity_index_from_molecule,
    #get_entity_id_from_molecule,
    #get_entity_name_from_molecule,
    #get_entity_type_from_molecule,
    #get_n_atoms_from_molecule,
    #get_n_groups_from_molecule,
    #get_n_components_from_molecule,
    #get_n_molecules_from_molecule,
    #get_n_chains_from_molecule,
    #get_n_entities_from_molecule,

    # From chain
    #get_atom_index_from_chain,
    #get_atom_id_from_chain,
    #get_atom_name_from_chain,
    #get_atom_type_from_chain,
    #get_group_index_from_chain,
    #get_group_id_from_chain,
    #get_group_name_from_chain,
    #get_group_type_from_chain,
    #get_component_index_from_chain,
    #get_component_id_from_chain,
    #get_component_name_from_chain,
    #get_component_type_from_chain,
    #get_chain_index_from_chain,
    #get_molecule_index_from_chain,
    #get_molecule_id_from_chain,
    #get_molecule_name_from_chain,
    #get_molecule_type_from_chain,
    #get_entity_index_from_chain,
    #get_entity_id_from_chain,
    #get_entity_name_from_chain,
    #get_entity_type_from_chain,
    #get_n_atoms_from_chain,
    #get_n_groups_from_chain,
    #get_n_components_from_chain,
    #get_n_molecules_from_chain,
    #get_n_chains_from_chain,
    #get_n_entities_from_chain,

    # From entity
    #get_atom_index_from_entity,
    #get_atom_id_from_entity,
    #get_atom_name_from_entity,
    #get_atom_type_from_entity,
    #get_group_index_from_entity,
    #get_group_id_from_entity,
    #get_group_name_from_entity,
    #get_group_type_from_entity,
    #get_component_index_from_entity,
    #get_component_id_from_entity,
    #get_component_name_from_entity,
    #get_component_type_from_entity,
    #get_chain_index_from_entity,
    #get_chain_id_from_entity,
    #get_chain_name_from_entity,
    #get_chain_type_from_entity,
    #get_molecule_index_from_entity,
    #get_molecule_id_from_entity,
    #get_molecule_name_from_entity,
    #get_molecule_type_from_entity,
    #get_entity_index_from_entity,
    #get_n_atoms_from_entity,
    #get_n_groups_from_entity,
    #get_n_components_from_entity,
    #get_n_molecules_from_entity,
    #get_n_chains_from_entity,
    #get_n_entities_from_entity,

    # From system
    #get_n_aminoacids_from_system,
    #get_n_nucleotides_from_system,
    #get_n_ions_from_system,
    #get_n_waters_from_system,
    #get_n_cosolutes_from_system,
    #get_n_small_molecules_from_system,
    #get_n_peptides_from_system,
    #get_n_proteins_from_system,
    #get_n_dnas_from_system,
    #get_n_rnas_from_system,
    #get_n_lipids_from_system,
    #get_coordinates_from_system,
    #get_box_shape_from_system,
    #get_box_lengths_from_system,
    #get_box_angles_from_system,
    #get_box_volume_from_system,
    #get_bonded_atoms_from_system,
    #get_bond_index_from_system,
    #get_inner_bonded_atoms_from_system,
    #get_inner_bond_index_from_system,

    # From bond
    #get_bond_index_from_bond,
    #get_n_bonds_from_bond

    )

