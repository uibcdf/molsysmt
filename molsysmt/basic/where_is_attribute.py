# If digest is used in this method, other methods become slower

def where_is_attribute(molecular_system, attribute, check_if_None=True):
    """
    Getting the item where a specific attribute is found.

    A molecular system can be formed by a list of items. The function returns
    the item and the form of the item where a specific attribute is found.


    Parameters
    ----------

    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.

    attribute: str
        The attribute name to be checked in the molecular system.

    check_if_None: bool, default True
        If an item has an attribute but its value is None, the situation is
        equal as if the attribute is not in the item.


    Returns
    -------

    item
        The function returns the item where the attribute was found.
    form
        The function returns also the form of the item where the attribute was found.


    .. versionadded:: 0.1.0

    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    See Also
    --------

    :func:`molsysmt.basic.get_attributes`
        Getting the list of attributes of a molecular system.

    :func:`molsysmt.basic.has_attribute`
        Checking if a molecular system has a certain attribute.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> structure = msm.systems.demo['pentalanine']['pentalanine.inpcrd']
    >>> topology = msm.systems.demo['pentalanine']['pentalanine.prmtop']
    >>> molecular_system = [topology, structure]
    >>> msm.basic.where_is_attribute(molecular_system, 'box')
    (PosixPath('/home/diego/projects@uibcdf/MolSysMT/molsysmt/data/inpcrd/pentalanine.inpcrd'),
     'file:inpcrd')


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Where is attribute <Tutorial_Where_is_attribute>`.


    """


    from . import get_form
    from molsysmt.form import _dict_modules

    if not isinstance(molecular_system, (list, tuple)):
        molecular_system = [molecular_system]

    forms_in = get_form(molecular_system)

    where_form=[]
    where_item=[]

    if check_if_None:
        for form_in, item in zip(forms_in, molecular_system):
            if _dict_modules[form_in].has_attribute(item, attribute):
                where_form.append(form_in)
                where_item.append(item)
    else:
        for form_in, item in zip(forms_in, molecular_system):
            if _dict_modules[form_in].attributes[attribute]:
                where_form.append(form_in)
                where_item.append(item)

    if len(where_form)>=1:
        output_item = where_item[-1]
        output_form = where_form[-1]
    elif len(where_form)==0:
        output_item = None
        output_form = None
    else:
        print('This to correct in where_is_attribute')

    return output_item, output_form

