"""Delivering PDBQT structural attributes without full-trajectory conversion."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting selected PDBQT coordinates with explicit length units.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    indices : int, list, tuple or numpy.ndarray, default='all'
        Source element positions to query. Structural getters preserve requested atom
        order and repetitions.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    quantity or None
        Length-valued coordinates shaped (n_structures, n_atoms, 3), standardized
        through PyUnitWizard from angstroms.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    if indices is None or structure_indices is None:
        return None
    return item._series("coordinates", indices, structure_indices)


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_occupancy_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting dimensionless occupancies on the selected structure and atom axes.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    indices : int, list, tuple or numpy.ndarray, default='all'
        Source element positions to query. Structural getters preserve requested atom
        order and repetitions.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    numpy.ndarray
        Dimensionless occupancies shaped (n_structures, n_atoms), with NaN for absent
        fields.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    if indices is None or structure_indices is None:
        return None
    return item._series("occupancy", indices, structure_indices)


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_b_factor_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting selected B factors with explicit area units.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    indices : int, list, tuple or numpy.ndarray, default='all'
        Source element positions to query. Structural getters preserve requested atom
        order and repetitions.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    quantity or None
        Selected B factors with explicit area units, converted from angstrom squared.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    if indices is None or structure_indices is None:
        return None
    return item._series("b_factor", indices, structure_indices)


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Counting selected source structure indices, including repetitions.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    int
        Number of requested structure positions, counting repetitions.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    return len(item._axis(structure_indices, item.n_structures, "structure_indices"))


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_structure_index_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """Getting source positions independently of MODEL labels.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    numpy.ndarray
        Source structure positions in requested order, including repetitions and empty
        selections.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    return item._axis(structure_indices, item.n_structures, "structure_indices")


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting declared MODEL labels; an unwrapped source has no model label.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    numpy.ndarray or None
        Selected string MODEL labels, or None for an unwrapped source without declared
        model IDs.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    selected = item._axis(structure_indices, item.n_structures, "structure_indices")
    values = item._document.labels[selected].copy()
    return values if any(v is not None for v in item._document.labels) else None
