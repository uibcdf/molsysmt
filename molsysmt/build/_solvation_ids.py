"""Preserve source labels by positional correspondence during OpenMM solvation."""

import numpy as np
import pandas as pd

from molsysmt._private.smonitor import StructuralInconsistencyError


def capture(source, modeller):
    """Retain original nullable labels without interpreting them as integers."""
    from molsysmt.basic import get

    atom_ids, group_indices = get(
        source, element="atom", atom_id=True, group_index=True
    )
    group_ids = get(source, element="group", group_id=True)
    # The provider copies the source by chain/group traversal. Its canonical
    # indexing must agree with positions before relying on the retained prefix.
    for elements, kind in (
        (modeller.topology.atoms(), "atom"),
        (modeller.topology.residues(), "group"),
    ):
        if any(element.index != index for index, element in enumerate(elements)):
            raise StructuralInconsistencyError(
                reason=f"OpenMM solvation requires {kind} traversal to agree with its positional indices; explicitly reorder the source before solvation.",
                caller="molsysmt.build.solvate",
            )
    return dict(
        atom_ids=list(atom_ids),
        group_ids=list(group_ids),
        group_indices=np.asarray(group_indices, dtype=np.int64),
    )


def _labels(original, source_to_output, n_output):
    output = pd.array([pd.NA] * n_output, dtype="string")
    retained = source_to_output >= 0
    output[source_to_output[retained]] = pd.array(original, dtype="string")[retained]
    reserved = set(output.dropna())
    new = np.ones(n_output, dtype=bool)
    new[source_to_output[retained]] = False
    next_id = 1
    for index in np.flatnonzero(new):
        while str(next_id) in reserved:
            next_id += 1
        output[index] = str(next_id)
        reserved.add(str(next_id))
        next_id += 1
    return output


def restore(output, labels, atom_map=None):
    """Label retained source sites and allocate only generated-site labels."""
    from molsysmt.basic import set

    n_source = len(labels["atom_ids"])
    forward = (
        np.arange(n_source, dtype=np.int64)
        if atom_map is None
        else np.asarray(atom_map[:n_source], dtype=np.int64)
    )
    group_map = np.full(len(labels["group_ids"]), -1, dtype=np.int64)
    if atom_map is None:
        group_map[:] = np.arange(len(group_map))
    else:
        retained = forward >= 0
        groups = output.topology.atoms["group_index"].to_numpy(dtype=np.int64)
        group_map[labels["group_indices"][retained]] = groups[forward[retained]]
    set(
        output,
        element="atom",
        atom_id=_labels(labels["atom_ids"], forward, output.topology.n_atoms).to_numpy(
            dtype=object
        ),
    )
    set(
        output,
        element="group",
        group_id=_labels(
            labels["group_ids"], group_map, output.topology.n_groups
        ).to_numpy(dtype=object),
    )
