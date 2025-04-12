from molsysmt._private.digestion import digest

def is_a_molecular_system(molecular_system):
    """
    Verify whether the input is a single valid molecular system.

    This function checks if the input — either a single item or a list of items — constitutes
    a single valid molecular system. Validity requires compatible forms and internal consistency
    (e.g., matching number of atoms across items). It does not check if multiple independent
    systems are valid — for that, use :func:`molsysmt.basic.are_multiple_molecular_systems`.

    Parameters
    ----------
    molecular_system : molecular system
        A tentative molecular system composed of one item or a list of items,
        in any of the :ref:`supported forms <Introduction_Forms>`.

    Returns
    -------
    bool
        `True` if the input is a valid molecular system, `False` otherwise.

    Notes
    -----
    This function returns `True` only if the input represents a **single** molecular system.
    For validating multiple molecular systems individually, use:
    :func:`molsysmt.basic.are_multiple_molecular_systems`.

    See also the list of supported forms:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    See Also
    --------
    :func:`molsysmt.basic.are_multiple_molecular_systems`
        Check whether a list of objects are each valid molecular systems.

    Examples
    --------
    >>> import molsysmt as msm
    >>> topology = msm.systems.demo['pentalanine']['pentalanine.prmtop']
    >>> structures_A = msm.systems.demo['pentalanine']['pentalanine.inpcrd']
    >>> structures_B = msm.systems.demo['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    >>> msm.basic.is_a_molecular_system([topology, structures_A])
    True
    >>> msm.basic.is_a_molecular_system([topology, structures_B])
    False

    .. admonition:: User guide

       For a tutorial on how to use this function, see:
       :ref:`User Guide > Tools > Basic > Is a molecular system <Tutorial_Is_a_molecular_system>`

    .. versionadded:: 1.0.0
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

