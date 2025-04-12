from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_label(molecular_system,
              element='atom',
              selection='all',
              string='{name}-{id}@{index}',
              syntax='MolSysMT',
              skip_digestion=False
         ):
    """
    Generate label strings for selected elements of a molecular system.

    This function returns one or more label strings for elements of a molecular system,
    based on the specified element type (e.g., atoms, groups, molecules) and selection.
    Labels are formatted according to a user-defined string pattern using element-specific attributes.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to be analyzed, in any of the :ref:`supported forms <Introduction_Forms>`.

    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'atom'
        Type of element for which the labels will be generated.

    selection : int, tuple, list, numpy.ndarray, or str, default 'all'
        Selection of elements of the specified type. Can be given as:
        - A list, tuple, or array of 0-based indices.
        - A string parsed using a supported selection syntax (see :ref:`Introduction_Selection`).
        The selection is interpreted relative to the chosen `element`.

    string : str, default '{name}-{id}@{index}'
        Pattern string used to construct labels. This must be written as a Python f-string (without the `f` prefix).
        Allowed placeholder keywords include `name`, `id`, and `index`, which are automatically mapped to the 
        appropriate attribute for the selected element (e.g., `atom_name`, `group_id`, etc.). Alternatively, explicit 
        attribute names such as `atom_name`, `group_id`, or `molecule_id` can also be used directly, regardless of the `element` value.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the `selection` string, if applicable. See :ref:`Introduction_Selection`.

    skip_digestion : bool, default False
        If True, skip validation of the input molecular system. For advanced use only.

    Returns
    -------
    str or list of str
        A single label string (if one element is selected), or a list of label strings for all selected elements.

    Raises
    ------
    NotSupportedFormError
        If the input molecular system is in an unsupported form.

    ArgumentError
        If input arguments are invalid or inconsistent.

    Notes
    -----
    - Label formatting is flexible and customizable via the `string` argument.
    - The mapping of generic placeholders (e.g., `name`, `id`) to specific attribute names depends on the value of `element`.

    See :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>` for supported forms.

    See :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>` for supported selection strings.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.

    :func:`molsysmt.basic.get`
        Retrieve values of attributes for selected elements.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['T4 lysozyme L99A']['181l.h5msm'])
    >>> msm.get_label(molsys, element='group', selection=[10, 12, 14],
    ...               string='{group_name}{group_id}/{entity_name}')
    ['GLU11/T4 lysozyme', 'LEU13/T4 lysozyme', 'LEU15/T4 lysozyme']

    .. admonition:: User guide

       For a tutorial on using this function, see:
       :ref:`User Guide > Tools > Basic > Get label <Tutorial_Get_label>`

    .. versionadded:: 1.0.0
    """

    if '{name}' in string:
        string = string.replace('{name}','{'+element+'_name}')
    if '{index}' in string:
        string = string.replace('{index}','{'+element+'_index}')
    if '{id}' in string:
        string = string.replace('{id}','{'+element+'_id}')

    from . import get
    from molsysmt.attribute import attributes as _attributes

    get_attributes = {}
    for attribute in _attributes.keys():
        if attribute in string:
            get_attributes[attribute] = True

    get_dict = get(molecular_system, element=element, selection=selection, syntax=syntax,
                       output_type='dictionary', **get_attributes)

    n_elements = []
    for value in get_dict.values():
        n_elements.append(len(value))


    output = []

    if np.all(np.array(n_elements)==n_elements[0]):

        aux_dict = {key:'' for key in get_dict.keys()}

        for ii in range(n_elements[0]):
            for key in get_dict.keys():
                aux_dict[key]=get_dict[key][ii]
            output.append(string.format(**aux_dict))

    if len(output)==1:
        return output[0]
    else:
        return output

