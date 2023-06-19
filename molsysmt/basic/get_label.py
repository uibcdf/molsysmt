from molsysmt._private.digestion import digest
import numpy as np

@digest()
def get_label(molecular_system,
              element='atom',
              selection='all',
              string='{name}-{id}@{index}',
              syntax='MolSysMT',
         ):
    """
    Getting label strings for elements

    This function returns label strings of a selection of elements of a molecular system.
    The format and attributes of the label strings can be defined by the user by means of the input
    argument ``string``.

    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by this function.

    element: {'atom', 'group', 'component', 'molecule', 'chain', 'entity', 'system'}, default 'atom'
        The label strings are produced for the elements of the system specified by this argument.

    selection : index, tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to get the label strings. The
        selection can be given by a list, tuple or numpy array of element indices (0-based
        integers) -up to the value of the ``element`` input argument-; or by means of a query
        string following any of :ref:`the selection syntaxes parsable by MolSysMT
        <Introduction_Selection>`.

    string: str, default '{name}-{id}@{index}'
        String with format and attributes to be produced for the selected elements. The value needs
        to be a string written as a f-string (without the f). The attribute names "name", "id"
        or "index" can be used instead of "element_name", "element_id" or "element_index". For
        example, "name" will be automatically replaced by "atom_name" in case the input argument
        ``element`` takes the value "atom".

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).


    Returns
    -------
    str, list of str
        The function returns the label string or label strings for the selected elements of the
        system.

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


    .. versionadded:: 0.5.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    The list of supported selection syntaxes can be checked in the documentation section
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`.


    See Also
    --------

    :func:`molsysmt.basic.select`
        Selecting elements of a molecular system


    Examples
    --------

    The following example illustrates the use of the function.


    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system = msm.basic.convert(demo['T4 lysozyme L99A']['181l.mmtf'])
    ['GLU11/T4 lysozyme', 'LEU13/T4 lysozyme', 'LEU15/T4 lysozyme']


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Get label <Tutorial_Get_label>`.

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

    if len(output)>1:
        return output
    else:
        return output[0]

