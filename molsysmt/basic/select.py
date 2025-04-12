from molsysmt._private.exceptions import NotImplementedMethodError, NotSupportedSyntaxError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt.element import _singular_element_to_plural
from .selector import _dict_select, _dict_indices_to_selection


@digest()
def select(molecular_system, selection='all', structure_indices='all', element='atom',
           mask=None, syntax='MolSysMT', to_syntax=None, skip_digestion=False):
    """
    Selecting elements from a molecular system.

    This function returns the indices of elements that satisfy a selection query. The selection
    can be based on topological or structural attributes, and applied to different element levels
    (atoms, groups, molecules, etc.). If a `to_syntax` is specified, the function returns the
    translated selection query in the desired syntax instead of indices.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of the :ref:`supported forms <Introduction_Forms>` to be analyzed
        by the function.

    selection : str, tuple, list, or numpy.ndarray, default 'all'
        Element selection to be applied to the molecular system. Can be provided as a list, tuple, or
        array of 0-based indices; or as a string query following any of the
        :ref:`supported selection syntaxes <Introduction_Selection>`.

    structure_indices : str, tuple, list, or numpy.ndarray, default 'all'
        Indices of structures (frames) to be considered for spatially constrained selections.

    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'atom'
        Element level on which the selection is applied. The returned indices correspond to this level.

    mask : str, tuple, list, or numpy.ndarray, optional
        Optional mask that restricts the selection to a subset of elements. Works similarly to the
        `selection` argument, and can be used to define a region of interest.

    syntax : str, default 'MolSysMT'
        Selection syntax used to interpret the `selection` string, if applicable.

    to_syntax : str, optional
        If specified, returns a translated query string in the desired syntax instead of numerical indices.

    Returns
    -------
    list or str
        If `to_syntax` is None, returns an array of 0-based indices of the selected elements.
        If `to_syntax` is given, returns a translated selection query string.

    Raises
    ------
    NotSupportedFormError
        Raised if the molecular system is provided in an unsupported form.

    ArgumentError
        Raised if one or more input arguments are invalid.

    Notes
    -----
    The list of supported molecular system forms is described in:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    For selection syntax and query expression examples, see:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :func:`molsysmt.basic.get`
        Retrieving attributes of selected elements.

    :func:`molsysmt.basic.remove`
        Removing selected atoms or structures from a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.basic.select(molecular_system, element='group', selection='group_name in ["HIS", "THR"]')
    [ 20,  25,  30,  33,  53,  58, 108, 114, 141, 150, 151, 154, 156]

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Select <Tutorial_Select>`

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import where_is_attribute
    from molsysmt.form import _dict_modules

    if is_all(selection):

        attribute = 'n_'+_singular_element_to_plural[element]
        aux_item, aux_form = where_is_attribute(molecular_system, attribute, skip_digestion=True)
        n_elements = getattr(_dict_modules[aux_form], f'get_{attribute}_from_system')(aux_item)

        output_indices = np.arange(n_elements, dtype='int64').tolist()

    elif isinstance(selection, (int, np.int64, np.int32)):

        output_indices = [selection]

    elif selection is None:

        output_indices = None

    elif isinstance(selection, (list, tuple, np.ndarray)):

        if all([isinstance(ii, (int, np.int32, np.int64)) for ii in selection]):

            output_indices = list(selection)

        else:

            output_indices = []

            for tmp_selection in selection:

                tmp_indices = select(molecular_system, selection=tmp_selection,
                                     structure_indices=structure_indices, element=element, syntax=syntax,
                                     skip_digestion=True)

                output_indices.append(tmp_indices)

    else:

        if syntax in _dict_select:
            atom_indices = _dict_select[syntax](molecular_system, selection, structure_indices)
        else:

            raise NotSupportedSyntaxError()

        if element == 'atom':

            output_indices = atom_indices

        elif element in ['group', 'component', 'chain', 'molecule', 'entity']:

            if is_iterable_of_iterables(atom_indices):

                output_indices = []

                aux_item, aux_form = where_is_attribute(molecular_system, element+'_index', skip_digestion=True)
                for aux_atom_indices in atom_indices:
                    temp_output_indices = getattr(_dict_modules[aux_form],
                                                  f'get_{element}_index_from_atom')(aux_item, indices=aux_atom_indices)
                    output_indices.append(np.unique(temp_output_indices).tolist())

            else:

                aux_item, aux_form = where_is_attribute(molecular_system, element+'_index', skip_digestion=True)
                output_indices = getattr(_dict_modules[aux_form], f'get_{element}_index_from_atom')(aux_item,
                                                                                                    indices=atom_indices)
                output_indices = np.unique(output_indices).tolist()

        elif element == 'bond':

            aux_item, aux_form = where_is_attribute(molecular_system, 'inner_bond_index', skip_digestion=True)
            output_indices = _dict_modules[aux_form].get_inner_bond_index_from_atom(aux_item, indices=atom_indices)
            output_indices = np.unique(np.concatenate(output_indices)).tolist()

        else:

            raise NotImplementedMethodError()

    if is_all(mask):
        mask = None

    if (mask is not None) and (output_indices is not None):
        if isinstance(mask, str):
            mask = select(molecular_system, selection=mask, element=element, syntax=syntax, skip_digestion=True)
        output_indices = np.intersect1d(output_indices, mask, assume_unique=True)

    if to_syntax is None:

        output = output_indices

    else:

        if to_syntax in _dict_indices_to_selection:
            output = _dict_indices_to_selection[to_syntax](molecular_system, output_indices, element)
        else:
            raise NotSupportedSyntaxError()

    return output
