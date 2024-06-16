from molsysmt._private.digestion import digest

def is_a_molecular_system(molecular_system):
    """
    Verifying the validity of a molecular system.

    An item, or a list of items, can be checked to verify the validity as molecular system.


    Parameters
    ----------

    molecular_system : molecular systems
        A tentative molecular system composed by an item or a list of items in any of :ref:`the
        supported forms <Introduction_Forms>`.


    Returns
    -------

    bool
        The function returns True in case the input molecular system is indeed a
        molecular system. The returned value is False otherwise.


    .. versionadded:: 0.1.0


    Notes
    -----

    The list of supported molecular systems' forms is detailed in the documentation section
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`.


    See Also
    --------

    :func:`molsysmt.basic.are_multiple_molecular_systems`
        Verifying the validity of a list of molecular systems.


    Examples
    --------

    The following example illustrates the use of the function.

    >>> import molsysmt as msm
    >>> topology = msm.systems.demo['pentalanine']['pentalanine.prmtop']
    >>> structures_A = msm.systems.demo['pentalanine']['pentalanine.inpcrd']
    >>> structures_B = msm.systems.demo['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    >>> msm.basic.is_a_molecular_system([topology, structures_A])
    True
    >>> msm.basic.is_a_molecular_system([topology, structures_B])
    False


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Basic > Is a molecular system <Tutorial_Is_a_molecular_system>`.

    """


    from . import get_form
    from ..form import _dict_modules

    if not isinstance(molecular_system, (list, tuple)):

        try:
            _ = get_form(molecular_system)
            return True
        except:
            return False

    else:

        output = True

        list_n_atoms = []

        for item in molecular_system:

            form_in = get_form(item)
            list_n_atoms.append(_dict_modules[form_in].get_n_atoms_from_system(item))

        set_n_atoms = set([ii for ii in list_n_atoms if ii is not None])

        if len(set_n_atoms)>1:
            output = False


        return output

