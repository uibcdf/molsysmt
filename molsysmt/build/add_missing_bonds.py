from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def add_missing_bonds(molecular_system, max_bond_length='2 angstroms', selection='all',
                      structure_index=0, syntax='MolSysMT', engine='MolSysMT',
                      in_place=True, skip_digestion=False):
    """
    Adding missing covalent bonds based on atomic distances and types.

    This function analyzes the atomic coordinates and element types in a molecular system
    to infer and add covalent bonds between atoms that are close enough based on standard
    bonding distances. The new bonds are added to the `bonded_atoms` attribute. No bond types
    or orders are assigned. The procedure can be applied in-place or return a modified copy.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>` to which new
        covalent bonds will be added.

    max_bond_length : str or float with unit, default '2 angstroms'
        Maximum distance between two atoms for a bond to be considered. Atoms further than this
        value will not be bonded. If a string is passed, it must include units (e.g., '0.19 nm').

    selection : tuple, list, numpy.ndarray or str, default 'all'
        Selection of atoms to which the method applies. The selection can be given by a list, tuple
        or numpy array of atom indices (0-based integers), or by a query string following any of
        :ref:`the selection syntaxes parsable by MolSysMT <Introduction_Selection>`.

    structure_index : int, default 0
        Structure index (0-based) to use when the molecular system contains multiple structures.
        The bond detection is based on the atomic positions at this structure.

    syntax : str, default 'MolSysMT'
        :ref:`Supported syntax <Introduction_Selection>` used in the `selection` argument (in case it is a string).

    engine : {'MolSysMT'}, default 'MolSysMT'
        Engine used to infer bonds. Currently only the native 'MolSysMT' engine is supported.

    in_place : bool, default True
        If `True`, the input molecular system is modified directly. If `False`, a new system with
        the added bonds is returned.

    skip_digestion : bool, default False
        If `True`, skips initial validation of input arguments. Used internally.

    Returns
    -------
    molecular system or None
        If `in_place=True`, the function returns `None` and modifies the input molecular system.
        If `in_place=False`, a new molecular system is returned with inferred bonds added.

    Raises
    ------
    NotSupportedFormError
        Raised if the input molecular system is in a form that cannot be edited.

    ArgumentError
        Raised if any of the input arguments are invalid or inconsistent.

    Notes
    -----
    This method updates only the `bonded_atoms` attribute of the system. No bond types or orders
    are assigned.

    This function is useful when working with coordinate files that lack bond information
    (e.g., `.xyz`, `.pdb`, or trajectory frames).

    The list of supported molecular systems' forms is detailed in the documentation section:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    The list of supported selection syntaxes can be found here:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`

    See Also
    --------
    :meth:`molsysmt.Topology.add_bonds`
        Manually add specific bonds to a native topology.

    :meth:`molsysmt.Topology.remove_bonds`
        Remove covalent bonds from a native topology.

    :func:`molsysmt.basic.get()`
        Access attributes like `bonded_atoms`.

    :func:`molsysmt.basic.convert()`
        Convert the system into a supported editable form.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm']
    >>> system = msm.convert(molsys)
    >>> system.topology.remove_bonds('all')
    >>> msm.build.add_missing_bonds(system)
    >>> msm.get(system, bonded_atoms=True)[:3]
    array([[0, 1],
           [1, 2],
           [2, 3]])

    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Build > Add missing bonds <Tutorial_Add_missing_bonds>`.

    .. versionadded:: 1.0.0
    """

    if engine=='MolSysMT':

        from molsysmt.basic import where_is_attribute
        from molsysmt.build import get_missing_bonds
        from molsysmt.form import _dict_modules

        bonds = get_missing_bonds(molecular_system, max_bond_length=max_bond_length, selection=selection,
                                 structure_index=structure_index, syntax=syntax,
                                 skip_digestion=True)
        if in_place:
            item, form = where_is_attribute(
                molecular_system, 'bonded_atom_pairs', include_none=False, skip_digestion=True
            )
            add_bonds_function = getattr(_dict_modules[form], 'add_bonds')
            add_bonds_function(item, bonds, skip_digestion=True)
            return None

        tmp_item = molecular_system.copy()
        item, form = where_is_attribute(tmp_item, 'bonded_atom_pairs', include_none=False, skip_digestion=True)
        add_bonds_function = getattr(_dict_modules[form], 'add_bonds')
        add_bonds_function(item, bonds, skip_digestion=True)
        return tmp_item

    else:

        raise NotImplementedError
