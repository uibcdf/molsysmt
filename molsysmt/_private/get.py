from molsysmt._private.variables import is_all
import numpy as np

def _get_index_from_element(module, item, indices, element):

    from molsysmt.element import _element_singular_to_plural as _plural

    if indices is None:
        return None

    if is_all(indices):
        aux_get = getattr(module, f'get_n_{_plural[element]}_from_system')
        n_aux = aux_get(item)
        output = np.arange(n_aux, dtype=int)
    else:
        output = np.array(indices, dtype=int)

    return output.tolist()

def _get_inf_index_from_element(module, item, indices, inf_element, base_element):

    from molsysmt.config import large_list_length

    if indices is None:
        return None

    aux_get = getattr(module, f'get_{base_element}_index_from_{inf_index}')
    target_index = aux_get(item)

    if len(target_index)>_large_list_length:

        serie = pd.Series(target_index_from_atom)
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
            except:
                indice_dict[num] = [idx]

        if is_all(indices):
            output = [indice_dict[ii] for ii in indice_dict.keys()]
        else:
            output = [indice_dict[ii] for ii in indices]

    return output


@digest(form=form)
def _get_inf_attr_from_element(module, item, indices, inf_element, attribute, base_element):

    if indices is None:
        return None

    get_1 = getattr(module, f'get_{inf_element}_index_from_{base_element}')
    target_indices = get_1(item)
    get_2 = getattr(module, f'get_{inf_element}_{attribute}_from_{inf_element}')

    if len(aux_indices)>0:
        aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
        aux_vals = get_2(item, indices=aux_unique_indices)
        aux_output = aux_vals[aux_indices]
        output = []
        ii = 0
        for aux in target_indices:
            jj = ii+len(aux)
            output.append(aux_output[ii:jj].to_lists())
            ii = jj
        del(aux_unique_indices, aux_vals, aux_output)
    else:
        output = []

    del(target_indices)

    return output


def _get_supr_index_from_element(module, function, item, indices):

    base_element = function.split('_from_')[-1]
    spr_element = function.split('get_')[-1].split('_index_')[0]

    if indices is None:
        return None

    get_1 = getattr(module, f'get_atom_index_from_{base_element}')
    get_2 = getattr(module, f'get_{supr_element}_index_from_atom')

    atom_index_from_target = get_1(item, indices=indices)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_2(item, indices=first_atom_index_from_target)

    del(atom_index_from_target, first_atom_index_from_target)

    return output


def _get_supr_attr_from_element(module, item, indices, supr_element, attr, base_element):

    if indices is None:
        return None

    aux_element = attr.split('_')[0]
    get_1 = getattr(module, f'get_{supr_element}_index_from_{base_element}')
    get_2 = getattr(module, f'get_{supr_element}_{attr}_from_{supr_element}')

    aux_indices = get_1(item, indices=indices)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_2(item, indices=aux_unique_indices)
    output = np.array(aux_vals)[aux_new_indices]

    del(aux_indices, aux_unique_indices, aux_vals, aux_new_indices)

    return output.tolist()

def _get_n_elements(module, function, item, indices):

    if indices is None:
        return 0

    if is_all(indices):
        from molsysmt.element import _element_singular_to_plural as _plural
        element =  attr.split('_from_')[-1]
        aux_get = getattr(module, f'get_n_{_plural[element]}_from_system')
        output = aux_get(item)
    else:
        output = indices.shape[0]

    return output


def _get_n_sup_from_element(module, function, item, indices):

    if indices is None:
        return 0

    from molsysmt.element import _element_plural_to_singular as _singular

    base_element =  function.split('_from_')[-1]
    supr_element_plural = function.split('_get_n_')[-1].split('_from_')[0]
    supr_element = _singular(supr_element_plural)

    if is_all(indices):
        aux_get = getattr(module, f'get_n_{supr_element_plural}_from_system')
        output = aux_get(item)
    else:
        aux_get = getattr(module, f'get_{supr_element}_index_from_{base_element}')
        output = aux_get(item, indices=indices)
        output = np.unique(output).shape[0]

    return output


def _get_n_group_type_from_element(module, item, indices, group_type, element):

    aux_get = getattr(module, f'get_group_index_from_{element}')
    group_indices = aux_get(item, indices=indices)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices)
    output = (group_types==group_type).sum()

    return output


def _get_n_molecule_type_from_element(module, item, indices, molecule_type, element):

    aux_get = getattr(__main__, f'get_molecule_index_from_{element}')
    molecule_indices = aux_get(item, indices=indices)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices)
    output = (molecule_types==molecule_type).sum()

    return output

