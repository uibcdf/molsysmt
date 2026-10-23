"""Reading explicit PDBQT mechanical labels without deriving assignments."""

import numpy as np

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_atom_ff_type_from_atom(item, indices="all", skip_digestion=False):
    """Getting stored atom_ff_type values on selected source atoms.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    indices : int, list, tuple or numpy.ndarray, default='all'
        Source element positions to query. Structural getters preserve requested atom
        order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    numpy.ndarray
        Source-aligned AutoDock4 labels, distinct from chemical element symbols.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    selected = item._axis(indices, item.n_atoms, "indices")
    return np.asarray(
        [item._document.first["atoms"][atom]["atom_ff_type"] for atom in selected]
    )


@arg_digest(form="molsysmt.PDBQTFileHandler")
def get_partial_charge_from_atom(item, indices="all", skip_digestion=False):
    """Getting stored partial_charge values on selected source atoms.

    Parameters
    ----------
    item : molecular system
        Open PDBQT handler retaining a validated resident document snapshot.
    indices : int, list, tuple or numpy.ndarray, default='all'
        Source element positions to query. Structural getters preserve requested atom
        order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip argument digestion for already validated inputs.

    Returns
    -------
    numpy.ndarray
        Explicit written charges in elementary-charge units, with no recalculation or
        renormalization.

    Notes
    -----
    Document conversions preserve only declared PDBQT evidence. Native graph projections omit the format-specific torsion tree only under the stated authorization; they do not infer complete chemistry. Closed handlers reject data queries.

    .. versionadded:: 1.0.0
    """
    selected = item._axis(indices, item.n_atoms, "indices")
    return np.asarray(
        [item._document.first["atoms"][atom]["partial_charge"] for atom in selected]
    )
