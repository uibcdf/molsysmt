from molsysmt._private.argdigest import arg_digest
import numpy as np
from smonitor import signal


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

@signal(tags=['api', 'get'])
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
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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
