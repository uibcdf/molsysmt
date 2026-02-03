from molsysmt._private.digestion import arg_digest
import numpy as np

def _evaluation(condition, value):
    """Internal helper for `contains` to evaluate a single condition/result pair.

    Supports boolean conditions (presence/absence/emptiness) and integer thresholds,
    returning `True` if the provided `value` satisfies the requested `condition`.
    """
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

@arg_digest()
def contains(molecular_system, selection='all', syntax='MolSysMT', skip_digestion=False, **kwargs):
    """
    Checking whether a molecular system contains specific elements or satisfies conditions.

    This function returns a boolean indicating whether the molecular system, or a selected subset
    of it, satisfies a set of conditions expressed via keyword arguments. Each keyword corresponds
    to an attribute to check, and its value specifies the condition to apply.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system to analyze, in any of the :ref:`supported forms <Introduction_Forms>`.
    selection : str, tuple, list or numpy.ndarray, default 'all'
        Subset of atoms the conditions are applied to. Either a 0-based index collection or a
        selection string parsed according to :ref:`Introduction_Selection`. The default 'all'
        applies the conditions to the entire system.
    syntax : str, default 'MolSysMT'
        Selection syntax used when `selection` is a string. See :ref:`Introduction_Selection`.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.
        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.
        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.
    **kwargs
        Attribute conditions expressed as ``attribute=value`` pairs, where the value can be:
        - `True`: the attribute must be present and **non-zero/non-empty** on the selected subset.
        - `False`: the attribute must be **absent or zero/empty** on the selected subset.
        - `int`: the attribute (interpreted as a count/size) must be **greater than or equal to**
          the given integer (threshold).

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
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.

    See Also
    --------
    :func:`molsysmt.basic.select`
        Select elements from a molecular system.
    :func:`molsysmt.basic.is_composed_of`
        Check if a molecular system is composed of specific types of elements.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['T4 lysozyme L99A']['181l.h5msm']
    >>> msm.contains(molsys, waters=True, ions=True)
    True
    >>> msm.contains(molsys, selection='atom_name=="CL"')
    True
    >>> msm.contains(molsys, selection='molecule_type!="water"', waters=True)
    False

    .. admonition:: User guide

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Contains`.

    .. versionadded:: 1.0.0
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
