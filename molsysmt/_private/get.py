from molsysmt._private.variables import is_all
from molsysmt.element import is_composed_of, is_element
from molsysmt.element import _plural_elements_to_singular, _singular_element_to_plural
from molsysmt.element.group import _plural_group_types_to_singular
from molsysmt.element.group import is_group_type
from molsysmt.element.molecule import _plural_molecule_types_to_singular
from molsysmt.element.molecule import is_molecule_type
import numpy as np
import pandas as pd
from networkx import Graph

def _auxiliary_getter(function, item, indices):

    words = function.__name__.split('_')

    if 'n' == words[1]:

        aux_word = function.__name__.split('get_n_')[-1].split('_from_')[0].replace('_', ' ')

        if is_element(aux_word):

            involved_element = _plural_elements_to_singular[words[2]]
            base_element = words[-1]

            if involved_element == base_element:

                return _get_n_elements(function.__module__, base_element, item, indices)

            else:

                if is_composed_of(base_element, involved_element):

                    return _get_n_inf_from_element(function.__module__, involved_element, base_element, item, indices)

                else:

                    return _get_n_sup_from_element(function.__module__, involved_element, base_element, item, indices)

        elif is_group_type(aux_word):

            base_element = words[-1]
            if aux_word in _plural_group_types_to_singular:
                aux_word = _plural_group_types_to_singular[aux_word]

            return _get_n_group_type_from_element(function.__module__, aux_word, base_element, item, indices)

        elif is_molecule_type(aux_word):

            base_element = words[-1]
            if aux_word in _plural_molecule_types_to_singular:
                aux_word = _plural_molecule_types_to_singular[aux_word]

            return _get_n_molecule_type_from_element(function.__module__, aux_word, base_element, item, indices)

            pass

    elif 'index' == words[2]:

        involved_element = words[1]
        base_element = words[-1]

        if involved_element == base_element:

            return _get_index_from_element(function.__module__, base_element, item, indices)

        else:

            if is_composed_of(base_element, involved_element):

                return _get_inf_index_from_element(function.__module__, involved_element, base_element, item, indices)

            else:

                return _get_sup_index_from_element(function.__module__, involved_element, base_element, item, indices)

    elif is_element(words[1]):

        involved_element = words[1]
        attribute = words[2]
        base_element = words[-1]

        if involved_element == base_element:

            raise NotImplementedError

        else:

            if is_composed_of(base_element, involved_element):

                return _get_inf_attr_from_element(function.__module__, involved_element, attribute, base_element, item,
                                                  indices)

            else:

                return _get_sup_attr_from_element(function.__module__, involved_element, attribute, base_element, item,
                                                  indices)

    elif function.__name__ == 'get_bond_index_from_atom':

        return _get_bond_index_from_atom(function.__module__, item, indices)

    elif function.__name__ == 'get_bonded_atoms_from_atom':

        return _get_bonded_atoms_from_atom(function.__module__, item, indices)

    elif function.__name__ == 'get_inner_bond_index_from_atom':

        return _get_inner_bond_index_from_atom(function.__module__, item, indices)

    elif function.__name__ == 'get_inner_bonded_atoms_from_atom':

        return _get_inner_bonded_atoms_from_atom(function.__module__, item, indices)

    elif function.__name__ == 'get_n_bonds_from_atom':

        return _get_n_bonds_from_atom(function.__module__, item, indices)

    elif function.__name__ == 'get_n_inner_bonds_from_atom':

        return _get_n_inner_bonds_from_atom(function.__module__, item, indices)



# n elements


def _get_n_elements(module, element, item, indices):

    if is_all(indices):
        aux_get = getattr(module, f'get_n_{_singular_element_to_plural[element]}_from_system')
        output = aux_get(item)
    else:
        output = indices.shape[0]

    return output


def _get_n_inf_from_element(module, involved_element, base_element, item, indices):

    aux_get = getattr(module, f'get_{involved_element}_index_from_{base_element}')
    output = aux_get(item, indices)
    output = [ii.shape[0] for ii in output]

    return output


def _get_n_sup_from_element(module, involved_element, base_element, item, indices):

    if is_all(indices):
        aux_get = getattr(module, f'get_n_{_singular_element_to_plural[involved_element]}_from_system')
        output = aux_get(item)
    else:
        aux_get = getattr(module, f'get_{involved_element}_index_from_{base_element}')
        output = aux_get(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


# n index

def _get_index_from_element(module, element, item, indices):

    if is_all(indices):
        aux_get = getattr(module, f'get_n_{_singular_element_to_plural[element]}_from_system')
        n_aux = aux_get(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output.tolist()


def _get_inf_index_from_element(module, involved_element, base_element, item, indices):

    from molsysmt.config import large_list_length

    aux_get = getattr(module, f'get_{base_element}_index_from_{involved_element}')
    target_index = aux_get(item)

    if len(target_index) > large_list_length:

        serie = pd.Series(target_index)
        groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
        if is_all(indices):
            output = [ii.tolist() for ii in groups_serie]
        else:
            output = [groups_serie[ii].tolist() for ii in indices]

    else:

        indice_dict = {}

        for idx, num in enumerate(target_index):
            try:
                indice_dict[num].append(idx)
            except KeyError:
                indice_dict[num] = [idx]

        if is_all(indices):
            output = [indice_dict[ii] for ii in indice_dict.keys()]
        else:
            output = [indice_dict[ii] for ii in indices]

    return output


def _get_sup_index_from_element(module, involved_element, base_element, item, indices):

    get_1 = getattr(module, f'get_atom_index_from_{base_element}')
    get_2 = getattr(module, f'get_{involved_element}_index_from_atom')

    atom_index_from_target = get_1(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_2(item, indices=first_atom_index_from_target)

    del atom_index_from_target, first_atom_index_from_target

    return output


# attrs


def _get_inf_attr_from_element(module, involved_element, attribute, base_element, item, indices):

    get_1 = getattr(module, f'get_{involved_element}_index_from_{base_element}')
    target_indices = get_1(item)
    get_2 = getattr(module, f'get_{involved_element}_{attribute}_from_{involved_element}')

    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_2(item, indices=aux_unique_indices)
    aux_output = aux_vals[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].to_lists())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


def _get_sup_attr_from_element(module, involved_element, attribute, base_element, item, indices):

    get_1 = getattr(module, f'get_{involved_element}_index_from_{base_element}')
    get_2 = getattr(module, f'get_{involved_element}_{attribute}_from_{involved_element}')

    aux_indices = get_1(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_2(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


# n group or molecule types


def _get_n_group_type_from_element(module, group_type, element, item, indices):

    get_1 = getattr(module, f'get_group_index_from_{element}')
    get_2 = getattr(module, 'get_group_type_from_group')

    group_indices = get_1(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_2(item, indices=group_indices)
    output = (group_types == group_type).sum()

    return output


def _get_n_molecule_type_from_element(module, molecule_type, element, item, indices):

    get_1 = getattr(module, f'get_molecule_index_from_{element}')
    get_2 = getattr(module, 'get_molecule_type_from_molecule')

    molecule_indices = get_1(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_2(item, indices=molecule_indices)
    output = (molecule_types == molecule_type).sum()

    return output


# bonds

def _get_bond_index_from_atom(module, item, indices):

    aux_get = getattr(module, 'get_bonded_atoms_from_bond')

    output = None

    G = Graph()
    edges = aux_get(item)
    n_bonds = edges.shape[0]
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

        indices = get_atom_index_from_atom(item)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n['index'] for n in G[ii].values()]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    del G, edges, edge_indices

    return output


def _get_bonded_atoms_from_atom(module, item, indices):

    output = None

    aux_get_1 = getattr(module, 'get_bonded_atoms_from_bond')
    aux_get_2 = getattr(module, 'get_atom_index_from_atom')

    G = Graph()
    edges = aux_get_1(item)
    G.add_edges_from(edges)

    if is_all(indices):

        indices = aux_get_2(item)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    for ii in range(output.shape[0]):
        output[ii] = np.sort(output[ii])

    del G, edges

    return output


def _get_bonded_atoms_from_atom(module, item, indices='all'):

    output = None

    aux_get_1 = getattr(module, 'get_bonded_atoms_from_bond')
    aux_get_2 = getattr(module, 'get_atom_index_from_atom')

    G = Graph()
    edges = aux_get_1(item)
    G.add_edges_from(edges)

    if is_all(indices):

        indices = aux_get_2(item)

    output = []

    for ii in indices:
        if ii in G:
            output.append(np.array([n for n in G[ii]]))
        else:
            output.append(np.array([]))

    output = np.array(output, dtype=object)

    for ii in range(output.shape[0]):
        output[ii] = np.sort(output[ii])

    del G, edges

    return output


def _get_inner_bond_index_from_atom(module, item, indices):

    raise NotImplementedError


def _get_inner_bonded_atoms_from_atom(module, item, indices):

    aux_get_1 = getattr(module, 'get_bonded_atoms_from_bond')
    aux_get_2 = getattr(module, 'get_inner_bond_index_from_atom')

    if is_all(indices):

        output = aux_get_1(item)

    else:

        bond_indices = aux_get_2(item, indices=indices)
        output = aux_get_1(item, indices=bond_indices)
        del bond_indices

    output = output[np.lexsort((output[:, 1], output[:, 0]))]

    return output

def _get_n_bonds_from_atom(module, item, indices):

    aux_get = getattr(module, 'get_bonded_atoms_from_bond')

    bond_indices = aux_get(item, indices)
    output = len(bond_indices)
    del bond_indices

    return(output)

def _get_n_inner_bonds_from_atom(module, item, indices):

    aux_get = getattr(module, 'get_inner_bonded_atoms_from_bond')

    bond_indices = aux_get(item, indices)
    output = len(bond_indices)
    del bond_indices

    return(output)





