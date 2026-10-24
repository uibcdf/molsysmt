from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "structure"])
@arg_digest()
def get_maximum_distances(
    molecular_system,
    selection="all",
    center_of_atoms=False,
    weights=None,
    as_entity=True,
    structure_indices="all",
    molecular_system_2=None,
    selection_2=None,
    center_of_atoms_2=False,
    weights_2=None,
    as_entity_2=True,
    structure_indices_2=None,
    pairs=False,
    pbc=False,
    engine="MolSysMT",
    syntax="MolSysMT",
):
    """
    Computing the maximum pairwise distances between two sets of atoms (or atom-group centers).

    Internally calls ``get_distances`` and then reduces the full distance matrix by
    selecting the maximum entry according to the ``as_entity`` / ``as_entity_2``
    flags.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Selection string or boolean/integer array specifying elements.
    center_of_atoms : bool, default=False
        Whether to compute distances relative to geometric centers.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    as_entity : bool, default=True
        Whether to reduce over the first endpoint population; False retains one result per first endpoint.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    molecular_system_2 : molecular system or None, default=None
        Second molecular system to compare with the first one.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    center_of_atoms_2 : bool, default=False
        Whether to compute distances relative to geometric centers for selection_2.
    weights_2 : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for selection_2.
    as_entity_2 : bool, default=True
        Whether to reduce over the second endpoint population; False retains one result per second endpoint.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    pairs : bool, default=False
        Whether corresponding selections define explicit pairs instead of a Cartesian product.
    pbc : bool, default=False
        Whether to take periodic boundary conditions into account.
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').

    Returns
    -------
    pairs_indices : numpy.ndarray
        Indices of the element pair (within the selection arrays) that achieves
        the maximum distance.  Shape depends on the ``as_entity`` flags and
        whether ``pairs`` mode is active.
    dists : quantity
        PyUnitWizard length quantity of the corresponding maximum distances in the
        standard length unit (nm).


    Raises
    ------
    ArgumentConflictError
        If both ``as_entity`` and ``as_entity_2`` are ``False`` (use
        ``get_distances`` directly in that case), or if ``pairs=True`` with
        ``as_entity=False`` or ``as_entity_2=False``.


    Notes
    -----
    Selections, weights and structure lists for the two endpoints remain
    independent. Structure lists are paired positionally and must have equal
    length; reuse a structure by repeating its index explicitly. Entity flags
    control reduction axes, while nested selections define weighted centers.
    Ties choose the first local occurrence in row-major order. Empty endpoint
    populations reject explicitly. Disk-backed distance intermediates are read
    one structure at a time and retired before returning the resident extrema.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.systems['particles 4']['traj_particles_4.xyznpy']
    >>> indices, values = get_maximum_distances(source,
    ...     selection=[0, 1], selection_2=[2, 3], center_of_atoms=True,
    ...     center_of_atoms_2=True, weights=[1., 1.], weights_2=[1., 3.], pbc=False)
    >>> msm.pyunitwizard.get_value(values, to_unit='nm').round(6).tolist()
    [3.579455, 1.118034, 2.09165]

    .. admonition:: User guide

       See :ref:`user-tools-distance-family`.

    .. versionadded:: 1.0.0
    """

    from ._distance_extrema import reduce, validate
    from .get_distances import get_distances

    caller = "molsysmt.structure.get_maximum_distances"
    validate(as_entity, as_entity_2, pairs, caller)

    all_dists = get_distances(
        molecular_system=molecular_system,
        selection=selection,
        center_of_atoms=center_of_atoms,
        weights=weights,
        structure_indices=structure_indices,
        molecular_system_2=molecular_system_2,
        selection_2=selection_2,
        center_of_atoms_2=center_of_atoms_2,
        weights_2=weights_2,
        structure_indices_2=structure_indices_2,
        pairs=pairs,
        pbc=pbc,
        engine=engine,
        syntax=syntax,
    )

    return reduce(all_dists, as_entity, as_entity_2, pairs, True, caller)
