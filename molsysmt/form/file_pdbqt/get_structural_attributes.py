"""Reading selected PDBQT structure attributes through an owned document."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:pdbqt")
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting selected coordinate blocks after full document validation.

    Parameters
    ----------
    item : molecular system
        Path to a PDBQT file; opening validates every model before returning data.
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
    from molsysmt.native import PDBQTFileHandler

    if indices is None or structure_indices is None:
        return None
    with PDBQTFileHandler(item) as handler:
        return handler._series("coordinates", indices, structure_indices)


@arg_digest(form="file:pdbqt")
def get_occupancy_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting selected dimensionless occupancy blocks after document validation.

    Parameters
    ----------
    item : molecular system
        Path to a PDBQT file; opening validates every model before returning data.
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
    from molsysmt.native import PDBQTFileHandler

    if indices is None or structure_indices is None:
        return None
    with PDBQTFileHandler(item) as handler:
        return handler._series("occupancy", indices, structure_indices)


@arg_digest(form="file:pdbqt")
def get_b_factor_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """Getting selected B-factor blocks with explicit area units.

    Parameters
    ----------
    item : molecular system
        Path to a PDBQT file; opening validates every model before returning data.
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
    from molsysmt.native import PDBQTFileHandler

    if indices is None or structure_indices is None:
        return None
    with PDBQTFileHandler(item) as handler:
        return handler._series("b_factor", indices, structure_indices)


@arg_digest(form="file:pdbqt")
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting selected source structure_id values from the document index.

    Parameters
    ----------
    item : molecular system
        Path to a PDBQT file; opening validates every model before returning data.
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
    from molsysmt.form.molsysmt_PDBQTFileHandler.get_structural_attributes import (
        get_structure_id_from_system as get_attribute,
    )
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(item) as handler:
        return get_attribute(handler, structure_indices=structure_indices)


@arg_digest(form="file:pdbqt")
def get_structure_index_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """Getting selected source structure_index values from the document index.

    Parameters
    ----------
    item : molecular system
        Path to a PDBQT file; opening validates every model before returning data.
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
    from molsysmt.form.molsysmt_PDBQTFileHandler.get_structural_attributes import (
        get_structure_index_from_system as get_attribute,
    )
    from molsysmt.native import PDBQTFileHandler

    with PDBQTFileHandler(item) as handler:
        return get_attribute(handler, structure_indices=structure_indices)
