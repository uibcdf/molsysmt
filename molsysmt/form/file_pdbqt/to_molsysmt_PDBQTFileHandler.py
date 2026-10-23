from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="file:pdbqt")
def to_molsysmt_PDBQTFileHandler(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """Opening and validating a PDBQT snapshot with independently owned lifetime.

    Parameters
    ----------
    item : molecular system
        Path to a PDBQT file; opening validates every model before returning data.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom positions to retain. Native graph extraction uses the native
        canonical subset order.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    molsysmt.PDBQTFileHandler
        Independent selected native data; no complete chemical graph is inferred.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    from molsysmt.native import PDBQTFileHandler

    output = PDBQTFileHandler(item)
    if is_all(atom_indices) and is_all(structure_indices):
        return output
    try:
        from molsysmt.form.molsysmt_PDBQTFileHandler.extract import extract

        return extract(
            output, atom_indices=atom_indices, structure_indices=structure_indices
        )
    finally:
        output.close()
