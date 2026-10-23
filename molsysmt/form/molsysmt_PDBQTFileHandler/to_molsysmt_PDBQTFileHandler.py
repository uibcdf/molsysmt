from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.PDBQTFileHandler")
def to_molsysmt_PDBQTFileHandler(
    item,
    atom_indices="all",
    structure_indices="all",
    copy_if_all=True,
    skip_digestion=False,
):
    """Copying a handler or producing a validated selected PDBQT document.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler with resident snapshot or source-bound indexed storage.
    atom_indices : int, list, tuple or numpy.ndarray, default='all'
        Source atom positions to retain. Native graph extraction uses the native
        canonical subset order.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure positions, independent of MODEL labels. Query/iteration order
        and repetitions are preserved; serialized documents require unique positions.
    copy_if_all : bool, default=True
        Return independent ownership for a full selection when True; False permits
        sharing the original handler.
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

    if is_all(atom_indices) and is_all(structure_indices):
        return item.copy() if copy_if_all else item
    return PDBQTFileHandler(
        "pdbqt_text:" + item._payload(atom_indices, structure_indices)
    )
