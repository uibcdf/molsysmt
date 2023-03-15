#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

form='mdtraj.Topology'


## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output=[item.atom(ii).serial for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

@digest(form=form)
def get_atom_name_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output=[item.atom(ii).name for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output

@digest(form=form)
def get_atom_type_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output=[item.atom(ii).element.symbol for ii in tmp_indices]
    output=np.array(output, dtype=object)
    return output

@digest(form=form)
def get_group_index_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output=[item.atom(ii).residue.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

@digest(form=form)
def get_component_index_from_atom(item, indices='all'):

    from molsysmt.element.component import get_component_index_from_atom

    output = get_component_index_from_atom(item, indices=indices)

    return output

@digest(form=form)
def get_chain_index_from_atom(item, indices='all'):

    tmp_indices = get_atom_index_from_atom(item, indices=indices)
    output=[item.atom(ii).residue.chain.index for ii in tmp_indices]
    output=np.array(output, dtype=int)
    return output

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_index_from_atom

    output = get_molecule_index_from_atom(item, indices=indices)

    return output

@digest(form=form)
def get_entity_index_from_atom(item, indices='all'):

    from molsysmt.element.entity import get_entity_index_from_atom

    output = get_entity_index_from_atom(item, indices=indices)

    return output

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all'):

    raise NotImplementedMethodError()


## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item)
        indices = np.arange(n_indices)

    output = [item.residue(ii).resSeq for ii in indices]
    output = np.array(output, dtype=int)
    return output

@digest(form=form)
def get_group_name_from_group(item, indices='all'):

    if is_all(indices):
        n_indices = get_n_groups_from_system(item)
        indices = np.arange(n_indices)

    output = [item.residue(ii).name for ii in indices]
    output = np.array(output, dtype=object)
    return output

@digest(form=form)
def get_group_type_from_group(item, indices='all'):

    from molsysmt.element.group import get_group_type_from_group_name as aux_get

    output = get_group_name_from_group(item, indices=indices)
    output = [aux_get(ii) for ii in output]
    output = np.array(output, dtype=object)

    return output


## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all'):

    from molsysmt.element.component import get_component_id_from_component

    output = get_component_id_from_component(item, indices=indices)

    return output

@digest(form=form)
def get_component_name_from_component(item, indices='all'):

    from molsysmt.element.component import get_component_name_from_component

    output = get_component_name_from_component(item, indices=indices)

    return output


@digest(form=form)
def get_component_type_from_component(item, indices='all'):

    from molsysmt.element.component import get_component_type_from_component

    output = get_component_type_from_component(item, indices=indices)

    return output


## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_id_from_molecule

    output = get_molecule_id_from_molecule(item, indices=indices)

    return output

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_name_from_molecule

    output = get_molecule_name_from_molecule(item, indices=indices)

    return output

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all'):

    from molsysmt.element.molecule import get_molecule_type_from_molecule

    output = get_molecule_type_from_molecule(item, indices=indices)

    return output


## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_name_from_chain(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_type_from_chain(item, indices='all'):

    raise NotImplementedMethodError()


## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all'):

    from molsysmt.element.entity import get_entity_id_from_entity

    output = get_entity_id_from_entity(item, indices=indices)

    return output

@digest(form=form)
def get_entity_name_from_entity(item, indices='all'):

    from molsysmt.element.entity import get_entity_name_from_entity

    output = get_entity_name_from_entity(item, indices=indices)

    return output

@digest(form=form)
def get_entity_type_from_entity(item, indices='all'):

    from molsysmt.element.entity import get_entity_type_from_entity

    output = get_entity_type_from_entity(item, indices=indices)

    return output


## From system

@digest(form=form)
def get_n_atoms_from_system(item):

    return item.n_atoms

@digest(form=form)
def get_n_groups_from_system(item):

    return item.n_residues

@digest(form=form)
def get_n_components_from_system(item):

    from molsysmt.element.component import get_n_components_from_system

    output = get_n_components_from_system(item)

    return output

@digest(form=form)
def get_n_chains_from_system(item):

    return item.n_chains

@digest(form=form)
def get_n_molecules_from_system(item):

    from molsysmt.element.molecule import get_n_molecules_from_system

    output = get_n_molecules_from_system(item)

    return output

@digest(form=form)
def get_n_entities_from_system(item):

    from molsysmt.element.entity import get_n_entities_from_system

    output = get_n_entities_from_system(item)

    return output

@digest(form=form)
def get_n_bonds_from_system(item):

    return item.n_bonds

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_box_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_time_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all'):

    raise NotWithThisFormError()


## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bond_type_from_bond(item, indices='all'):

    raise NotImplementedMethodError()

@digest(form=form)
def get_atom_index_from_bond(item, indices='all'):

    tmp_indices = get_bond_index_from_bond(item, indices=indices)
    bond = list(item.bonds)
    output=[[bond[ii].atom1.index, bond[ii].atom2.index] for ii in tmp_indices]
    output=np.array(output)
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

