# Digestion can not be done in this method since it is redundant.

def are_multiple_molecular_systems(molecular_systems):
    """
    Checking whether a container holds only valid molecular systems.

    This function verifies that every element in the given container is a valid
    molecular system in one of the supported forms recognized by MolSysMT.

    Parameters
    ----------
    molecular_systems : list or tuple of molecular systems
        Container to check. Each item must be in one of the
        :ref:`supported forms <Introduction_Forms>`.

    Returns
    -------
    bool
        `True` if (i) the input is a list or tuple, (ii) it is not empty, and
        (iii) all items are valid molecular systems. `False` otherwise.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - See :func:`molsysmt.basic.is_a_molecular_system` to validate single objects.

    See Also
    --------
    :func:`molsysmt.basic.is_a_molecular_system`
        Check whether a single object is a valid molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> A = '2LAO'  # PDB id (supported form)
    >>> B = 'AVLYAWPA'  # one-letter peptide sequence (supported form)
    >>> C = systems['Trp-Cage']['1l2y.h5msm']  # demo system (supported form)
    >>> msm.are_multiple_molecular_systems([A, B, C])
    True
    >>> msm.are_multiple_molecular_systems([])  # empty container -> False
    False
    >>> msm.are_multiple_molecular_systems(A)  # not a list/tuple
    False

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Are_multiple_molecular_systems`.

    .. versionadded:: 1.0.0
    """

    from . import is_a_molecular_system

    if not isinstance(molecular_systems, (list, tuple)):
        return False

    if len(molecular_systems) == 0:
        return False

    return all(is_a_molecular_system(item) for item in molecular_systems)

