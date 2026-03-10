from molsysmt._private.smonitor import NotImplementedMethodError, NotSupportedSyntaxError
from molsysmt._private.arg_digestion import arg_digest
import numpy as np
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt.element import _singular_element_to_plural
from .selector import _dict_select, _dict_indices_to_selection


from smonitor import signal

@signal(tags=['api', 'selection'])
@arg_digest()
def select(molecular_system, selection='all', structure_indices='all', element='atom',
           mask=None, syntax='MolSysMT', to_syntax=None, skip_digestion=False):
    """
    Selecting elements from a molecular system.

    This function returns the indices of elements that match a selection query (unless `to_syntax` is used). The selection
    can be based on topological or structural attributes and applied at different hierarchical
    levels such as atoms, groups, components, molecules, chains or entities. If `to_syntax` is specified, the function
    returns a translated selection string instead of indices.

    Selection strings must follow one of the syntaxes described in :ref:`Introduction_Selection`.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to be queried. It can be in any of the :ref:`supported forms <Introduction_Forms>`.
    selection : str, tuple, list or numpy.ndarray, default='all'
        Selection query defining the elements to be selected. It can be:
        - A string with a selection expression (e.g. `"group_name in ['ALA', 'GLY']"`)
        - A list/array of 0-based indices
        - A nested list of multiple queries (for grouped selections)
    structure_indices : str, tuple, list or numpy.ndarray, default='all'
        0-based indices of the structures over which the selection is applied.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default='atom'
        Structural level on which the selection is applied. Returned indices correspond to this level.
    mask : str, tuple, list or numpy.ndarray, optional
        Optional subset of elements to restrict the selection. It is applied as an intersection filter.
    syntax : str, default='MolSysMT'
        Syntax used to interpret the `selection` string. See :ref:`Introduction_Selection` for available syntaxes.
    to_syntax : str, optional
        If provided, returns the translated selection query string in the target syntax instead of indices.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Returns
    -------
    list or str
        If `to_syntax` is `None`, returns a list of selected element indices.
        Otherwise, returns a translated selection string in the specified syntax.

    Raises
    ------
    NotSupportedFormError
        Raised if the molecular system is provided in an unsupported form.
    ArgumentError
        Raised if one or more input arguments are invalid.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection syntaxes and valid query expressions are described in :ref:`Introduction_Selection`.
    - The selection is always returned as indices corresponding to the specified element level,
    unless a translation to another syntax is explicitly requested via `to_syntax`.
    - When using the MolSysMT syntax, numeric comparisons on `*_id` fields (for example,
      ``atom_id<10``) are allowed as a convenience: if the underlying IDs are integer-like strings,
      they are temporarily converted to integers inside this function; otherwise a warning is issued
      and the comparison uses string semantics.

    See Also
    --------
    :func:`molsysmt.basic.get`
        Retrieving attributes of selected elements.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys = systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.basic.select(molsys, element='group', selection='group_name in ["HIS", "THR"]')
    [20, 25, 30, 33, 53, 58, 108, 114, 141, 150, 151, 154, 156]

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Select`

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

            raise NotSupportedSyntaxError(syntax=syntax)

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

            raise NotImplementedMethodError(caller='molsysmt.basic.select')

    if is_all(mask):
        mask = None

    if (mask is not None) and (output_indices is not None):
        if isinstance(mask, str):
            mask = select(molecular_system, selection=mask, element=element, syntax=syntax, skip_digestion=True)
        output_indices = np.intersect1d(output_indices, mask, assume_unique=True).tolist()

    if to_syntax is None:

        output = output_indices

    else:

        if to_syntax in _dict_indices_to_selection:
            output = _dict_indices_to_selection[to_syntax](molecular_system, output_indices, element)
        else:
            raise NotSupportedSyntaxError(syntax=to_syntax)

    return output
