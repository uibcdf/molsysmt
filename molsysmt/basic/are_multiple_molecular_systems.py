from molsysmt._private.digestion import digest
import numpy as np

def are_multiple_molecular_systems(molecular_systems):
    """
    Check whether a list contains only valid molecular systems.

    This function verifies that all elements in the input list are molecular systems,
    each in one of the supported forms recognized by MolSysMT.

    Parameters
    ----------
    molecular_systems : list of molecular systems
        List of objects to check. Each item must be in one of 
        :ref:`the supported forms <Introduction_Forms>`.

    Returns
    -------
    bool
        True if all objects in the list are valid molecular systems.
        False if any object is not recognized as a molecular system.

    Notes
    -----
    The list of supported molecular system forms is detailed in
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.

    See Also
    --------
    :func:`molsysmt.basic.is_a_molecular_system`
        Check whether a single object is a valid molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> molsys_A = '2LAO'
    >>> molsys_B = 'AVLYAWPA'
    >>> molsys_C = systems['Trp-Cage']['1l2y.mmtf']
    >>> msm.basic.are_multiple_molecular_systems([molsys_A, molsys_B, molsys_C])
    True

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Are multiple molecular systems <Tutorial_Are_multiple_molecular_systems>`.

    .. versionadded:: 1.0.0
    """

    from . import is_a_molecular_system

    output = False

    aux_list = []
    if isinstance(molecular_systems, (list, tuple)):

        for molecular_system in molecular_systems:
            aux_list.append(is_a_molecular_system(molecular_system))

        output = np.all(aux_list)

    return output

