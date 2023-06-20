from molsysmt._private.digestion import digest
import numpy as np

def _evaluation(condition, value):

    output = True

    if condition is not None:
        if isinstance(condition, bool):
            if condition==True:
                if value is None:
                    output = False
                elif isinstance(value, (int, np.int64)):
                    if value==0:
                        output = False
            else:
                if isinstance(value, (int, np.int64)):
                    if value>0:
                        output = False
                elif isinstance(value, (np.ndarray, list, tuple)):
                        output = False
        elif isinstance(condition, int):
            if isinstance(value, int):
                if condition>value:
                    output = False

    return output

@digest()
def contains(molecular_system, selection='all', syntax='MolSysMT', **kwargs):
    """
    Checking if a molecular system contains certain elements or attributes.

    The function returns True or False depending on whether or not the system has the elements or
    attributes required.


    Parameters
    ----------

    molecular_system : molecular system
        The molecular system in any of :ref:`the supported forms
        <Introduction_Forms>` to be analysed by the function.

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of elements of the molecular system to be checked by the function. The selection can be
        given by a list, tuple or numpy array of atom indices (0-based
        integers); or by means of a string following any of :ref:`the selection
        syntaxes parsable by MolSysMT <Introduction_Selection>`.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case
        it is a string).

    **kwargs : {{keyword : str,  value : (bool, int)}, default None}
        The attributes or elements to be checked in the molecular system are introduced as
        additional keywords with value either 'True', 'False', or by means of an integer to
        indicate to amount of specific elements the system contains.


    Returns
    -------

    bool
        A boolean value is returned reporting if the molecular system contains the elements and/or
        attributes required.


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
        Selecting elements of a molecular system.

    :func:`molsysmt.basic.is_composed_of`
        Checking if a molecular system is composed of specific elements.

    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> molecular_system = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.basic.contains(molecular_system, waters=True, ions=True)
    True
    >>> msm.basic.contains(molecular_system, selection='atom_name=="Cl"')
    True
    >>> msm.basic.contains(molecular_system, selection='molecule_type!="water"', waters=True)
    False


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Contains <Tutorial_Contains>`.


    """

    from . import get

    atts_required = {}
    aux_atts = {}
    for key in kwargs.keys():
        atts_required[key] = kwargs[key]
        aux_atts[key] = True

    n_atts_required = len(atts_required)

    if n_atts_required:

        atts_values = get(molecular_system, selection=selection, syntax=syntax, **aux_atts)

        if n_atts_required==1:
            atts_values = [atts_values]

        for att, att_value in zip(aux_atts.keys(), atts_values):
            if not _evaluation(atts_required[att], att_value):
                return False

    else:

        n_atoms = get(molecular_system, element='atom', selection=selection, syntax=syntax, n_atoms=True)

        if not n_atoms:
            return False

    return True

