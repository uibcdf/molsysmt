from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def to_molsysmt_MolecularMechanics(
    item,
    atom_indices="all",
    structure_indices="all",
    discard_torsion_tree=True,
    skip_digestion=False,
):
    """Converting selected PDBQT document data to native MolecularMechanics.

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
    discard_torsion_tree : bool, default=True
        Explicitly authorize omission of document-specific torsion evidence from a
        native domain. No complete graph or missing bond orders are inferred.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    molsysmt.MolecularMechanics
        Independent selected native data; no complete chemical graph is inferred.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    return item._domain(
        "molecular_mechanics", atom_indices, structure_indices, discard_torsion_tree
    )
