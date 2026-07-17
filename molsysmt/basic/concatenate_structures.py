from molsysmt._private.arg_digestion import arg_digest
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def concatenate_structures(molecular_systems, selections='all', structure_indices='all', to_form=None,
                           syntax='MolSysMT', skip_digestion=False):
    """
    Concatenate structures from a list of molecular systems into a single molecular system.

    This function collects structures from several molecular systems and returns a new
    molecular system whose structural dimension is the concatenation of the selected structures.
    All participating systems must be aligned in atom count and ordering over the chosen selections;
    use `selections` to provide per-system matching subsets when needed. Optionally, select specific
    structures from each input with `structure_indices`.

    Parameters
    ----------
    molecular_systems : list of molecular systems
        List of input molecular systems in any of the :ref:`supported forms <Introduction_Forms>`.
        Structures will be taken from these systems.
    selections : list, tuple, numpy.ndarray, int, str or 'all', default 'all'
        Atom selections for the input systems. A list or tuple contains one selection per
        system and must match `molecular_systems` in length. A scalar, string, NumPy array,
        or range is applied to every system. Nest index collections to provide a different
        collection for each system.
    structure_indices : list, tuple, numpy.ndarray, range, int or 'all', default 'all'
        0-based structure indices to include. A list or tuple contains one value or index
        collection per system and must match `molecular_systems` in length. A scalar, NumPy
        array, range, or `'all'` is applied to every system.
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
    - Input topology is optional after the first system establishes the output topology.
      Atom-count and ordering compatibility remain the caller's responsibility.
    - A native target with one chemical state associates new structures with that state
      implicitly. Multi-state targets preserve compatible explicit associations and use an
      unknown association only when the incoming state cannot be determined.
    - Lists and tuples always express per-system intent. Use a NumPy array or range when one
      index collection should be applied to every system.

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

    from . import append_structures, convert, extract, get_form
    from molsysmt._private.smonitor import ArgumentLengthError

    n_molecular_systems = len(molecular_systems)

    if not isinstance(selections, (list, tuple)):
        selections = [selections for ii in range(n_molecular_systems)]
    elif len(selections) != n_molecular_systems:
        raise ArgumentLengthError(
            argument="selections",
            expected=n_molecular_systems,
            actual=len(selections),
            caller="molsysmt.basic.concatenate_structures",
        )

    if not isinstance(structure_indices, (list, tuple)):
        structure_indices = [structure_indices for ii in range(n_molecular_systems)]
    elif len(structure_indices) != n_molecular_systems:
        raise ArgumentLengthError(
            argument="structure_indices",
            expected=n_molecular_systems,
            actual=len(structure_indices),
            caller="molsysmt.basic.concatenate_structures",
        )

    if to_form is None:
        to_molecular_system = extract(molecular_systems[0], selection=selections[0],
                                      structure_indices=structure_indices[0])
        to_form = get_form(to_molecular_system)
    else:
        to_molecular_system = convert(molecular_systems[0], to_form=to_form, selection=selections[0],
                                      structure_indices=structure_indices[0])

    for aux_molecular_system, aux_selection, aux_structure_indices in zip(molecular_systems[1:], selections[1:], structure_indices[1:]):
        append_structures(
            to_molecular_system,
            aux_molecular_system,
            selection=aux_selection,
            structure_indices=aux_structure_indices,
            syntax=syntax,
            in_place=True,
            skip_digestion=True,
        )

    output = to_molecular_system

    return output
