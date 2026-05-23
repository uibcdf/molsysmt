from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal

@signal(tags=['api', 'get'])
@arg_digest()
def where_is_attribute(molecular_system, attribute, include_none=False, skip_digestion=False):
    """
    Locating the item where a specific attribute is found.

    A molecular system can be composed of multiple items in different forms. This function
    returns the item and its form where the given attribute is available. If `include_none`
    is `False`, items that have the attribute but with value `None` will be ignored.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to be analyzed. It can be in any of the :ref:`supported forms <Introduction_Forms>`.
    attribute : str
        Name of the attribute to search for within the molecular system.
    include_none : bool, default=False
        Whether to ignore items that have the attribute defined but its value is `None`. With default value `False`,
        such items will be ignored.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT’s internal argument digestion mechanism.

        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.

        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.


    Returns
    -------
    item
        The item in which the attribute was found.
    str
        The form of the item where the attribute was found.


    Notes
    -----
    - Supported molecular-system forms are described in :ref:`Introduction_Forms`.
    - If multiple items contain the same attribute, the last matching one is returned.
    - If no item contains the attribute both outputs will be `None`.


    See Also
    --------
    :func:`molsysmt.basic.has_attribute`
        Checking whether a molecular system contains a given attribute.
    :func:`molsysmt.basic.get_attributes`
        Retrieving the list of attributes present in a molecular system.


    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> structure = systems['pentalanine']['pentalanine.inpcrd']
    >>> topology = systems['pentalanine']['pentalanine.prmtop']
    >>> molecular_system = [topology, structure]
    >>> item, form = msm.basic.where_is_attribute(molecular_system, 'box')
    >>> form
    'file:inpcrd'
    >>> item, form = msm.basic.where_is_attribute(molecular_system, 'atom_id')
    >>> form
    'file:prmtop'


    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Where_is_attribute`


    .. versionadded:: 1.0.0
    """


    from . import get_form
    from molsysmt.form import _dict_modules

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    where_form=[]
    where_item=[]

    for form_in, item in zip(forms_in, molecular_system):
        if _dict_modules[form_in].has_attribute(item, attribute, include_none=include_none,
                                                skip_digestion=True):
            where_form.append(form_in)
            where_item.append(item)

    if len(where_form)>=1:
        output_item = where_item[-1]
        output_form = where_form[-1]
    elif not include_none:
        # Fallback to include_none=True to find where the attribute can be defined
        for form_in, item in zip(forms_in, molecular_system):
            if _dict_modules[form_in].has_attribute(item, attribute, include_none=True,
                                                     skip_digestion=True):
                where_form.append(form_in)
                where_item.append(item)
        if len(where_form)>=1:
            output_item = where_item[-1]
            output_form = where_form[-1]
        else:
            output_item = None
            output_form = None
    else:
        output_item = None
        output_form = None

    return output_item, output_form
