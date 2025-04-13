from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def add_bonds(molecular_system, bonded_atom_pairs, in_place=True, skip_digestion=False):
    """
    Adding covalent bonds between atom pairs in a molecular system.

    This function adds new covalent bonds between pairs of atoms in a molecular system. The
    new bonds are defined by a list of atom index pairs. The function modifies the input
    molecular system in place unless otherwise specified.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` to which new
        bonds will be added.

    bonded_atom_pairs : list, tuple, or numpy.ndarray of shape (n_bonds, 2)
        List or array of atom index pairs (0-based integers), where each pair defines a bond to
        be added.

    in_place : bool, default True
        Whether to modify the input molecular system in place. If set to `False`, a copy of the
        molecular system is returned with the new bonds added.

    skip_digestion : bool, default False
        If `True`, skips the initial validation and normalization of the input arguments. Mainly
        used internally.

    Returns
    -------
    molecular system or None
        If `in_place=True`, the function modifies the input system and returns `None`.
        If `in_place=False`, a new molecular system is returned with the added bonds.

    Raises
    ------
    NotSupportedFormError
        Raised if the molecular system has a format that does not support topology editing.

    ArgumentError
        Raised if the input atom indices are invalid or improperly formatted.

    Notes
    -----
    - This function only updates the topological attribute `bonded_atoms`.
    - No bond orders or bond types are inferred or assigned.
    - Atom indices must be valid and within the range of the molecular system's atoms.

    See Also
    --------
    :func:`molsysmt.build.remove_bonds`
        Remove specific bonds from a molecular system.

    :func:`molsysmt.build.add_missing_bonds`
        Add bonds based on distance criteria and atomic types.

    Examples
    --------
    >>> import molsysmt as msm
    >>> system = msm.convert('181L')
    >>> new_bonds = [(0, 4), (5, 10)]
    >>> msm.build.add_bonds(system, new_bonds)
    >>> msm.get(system, bonded_atoms=True)[:5]
    array([[0, 1],
           [1, 2],
           [2, 3],
           [3, 4],
           [0, 4]])

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Build > Add bonds <Tutorial_Add_bonds>`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import where_is_attribute
    from molsysmt.form import _dict_modules

    if in_place:

        item, form = where_is_attribute(molecular_system, 'bonded_atom_pairs', check_if_None=False,
                                        skip_digestion=True)

        add_bonds_function = getattr(_dict_modules[form], f'add_bonds')
        add_bonds_function(item, bonded_atom_pairs)

    else:

        raise NotImplementedMethodError

