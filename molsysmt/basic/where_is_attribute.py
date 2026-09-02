from molsysmt._private.argdigest import arg_digest
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
        Molecular system in any supported MolSysMT format.
    attribute : str
        Name of the molecular-system attribute to locate or inspect.
    include_none : bool, default=False
        Whether to include attributes whose value is `None`.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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
    - A **structural** attribute is only looked for in items spanning the structure axis of
      the molecular system, which is the largest number of structures any of its items
      carries. An item holding a single reference conformation therefore does not supply a
      structural series for a trajectory held by another item, and the rule above applies
      only among the items that do span the axis. This makes the result independent of the
      order the items were listed in. When the attribute exists solely off the axis, both
      outputs are `None` and a `StructuralAttributeOffAxisWarning` is emitted.
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

    # A structural attribute may only come from an item spanning the structure axis of
    # the system. Without this, the tie-break below would choose between items that are
    # not interchangeable -- a single reference conformation and a whole trajectory --
    # and the answer would depend on the order the items were listed in.
    spans_axis = [True]*len(forms_in)
    if len(forms_in)>1:
        from molsysmt.attribute import is_structural_attribute

        if is_structural_attribute(attribute):
            from molsysmt._private.structure_axis import structure_axis

            axis, counts = structure_axis(molecular_system, forms_in,
                                          caller='molsysmt.where_is_attribute')
            if axis is not None:
                spans_axis = [count==axis for count in counts]

    where_form=[]
    where_item=[]
    dropped_forms=[]

    for spans, form_in, item in zip(spans_axis, forms_in, molecular_system):
        if _dict_modules[form_in].has_attribute(item, attribute, include_none=include_none,
                                                skip_digestion=True):
            if spans:
                where_form.append(form_in)
                where_item.append(item)
            else:
                dropped_forms.append(form_in)

    if len(where_form)>=1:
        output_item = where_item[-1]
        output_form = where_form[-1]
    elif not include_none:
        # Fallback to include_none=True to find where the attribute can be defined
        for spans, form_in, item in zip(spans_axis, forms_in, molecular_system):
            if not spans:
                continue
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

    if output_item is None and dropped_forms:
        # The system does carry the attribute, but only on an item that does not span the
        # structure axis -- a reference conformation beside a trajectory. Saying so is the
        # difference between an attribute that is absent and one that was truncated.
        import warnings

        from molsysmt._private.smonitor import StructuralAttributeOffAxisWarning, warn

        warn(
            StructuralAttributeOffAxisWarning(attributes=[attribute],
                                              caller='molsysmt.where_is_attribute'),
            stacklevel=2,
        )

    return output_item, output_form
