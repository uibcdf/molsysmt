import numpy as np
from smonitor import signal

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError, NotImplementedMethodError
from molsysmt.configure import with_configure_overrides

_CALLER = "molsysmt.structure.least_rmsd_align"


def _anchor_population(source, selection, structures, syntax, argument):
    from molsysmt.basic import get, select
    from molsysmt.basic._index_validation import normalize_mask

    if isinstance(selection, str):
        atoms = select(
            source, selection=selection, structure_indices=structures, syntax=syntax
        )
    else:
        atoms = normalize_mask(source, selection, "atom", _CALLER)
    if atoms is None or np.asarray(atoms).ndim != 1 or len(atoms) == 0:
        raise ArgumentError(
            argument,
            caller=_CALLER,
            message="Alignment requires one nonempty flat atom population.",
        )
    atoms = np.unique(np.asarray(atoms, dtype=np.int64))
    data = get(
        source,
        element="atom",
        selection=atoms,
        group_index=True,
        atom_name=True,
        output_type="dictionary",
    )
    groups = np.asarray(data["group_index"])
    names = np.asarray(data["atom_name"], dtype=object)
    return atoms, groups, names


def _paired_anchors(query, reference, groups, reference_groups):
    """Preserve aligned group pairs and match unambiguous selected atom names."""
    query_atoms, query_groups, query_names = query
    reference_atoms, reference_group_indices, reference_names = reference
    query_positions, reference_positions = {}, {}
    for position, group in enumerate(query_groups):
        query_positions.setdefault(int(group), []).append(position)
    for position, group in enumerate(reference_group_indices):
        reference_positions.setdefault(int(group), []).append(position)
    fitted, fitted_reference = [], []
    for group, reference_group in zip(groups, reference_groups, strict=True):
        left = query_positions[group]
        right = reference_positions[reference_group]
        left_names = query_names[left].tolist()
        right_names = reference_names[right].tolist()
        if (
            any(
                not isinstance(name, str) or not name
                for name in left_names + right_names
            )
            or len(set(left_names)) != len(left_names)
            or len(set(right_names)) != len(right_names)
            or set(left_names) != set(right_names)
        ):
            raise ArgumentError(
                "reference_selection",
                caller=_CALLER,
                message="Each aligned group pair must select the same unique atom names; use least_rmsd_fit for explicit arbitrary atom correspondences.",
            )
        by_name = dict(zip(right_names, reference_atoms[right], strict=True))
        fitted.extend(query_atoms[left].tolist())
        fitted_reference.extend(int(by_name[name]) for name in left_names)
    if len(fitted) < 3:
        raise ArgumentError(
            "selection",
            caller=_CALLER,
            message="Sequence alignment must supply at least three corresponding anchor atoms.",
        )
    return fitted, fitted_reference


@signal(tags=["api", "structure"])
@with_configure_overrides
@arg_digest()
def least_rmsd_align(
    molecular_system,
    selection='atom_name=="CA"',
    structure_indices="all",
    reference_molecular_system=None,
    reference_selection=None,
    reference_structure_index=0,
    syntax="MolSysMT",
    engine_sequence_alignment="Biopython",
    engine_least_rmsd_fit="MolSysMT",
    in_place=False,
    use_gpu=None,
    gpu_backend=None,
    precision=None,
    skip_digestion=False,
):
    """
    Aligning molecular components using sequence-derived atomic correspondences.

    The selected atom populations are projected to their original amino-acid
    groups. Biopython aligns these sequences; only identically aligned groups
    supply fit anchors. Selected atoms are paired by name within each matched
    group. A Kabsch fit computes a common rigid transformation per structure,
    applied to every atom in each query component touched by ``selection``.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing readable/writable
        coordinates, group identity, atom names and component membership.
    selection : str, list, tuple, or numpy.ndarray, default='atom_name=="CA"'
        Query anchor atom population: a selection expression, atom indices or
        a Boolean mask over the full query atom axis. Numeric values always
        address atoms, never groups. Order and repetitions do not change this
        population. Complete components containing these atoms are moved.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Nonnegative query structure indices to align. Nonconsecutive and
        repeated indices are supported; unselected structures stay unchanged.
    reference_molecular_system : molecular system or None, default=None
        Readable reference system. None uses the input system. Reference anchor
        coordinates are captured before edits, also for in-place self alignment.
    reference_selection : str, list, tuple, or numpy.ndarray, or None, default=None
        Anchor atom population on the reference's own atom axis. None uses
        ``selection``. Supply an independent selection when atom numbering or
        Boolean-mask lengths differ between the systems.
    reference_structure_index : int, default=0
        Nonnegative reference structure index used for every query structure.
    syntax : str, default='MolSysMT'
        Selection syntax used to resolve both atom populations before sequence
        projection. Resolved indices are delegated in canonical MolSysMT syntax.
    engine_sequence_alignment : str, default='Biopython'
        Sequence alignment provider. Only 'Biopython' is supported; the optional
        Biopython dependency is required for this calculation.
    engine_least_rmsd_fit : str, default='MolSysMT'
        Structural fit provider. Only 'MolSysMT' is supported.
    in_place : bool, default=False
        If True, update query components and return None. Otherwise return an
        independent aligned system in the query's form.
    use_gpu : bool or None, default=None
        GPU control delegated to least_rmsd_fit. None uses application settings.
    gpu_backend : str or None, default=None
        GPU backend delegated to least_rmsd_fit; None uses application settings.
    precision : {'single', 'double'} or None, default=None
        Precision delegated to least_rmsd_fit; None uses application settings.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated internal calls.

    Returns
    -------
    molecular system or None
        Independent aligned system when ``in_place=False``; None otherwise.

    Raises
    ------
    ArgumentError
        If an atom population or structure scope is invalid or empty, fewer
        than three corresponding atoms exist, or a matched group pair does not
        select the same unique atom names. Invalid correspondences reject before
        coordinate publication.
    StructuralInconsistencyError
        If fit anchors cannot define a unique three-dimensional rotation,
        including collinear points.
    NotImplementedMethodError
        If an unsupported sequence alignment or fit engine is requested.

    Notes
    -----
    Atom populations project to unique group indices in topology sequence order.
    Caps, water and other non-amino-acid groups do not supply sequence letters.
    The sequence tool retains its separate group-index selection contract.
    Paired source group indices remain paired when constructing atom anchors;
    atom numbering and local atom order may differ in the two systems.
    Mismatched amino acids do not supply anchors. Selected atoms in unmatched
    groups still contribute their components to the moved population.

    No chain-assignment search, chemistry preparation or periodic reconstruction
    is performed. Make components whole before fitting when appropriate. The
    reference and unselected query components remain unchanged. Native coordinate
    setters invalidate stored interaction coverage for edited structures.
    Length units and precision are handled by least_rmsd_fit and PyUnitWizard.
    Sequence-identity attribution and executed Biopython version remain owned by
    get_sequence_identity, including its optional Ackredit reporting.

    See Also
    --------
    molsysmt.topology.get_sequence_identity : Mapping identical aligned groups.
    molsysmt.structure.least_rmsd_fit : Fitting explicit ordered atom pairs.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    ...     structure_indices=[0, 8, 3])
    >>> atoms = msm.select(molsys, selection='atom_name=="CA"')
    >>> aligned = msm.structure.least_rmsd_align(
    ...     molsys, selection=atoms, structure_indices=[2, 0],
    ...     reference_structure_index=1, use_gpu=False)
    >>> msm.get(aligned, n_structures=True)
    3

    .. admonition:: Tutorial

       See :ref:`Tutorial_Least_rmsd_align` for independent atom populations and
       self-reference examples.

    .. versionadded:: 1.0.0
    """

    if engine_sequence_alignment != "Biopython" or engine_least_rmsd_fit != "MolSysMT":
        raise NotImplementedMethodError(caller=_CALLER)

    from molsysmt._private.structure_indices import ensure_nonempty_structure_indices
    from molsysmt.basic import get
    from molsysmt.basic._index_validation import validate_structure_indices
    from molsysmt.structure import least_rmsd_fit
    from molsysmt.topology import get_sequence_identity

    reference = (
        molecular_system
        if reference_molecular_system is None
        else reference_molecular_system
    )
    if reference_selection is None:
        reference_selection = selection
    structure_indices = validate_structure_indices(
        molecular_system, structure_indices, _CALLER
    )
    ensure_nonempty_structure_indices(structure_indices, caller=_CALLER)
    reference_structure_indices = validate_structure_indices(
        reference, [reference_structure_index], _CALLER
    )
    query = _anchor_population(
        molecular_system, selection, structure_indices, syntax, "selection"
    )
    target = _anchor_population(
        reference,
        reference_selection,
        reference_structure_indices,
        syntax,
        "reference_selection",
    )
    # Atom populations project to unique source groups in topology sequence order.
    # The sequence tool retains its independent group-index contract.
    _, groups, reference_groups = get_sequence_identity(
        molecular_system,
        selection=np.unique(query[1]).tolist(),
        reference_molecular_system=reference,
        reference_selection=np.unique(target[1]).tolist(),
        syntax="MolSysMT",
        engine="Biopython",
    )
    fitted, reference_fitted = _paired_anchors(query, target, groups, reference_groups)
    components = np.asarray(get(molecular_system, element="atom", component_index=True))
    selected_components = np.unique(components[query[0]])
    moving = np.flatnonzero(np.isin(components, selected_components)).tolist()

    return least_rmsd_fit(
        molecular_system=molecular_system,
        selection=moving,
        selection_fit=fitted,
        structure_indices=structure_indices,
        reference_molecular_system=reference,
        reference_selection_fit=reference_fitted,
        reference_structure_index=reference_structure_index,
        to_form=None,
        in_place=in_place,
        engine="MolSysMT",
        syntax="MolSysMT",
        use_gpu=use_gpu,
        gpu_backend=gpu_backend,
        precision=precision,
        skip_digestion=True,
    )
