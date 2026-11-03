"""Recover the old group-free representation only during explicit legacy decoding."""

import numpy as np

from molsysmt._private.smonitor import StructuralInconsistencyError

from ._atom_molecules import compact


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
