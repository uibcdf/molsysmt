from molsysmt._private.digestion import digest

@digest()
def concatenate_structures(molecular_systems, selections='all', structure_indices='all', to_form=None,
                           syntax='MolSysMT', skip_digestion=False):
    """
    Concatenate structures from a list of molecular systems into a single molecular system.

    This function collects structures (frames) from several molecular systems and returns a new
    molecular system whose structural dimension is the concatenation of the selected structures.
    All participating systems must be aligned in atom count and ordering over the chosen selections;
    use `selections` to provide per-system matching subsets when needed. Optionally, select specific
    structures from each input with `structure_indices`.

    Parameters
    ----------
    molecular_systems : list of molecular systems
        List of input molecular systems in any of the :ref:`supported forms <Introduction_Forms>`.
        Structures will be taken from these systems.
    selections : list of (str, tuple, list, numpy.ndarray) or 'all', default 'all'
        Atom selections to extract structures from each molecular system. Provide a single value (applied to all
        systems) or a list of selections with the same length as `molecular_systems`. Each entry can be a 0-based index collection or a
        selection string parsed according to :ref:`Introduction_Selection`.
    structure_indices : list of (int, tuple, list, numpy.ndarray) or 'all', default 'all'
        Structure indices (0-based) per system to include. Provide a single value (applied to all
        systems) or a list matching `molecular_systems` in length.
    to_form : str or None, default None
        Output form for the resulting molecular system. If `None`, the form is inherited from the
        first input system.
    syntax : str, default 'MolSysMT'
        Selection syntax used when entries of `selections` are strings. See :ref:`Introduction_Selection`.
    skip_digestion : bool, default False
        Whether to skip MolSysMT’s internal argument digestion mechanism.
        MolSysMT includes a built-in digestion system that validates and normalizes
        function arguments. This process checks types, shapes, and values, and automatically
        adjusts them when possible to meet expected formats.
        Setting `skip_digestion=True` disables this process, which may improve performance
        in workflows where inputs are already validated. Use with caution: only set this to
        `True` if you are certain all input arguments are correct and consistent.

    Returns
    -------
    molecular system
        New molecular system containing the concatenated structures. The topology is inherited
        from the first item in `molecular_systems`. The output form is controlled by `to_form`
        (or inherited if `None`).

    Raises
    ------
    NotSupportedFormError
        If any input system is provided in an unsupported form.
    ArgumentError
        If input values are invalid or inconsistent.

    Notes
    -----
    - Supported molecular-system forms are summarized in :ref:`Introduction_Forms`.
    - Selection strings must follow one of the syntaxes described in
      :ref:`Introduction_Selection`.
    - All systems must be consistent in **number and ordering of atoms** over the final selections.
      Use `selections` to align subsets when needed.
    - Structural attributes concatenated include `coordinates`, `velocities`, `box`, `time`
      (when available in the inputs).

    See Also
    --------
    :func:`molsysmt.basic.select` :
        Select elements from a molecular system.
    :func:`molsysmt.basic.append_structures` :
        Append structures from one molecular system to another.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import systems
    >>> A = msm.convert(systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> B = msm.structure.translate(A, translation='[0.1, 0.1, 0.1] nanometers')
    >>> C = msm.concatenate_structures([A, B])
    >>> msm.get(C, n_structures=True)
    2

    .. admonition:: Tutorial with more examples

       See the following tutorial for a practical demonstration of how to use this function,
       along with additional examples:
       :ref:`Tutorial_Concatenate_structures`.

    .. versionadded:: 1.0.0
    """

    from . import convert, extract, get, get_form
    from molsysmt.form import _dict_modules

    n_molecular_systems = len(molecular_systems)

    if not isinstance(selections, (list, tuple)):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections)!=n_molecular_systems:
        raise ValueError("The length of the lists items and selections need to be equal.")

    if not isinstance(structure_indices, (list, tuple)):
        structure_indices = [structure_indices for ii in range(n_molecular_systems)]
    elif len(structure_indices)!=n_molecular_systems:
        raise ValueError("The length of the lists items and structure_indices need to be equal.")

    if to_form is None:
        to_molecular_system = extract(molecular_systems[0], selection=selections[0],
                                      structure_indices=structure_indices[0])
        to_form = get_form(to_molecular_system)
    else:
        to_molecular_system = convert(molecular_systems[0], to_form=to_form, selection=selections[0],
                                      structure_indices=structure_indices[0])

    for aux_molecular_system, aux_selection, aux_structure_indices in zip(molecular_systems[1:], selections[1:], structure_indices[1:]):

        coordinates, velocities = get(aux_molecular_system, element='atom', selection=aux_selection,
                          structure_indices=aux_structure_indices, coordinates=True, velocities=True)
        structure_id, time, box = get(aux_molecular_system, structure_indices=aux_structure_indices, structure_id=True, time=True,
                              box=True)

        _dict_modules[to_form].append_structures(to_molecular_system, structure_id=structure_id, time=time, coordinates=coordinates,
                velocities=velocities, box=box)

    output = to_molecular_system

    return output

