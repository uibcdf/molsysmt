from molsysmt._private.argdigest import arg_digest


@arg_digest()
def add_missing_bonds(
    molecular_system,
    max_bond_length="2 angstroms",
    selection="all",
    structure_index=0,
    syntax="MolSysMT",
    engine="MolSysMT",
    in_place=True,
    skip_digestion=False,
):
    """
    Adding missing covalent bonds based on atomic distances and types.

    This function adds candidates returned by ``get_missing_bonds`` from group
    templates and distance criteria. Peptide candidates require consecutive source
    group indices with one identical, defined chain index. Selecting separated
    groups does not make them adjacent. No bond types or orders are assigned.
    The procedure can be applied in-place or return a modified copy; its heuristics
    do not certify a complete or chemically validated molecular graph.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    max_bond_length : quantity or str, default='2 angstroms'
        Distance cutoff for geometric candidates, with explicit length units.
        Defaults to '2 angstroms'.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atom selection. Integer lists refer to source atom indices. Both endpoints
        of each added pair must belong to the selection. Defaults to 'all'.
    structure_index : int, default=0
        Source structure index used for distance-based candidates. Defaults to 0.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    engine : str, default='MolSysMT'
        Reconstruction engine. Defaults to 'MolSysMT'.
    in_place : bool, default=True
        Whether to modify the source or return a modified copy. Defaults to True.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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
    (e.g., `.xyz`, `.pdb`, or trajectory structures).

    The list of supported molecular systems' forms is detailed in the documentation section:
    :ref:`User Guide > Introduction > Molecular systems > Forms <Introduction_Forms>`

    The list of supported selection syntaxes can be found here:
    :ref:`User Guide > Introduction > Selection syntaxes <Introduction_Selection>`


    See Also
    --------
    :func:`molsysmt.build.get_missing_bonds`
        Inspect candidates and their selection and chain constraints before adding them.

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
    >>> msm.get(system, bonded_atom_pairs=True)[:3]
    [[0, 1], [1, 2], [1, 3]]


    .. admonition:: User guide

       Follow this link for a tutorial on how to work with this function:
       :ref:`User Guide > Tools > Build > Add missing bonds <Tutorial_Add_missing_bonds>`.

    .. versionadded:: 1.0.0
    """

    if engine == "MolSysMT":
        from molsysmt.basic import where_is_attribute
        from molsysmt.build import get_missing_bonds
        from molsysmt.form import _dict_modules

        bonds = get_missing_bonds(
            molecular_system,
            max_bond_length=max_bond_length,
            selection=selection,
            structure_index=structure_index,
            syntax=syntax,
            skip_digestion=True,
        )
        if in_place:
            item, form = where_is_attribute(
                molecular_system,
                "bonded_atom_pairs",
                include_none=False,
                skip_digestion=True,
            )
            add_bonds_function = getattr(_dict_modules[form], "add_bonds")
            add_bonds_function(item, bonds, skip_digestion=True)
            return None

        tmp_item = molecular_system.copy()
        item, form = where_is_attribute(
            tmp_item, "bonded_atom_pairs", include_none=False, skip_digestion=True
        )
        add_bonds_function = getattr(_dict_modules[form], "add_bonds")
        add_bonds_function(item, bonds, skip_digestion=True)
        return tmp_item

    else:
        raise NotImplementedError
