from molsysmt._private.digestion import digest
import numpy as np

def are_multiple_molecular_systems(molecular_systems):
    """
    Verifying the validity of a list of molecular systems.

    A list of objects is checked to verify that all objects are molecular systems.


    Parameters
    ----------

    molecular_systems : list of molecular systems
        A list of molecular system in any of :ref:`the supported forms <Introduction_Forms>`.


    Returns
    -------

    bool
        The function returns True in case all objects in the input list are
        molecular systems. The returned value is False otherwise.


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.    


    See Also
    --------

    :func:`molsysmt.basic.is_a_molecular_system`
        Verifying the validity of a molecular system.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> from molsysmt.systems import demo
    >>> molecular_system_1 = '2LAO'
    >>> molecular_system_2 = 'AVLYAWPA'
    >>> molecular_system_3 = demo['Trp-Cage']['1l2y.mmtf']
    >>> msm.basic.are_multiple_molecular_systems([molecular_system_1, molecular_system_2, molecular_system_3])
    True


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Are multiple molecular systems <Tutorial_Are_multiple_molecular_systems>`.    

    """


    from . import is_a_molecular_system

    output = False

    aux_list = []
    if isinstance(molecular_systems, (list, tuple)):

        for molecular_system in molecular_systems:
            aux_list.append(is_a_molecular_system(molecular_system))

        output = np.all(aux_list)

    return output

