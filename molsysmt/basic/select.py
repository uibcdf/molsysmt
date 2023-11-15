from molsysmt._private.exceptions import NotImplementedMethodError, NotSupportedSyntaxError
from molsysmt._private.digestion import digest
import numpy as np
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt.element import _singular_element_to_plural
from .selector import _dict_select, _dict_indices_to_selection


@digest()
def select(molecular_system, selection='all', structure_indices='all', element='atom',
           mask=None, syntax='MolSysMT', to_syntax=None):
    """
    Selecting elements in a molecular system

    The indices of the elements that matches a query string can be obtained with this function.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to be extracted by the function. The selection can be
        given by a list, tuple or numpy array of element indices (0-based
        integers); or by means of a query string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_indices : tuple, list, numpy.ndarray or 'all', default 'all'
        Indices of structures (0-based integers) to be analysed by the selection function if
        spatial constraints are included.

    element: {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'system'
        The indices returned by this function corresponds to the elements specified by this input
        argument -matching the selecton criteria-.

    mask: tuple, list, numpy.ndarray or str, default=None
        Mask to be applied in the selection. If this argument is different
        from None, the selection is done only over the elements specified by this
        argument.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).

    to_syntax : str, default None
        The function will return a query string with the syntax specified by this input argument if
        its value is different from None.


    Returns
    -------

    numpy.ndarray of int
        List of element indices in agreement with the selection criterion applied over the input molecular
        system. The nature of the elements is chosen with the input argument ``element``.


    Raises
    ------

    NotSupportedFormError
        The function raises a NotSupportedFormError in case a molecular system
        is introduced with a not supported form.

    ArgumentError
        The function raises an ArgumentError in case an input argument value
        does not meet the required conditions.

    SyntaxError
        The function raises a SyntaxError in case the syntax argument takes a not supported value.


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.


    See Also
    --------

    :ref:'User Guide > Introduction > Configuration options'

    :ref:'User Guide > Introduction > Selection syntaxes'


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.select(molecular_system, element='group', selection='group_name in ["HIS","THR"]')
    array([ 20,  25,  30,  33,  53,  58, 108, 114, 141, 150, 151, 154, 156])

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Select <Tutorial_Select>`.


    """

    from molsysmt.basic import where_is_attribute
    from molsysmt.form import _dict_modules

    if is_all(selection):

        attribute = 'n_'+_singular_element_to_plural[element]
        aux_item, aux_form = where_is_attribute(molecular_system, attribute)
        n_elements = getattr(_dict_modules[aux_form], f'get_{attribute}_from_system')(aux_item)

        return np.arange(n_elements, dtype='int64').tolist()

    elif isinstance(selection, (int, np.int64, np.int32)):

        return [selection]

    elif selection is None:

        return None

    elif isinstance(selection, (list, tuple, np.ndarray)):

        if all([isinstance(ii, (int, np.int32, np.int64)) for ii in selection]):

            return list(selection)

        else:

            output = []

            for tmp_selection in selection:

                tmp_indices = select(molecular_system, selection=tmp_selection,
                                     structure_indices=structure_indices, element=element, syntax=syntax)

                output.append(tmp_indices)

            return output

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

            aux_item, aux_form = where_is_attribute(molecular_system, element+'_index')
            for aux_atom_indices in atom_indices:
                temp_output_indices = getattr(_dict_modules[aux_form],
                                              f'get_{element}_index_from_atom')(aux_item, indices=aux_atom_indices)
                output_indices.append(np.unique(temp_output_indices))

        else:

            aux_item, aux_form = where_is_attribute(molecular_system, element+'_index')
            output_indices = getattr(_dict_modules[aux_form], f'get_{element}_index_from_atom')(aux_item,
                                                                                                indices=atom_indices)
            output_indices = np.unique(output_indices)

    elif element == 'bond':

        aux_item, aux_form = where_is_attribute(molecular_system, 'inner_bond_index')
        output_indices = _dict_modules[aux_form].get_inner_bond_index_from_atom(aux_item, indices=atom_indices)

    else:

        raise NotImplementedMethodError()

    if is_all(mask):
        mask = None

    if mask is not None:
        if isinstance(mask, str):
            mask = select(molecular_system, selection=mask, element=element, syntax=syntax)
        output_indices = np.intersect1d(output_indices, mask, assume_unique=True)

    if to_syntax is None:

        output = output_indices

    else:

        if to_syntax in _dict_indices_to_selection:
            output = _dict_indices_to_selection[to_syntax](molecular_system, output_indices, element)
        else:
            raise NotSupportedSyntaxError()

    return output
