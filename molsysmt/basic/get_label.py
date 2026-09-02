from molsysmt._private.argdigest import arg_digest
import numpy as np
from smonitor import signal

@signal(tags=['api', 'get'])
@arg_digest()
def get_label(molecular_system,
              element='atom',
              selection='all',
              string='{name}-{id}@{index}',
              syntax='MolSysMT',
              skip_digestion=False,
              **kwargs):
    """
    Generating label strings for selected elements of a molecular system.

    This function builds one or more human-readable labels for elements of a molecular system,
    based on the requested `element` level and an f-string-like `string` pattern. Generic
    placeholders (`{name}`, `{id}`, `{index}`) are automatically mapped to the appropriate
    attribute names for the chosen `element` (e.g., `atom_name`, `group_id`). Explicit
    attribute names (e.g., `molecule_name`) are also allowed regardless of `element`.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    element : str, default='atom'
        Structural element level to query ('atom', 'group', 'component', 'molecule', 'chain', 'entity').
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    string : str, default='{name}-{id}@{index}'
        Format template built from element attributes such as name, ID, and index.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or list of str
        A single label string if only one element is selected; otherwise, a list of label strings
        in the order of the selection.


    Raises
    ------
    NotSupportedFormError
        If the input molecular system has an unsupported form.
    ArgumentError
        If input arguments are invalid or inconsistent.


    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.


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
    ['GLU11/T4 LYSOZYME', 'LEU13/T4 LYSOZYME', 'LEU15/T4 LYSOZYME']


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Get_label`.

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
                       output_type='dictionary', skip_digestion=True, **get_attributes)

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
