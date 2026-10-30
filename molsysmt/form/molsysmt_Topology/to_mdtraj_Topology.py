from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.Topology")
@dep_digest("mdtraj")
def to_mdtraj_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.Topology to mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Independent target preserving selected atom order, declared hierarchy,
        available formal charges and bonds. Missing source groups/chains use
        temporary target-only parents, never new native assignments.

    Raises
    ------
    StructuralInconsistencyError
        If a group spans several declared chains or parent indices are invalid.

    Notes
    -----
    MDTraj requires every atom to belong to a residue and chain. Existing native
    groups retain their target order. Ungrouped atoms use UNL placeholders per
    known source molecule and chain; when molecule ownership is absent, each
    ungrouped atom receives its own placeholder. Missing chains share one target
    fallback chain. A partially assigned group's one known chain is used for
    that whole target group; conflicting known chains fail explicitly.

    These external residue/chain indices are not missing native group/chain
    indices. MDTraj selectors such as resid or protein operate on the target's
    available metadata, including placeholders. Atom-index selections remain
    aligned with the selected source atom order. No source hierarchy, chemistry
    or coordinates are changed, and no physical group identity is inferred.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.mdtraj_Topology._from_native import export_native

    return export_native(item, atom_indices=atom_indices, skip_digestion=True)
