#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.execfile import execfile
from molsysmt._private.exceptions import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

form='parmed.Structure'

## From atom

@digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):

    output = item.coordinates

    if len(output.shape)==2 and output.shape[1]==3:
        output = output[np.newaxis,:,:]

    if output is None:
        return output

    if not is_all(indices):
        output = output[:,indices,:]
    if not is_all(structure_indices):
        output = output[structure_indices,:,:]

    if not puw.is_quantity(output):
        output = puw.quantity(output,'angstroms')

    output = puw.standardize(output)

    return output

## From group

@digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

## From component

@digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

## From molecule

@digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

## From chain

@digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

## From entity

@digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()


## From system

@digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    return len(item.atoms)

@digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    return len(item.residues)

@digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):

    if is_all(structure_indices):
        if item.coordinates is None:
            return 0
        else:
            return item.coordinates.shape[0]
    else:
        return len(structure_indices)

@digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):

    output = item.box

    if output is None:
        return output

    if not is_all(structure_indices):
        output = output[structure_indices,:,:]

    if not puw.is_quantity(output):
        output = puw.quantity(output,'angstroms')

    output = puw.standardize(output)

    return output

@digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):

    return None

@digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):

    return None

## From bond

@digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    raise NotImplementedMethodError()

@digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    tmp_bonds = []
    for bond in item.bonds:
        tmp_bonds.append([bond.atom1.idx,bond.atom2.idx])

    return tmp_bonds

#######################################################################################
######### DO NOT TOUCH THE FOLLOWING LINES, JUST INCLUDE THEM AS THEY ARE #############
#######################################################################################

from os import path
this_folder = path.dirname(path.abspath(__file__))
common_get = path.join(this_folder, '../../_private/common_get.py')
execfile(common_get, globals(), locals())
del(path, this_folder, common_get)

