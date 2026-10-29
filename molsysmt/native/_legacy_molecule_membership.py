"""Recover the old group-free representation only during explicit legacy decoding."""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError

from ._atom_molecules import compact, stored


def validate_record_export(topology):
    """Reject new declarations that the legacy 0.1 dictionary cannot represent."""
    membership = stored(topology)
    if membership is None and not (
        topology.n_atoms and topology.n_molecules and not topology.n_groups
    ):
        return
    state = topology._resolve_reference_chemical_state()
    partition = state.component_indices.to_numpy(dtype=np.int64, na_value=-1)
    if (
        topology.n_groups
        or membership is None
        or np.any(membership < 0)
        or len(state.components) != topology.n_molecules
        or not np.array_equal(membership, partition)
    ):
        raise ValueError(
            "Dictionary schema 0.1 cannot preserve independent atom/molecule "
            "membership. Use H5MSM 0.5 until the independent dictionary "
            "schema is available."
        )


def restore(topology, states):
    """Snapshot legacy reference components into the independent stable inventory.

    Callers must establish the original shared atom axis. Missing or ambiguous
    source evidence cannot establish membership and remains unknown. Stable
    queries never invoke this migration helper.
    """
    if (
        topology is None
        or states is None
        or topology.n_groups
        or topology.n_molecules == 0
        or getattr(topology, "_atom_molecule_membership", None) is not None
    ):
        return
    if topology.n_atoms != states.n_atoms:
        raise StructuralInconsistencyError(
            reason="Legacy molecule migration requires a shared atom domain."
        )
    try:
        state = states._states[states._resolve_index()]
    except StructuralInconsistencyError:
        return
    if len(state.components) != topology.n_molecules:
        return
    values = state.component_indices.to_numpy(dtype=np.int64, na_value=-1)
    if (
        values.shape == (topology.n_atoms,)
        and np.all(values >= -1)
        and np.all(values < topology.n_molecules)
    ):
        topology._atom_molecule_membership = compact(values)
