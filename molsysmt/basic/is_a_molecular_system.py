# Digestion can not be done in this method since it is redundant.

def is_a_molecular_system(molecular_system):
    """
    Verifying whether the input is a single valid molecular system.

    This function checks whether `molecular_system` represents one valid molecular system.
    The input may be a single item (any supported form) or a list/tuple combining compatible
    items (e.g., topology + coordinates files). For sequence inputs, validity requires internal
    consistency such as a matching number of atoms across all items.

    Parameters
    ----------
    molecular_system : molecular system
        Tentative molecular system, provided as a single item or a list/tuple of items in any of
        the :ref:`supported forms <Introduction_Forms>`.


    Returns
    -------
    bool
        `True` if the input encodes a single valid molecular system, `False` otherwise.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.

    See Also
    --------
    :func:`molsysmt.basic.are_multiple_molecular_systems` :
        Check whether each item in a container is a valid molecular system.
    :func:`molsysmt.basic.get_form` :
        Retrieve the form of a molecular system.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> topology = systems['pentalanine']['pentalanine.prmtop']
    >>> structures_A = systems['pentalanine']['pentalanine.inpcrd']
    >>> structures_B = systems['chicken villin HP35']['traj_chicken_villin_HP35_solvated.dcd']
    >>> msm.basic.is_a_molecular_system([topology, structures_A])
    True
    >>> msm.basic.is_a_molecular_system([topology, structures_B])
    False

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Is_a_molecular_system`.

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

