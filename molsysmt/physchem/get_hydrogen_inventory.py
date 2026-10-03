"""Auditing a stored hydrogen inventory without predicting a protonation state."""

from smonitor import signal

from molsysmt._private.argdigest import arg_digest


@signal(tags=["api", "physchem"])
@arg_digest()
def get_hydrogen_inventory(
    molecular_system,
    selection="all",
    structure_indices="all",
    chemical_state="reference",
    syntax="MolSysMT",
    skip_digestion=False,
):
    """Getting indexed and stored hydrogen counts for selected parent atoms.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form providing elements and stored chemical assignments.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Parent atoms to report. The full graph is audited before selecting output.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Select at most one for state resolution.
    chemical_state : str or int, default='reference'
        Selected state; 'structure' resolves its selected frame association.
    syntax : str, default='MolSysMT'
        Syntax used for selection.
    skip_digestion : bool, default=False
        Whether to skip argument digestion.

    Returns
    -------
    dict
        Detached molsysmt.hydrogen_inventory@1 report with int64 atom_indices,
        indexed_hydrogen_counts, missing_hydrogen_counts and total_hydrogen_counts.
        Unknown counts are -1. parent_hydrogen_pairs has shape (n_pairs, 2),
        parent first. Status is available, unassessed, conflict or empty;
        indexed issues retain diagnostics. Counts have no units.

    Raises
    ------
    ArgumentError
        If selection, state or frame arguments are invalid.
    StructuralInconsistencyError
        If source chemical and structural domains are incompatible.

    Notes
    -----
    Stored n_explicit_hydrogens denotes annotated virtual H, not indexed neighbors.
    Both stored counts are added to the indexed-neighbor count for the total.
    Available means the stored inventory can be read; valence and protonation
    are not independently validated. No atoms, counts or coordinates are changed.

    See Also
    --------
    get_chemical_readiness : Audit other stored chemical fields.
    molsysmt.build.add_missing_hydrogens : Materialize H for a fixed prepared state.

    Examples
    --------
    >>> import molsysmt as msm
    >>> report = msm.physchem.get_hydrogen_inventory(msm.systems['caffeine']['caffeine.sdf'])
    >>> int(report['indexed_hydrogen_counts'].sum())
    10

    .. admonition:: User guide

       See :ref:`Tutorial_Hydrogen_Inventory` for counts, scopes and limitations.

    .. versionadded:: 1.0.0
    """
    if not isinstance(skip_digestion, bool):
        from molsysmt._private.argdigest.argument.skip_digestion import (
            digest_skip_digestion,
        )

        digest_skip_digestion(
            skip_digestion, caller=__name__ + ".get_hydrogen_inventory"
        )
    from molsysmt._private.hydrogen_inventory import inventory

    return inventory(
        molecular_system,
        selection,
        structure_indices,
        chemical_state,
        syntax,
        "molsysmt.physchem.get_hydrogen_inventory",
    )
