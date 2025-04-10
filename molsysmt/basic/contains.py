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
    Check whether a molecular system contains specific elements or satisfies certain conditions.

    This function returns a boolean value indicating whether the molecular system, or a subset
    defined by the given selection, contains specific elements or attributes as specified
    via keyword arguments.

    Parameters
    ----------
    molecular_system : molecular system
        The molecular system to be analyzed, in any of the :ref:`supported forms <Introduction_Forms>`.

    selection : str, tuple, list, or numpy.ndarray, default 'all'
        Subset of atoms to which the condition should be applied. Can be specified as:
        - A string using a supported selection syntax.
        - A tuple, list, or array of atom indices (0-based).
        The default 'all' applies the condition to the entire system.

    syntax : str, default 'MolSysMT'
        Syntax used to parse the selection string, if `selection` is given as a string.
        See :ref:`Introduction_Selection` for supported options.

    **kwargs : dict
        Keyword arguments specifying the conditions to be checked. Keys must be attribute names,
        and values can be:
        - `True`: the attribute must be present or non-zero.
        - `False`: the attribute must be absent or zero.
        - An integer: the attribute must equal the specified value.

    Returns
    -------
    bool
        `True` if all specified conditions are satisfied by the selected subset of the system;
        otherwise, `False`.

    Raises
    ------
    NotSupportedFormError
        If the molecular system is not in a supported form.

    ArgumentError
        If input arguments are invalid or inconsistent.

    Notes
    -----
    See :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>` for a list of valid molecular system forms.

    See :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>` for details on supported selection strings.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.

    :func:`molsysmt.basic.is_composed_of`
        Check if a molecular system is composed of specific types of elements.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems.demo['T4 lysozyme L99A']['181l.mmtf']
    >>> msm.contains(molsys, waters=True, ions=True)
    True
    >>> msm.contains(molsys, selection='atom_name=="Cl"')
    True
    >>> msm.contains(molsys, selection='molecule_type!="water"', waters=True)
    False

    .. admonition:: User guide

       Follow this link for a tutorial on how to use this function:
       :ref:`User Guide > Tools > Basic > Contains <Tutorial_Contains>`

    .. versionadded:: 1.0.0
    ```

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

