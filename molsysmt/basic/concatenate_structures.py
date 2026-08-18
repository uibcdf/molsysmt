from molsysmt._private.argdigest import arg_digest
from smonitor import signal

@signal(tags=['api', 'structure'])
@arg_digest()
def concatenate_structures(molecular_systems, selections='all', structure_indices='all', to_form=None,
                           syntax='MolSysMT', attribute_policy='intersection',
                           skip_digestion=False):
    """
    Concatenate structures from a list of molecular systems into a single molecular system.

    This function collects structures from several molecular systems and returns a new
    molecular system whose structural dimension is the concatenation of the selected structures.
    All participating systems must be aligned in atom count and ordering over the chosen selections;
    use `selections` to provide per-system matching subsets when needed. Optionally, select specific
    structures from each input with `structure_indices`.


    Parameters
    ----------
    molecular_systems : object
        Argument molecular_systems.
    selections : object, default='all'
        Argument selections.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    to_form : object, default=None
        Argument to_form.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    attribute_policy : object, default='intersection'
        Argument attribute_policy.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

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
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )

    output = to_molecular_system

    return output
