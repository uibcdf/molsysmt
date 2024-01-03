#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

form='openmm.Topology'

## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    atom=list(item.atoms())
    output=[atom[ii].id for ii in tmp_indices]
    output=np.array(output, dtype=int)
    del(atom)

    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    atom=list(item.atoms())
    output=[atom[ii].name for ii in tmp_indices]
    output=np.array(output)
    del(atom)

    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    atom=list(item.atoms())
    output=[atom[ii].element.symbol for ii in tmp_indices]
    output=np.array(output)
    del(atom)

    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.index for ii in tmp_indices]
    output=np.array(output)
    del(atom)

    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    from molsysmt.element.component import get_component_index as _get

    output = _get(item, element='atom', selection=indices, redefine_indices=True)

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    atom=list(item.atoms())
    output = [atom[ii].residue.chain.index for ii in tmp_indices]
    del(atom)
    output = np.array(output)

    return output


@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    output = get_component_index_from_atom(item, indices=indices)

    return output


@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    from molsysmt.element.entity import get_entity_index as _get
    return _get(item, element='atom', selection=indices, redefine_molecules=True,
            redefine_indices=True)


@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    output=[]

    if is_all(indices):

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

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    if is_all(indices):
        return get_n_bonds_from_system(item)
    else:
        inner_bonded_atoms = get_inner_bonded_atoms_from_atom(item, indices=indices)
        return inner_bonded_atoms.shape[0]


@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all'):

    raise _NotWithThisFormError()

## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].id for ii in indices]
    del(group)
    output = np.array(output, dtype=int)

    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [group[ii].name for ii in indices]
    del(group)
    output = np.array(output, dtype=object)

    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    from molsysmt.element.group.get_group_type import _get_group_type_from_group_name

    if is_all(indices):
        n_indices = get_n_groups_from_system(item)
        indices = range(n_indices)

    group=list(item.residues())
    output = [_get_group_type_from_group_name(group[ii].name) for ii in indices]
    del(group)
    output = np.array(output, dtype=object)

    return output

## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    output = get_component_index_from_component(item, indices=indices)

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    output = get_component_index_from_component(item, indices=indices)

    return output

@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    from molsysmt.element.component import get_component_type as _get

    return _get(item, element='component', selection=indices, redefine_components=True)

## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_id as _get

    return _get(item, element='molecule', selection=indices, redefine_molecules=True)

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_name as _get

    return _get(item, element='molecule', selection=indices, redefine_molecules=True)

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_type as _get

    return _get(item, element='molecule', selection=indices, redefine_molecules=True)

## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    chain=list(item.chains())
    output = [chain[ii].id for ii in indices]
    del(chain)
    output = np.array(output)

    return output

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_chains_from_system(item)
        indices = range(n_indices)

    output = [None for ii in indices]
    output = np.array(output)
    return output

## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    from molsysmt.element.entity import get_entity_id_from_entity as _get
    return _get(item, indices)

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    from molsysmt.element.entity import get_entity_name_from_entity as _get
    return _get(item, indices)

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    from molsysmt.element.entity import get_entity_type_from_entity as _get
    return _get(item, indices)

## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    return item.getNumAtoms()

@digest(form=form)
def get_n_groups_from_system(item):

    return item.getNumResidues()

@digest(form=form)
def get_n_components_from_system(item):

    component_index_from_atom = get_component_index_from_atom(item, indices='all')

    if component_index_from_atom[0] is None:
        n_components = 0
    else:
        output = np.unique(component_index_from_atom)
        n_components = output.shape[0]

    return n_components

@digest(form=form)
def get_n_chains_from_system(item):

    return item.getNumChains()

@digest(form=form)
def get_n_molecules_from_system(item):

    molecule_index_from_atom = get_molecule_index_from_atom(item)
    if molecule_index_from_atom[0] is None:
        n_molecules = 0
    else:
        output = np.unique(molecule_index_from_atom)
        n_molecules = output.shape[0]
    return n_molecules

@digest(form=form)
def get_n_entities_from_system(item):

    entity_index_from_atom = get_entity_index_from_atom(item)
    if entity_index_from_atom[0] is None:
        n_entities = 0
    else:
        output = np.unique(entity_index_from_atom)
        n_entities = output.shape[0]
    return n_entities

@digest(form=form)
def get_n_bonds_from_system(item):

    return item.getNumBonds()

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    return 0

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    box = item.getPeriodicBoxVectors()

    output = None

    if box is not None:
        unit = puw.get_unit(box)
        box = np.array(puw.get_value(box))
        box = box.reshape(1, box.shape[0], box.shape[1])
        box = box * unit
        output = puw.standardize(box)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    return None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    return None


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices)
    bond = list(item.bonds())
    output=[bond[ii].order for ii in tmp_indices]
    output=np.array(output)
    del(bond)

    return output

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices)
    bond = list(item.bonds())
    output=[bond[ii].type for ii in tmp_indices]
    output=np.array(output)
    del(bond)

    return output

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all'):

    if is_all(indices):
        n_bonds = get_n_bonds_from_system(item)
        indices = np.arange(n_bonds)

    bond = list(item.bonds())
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in indices]
    output=np.sort(np.array(output))
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

