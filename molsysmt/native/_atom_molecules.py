"""Validate and project stable molecule ownership without chemical-state access."""

import numpy as np
import pandas as pd

from molsysmt._private.argdigest.argument._correspondence_axes import flat_axis
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt._private.variables import is_all

CALLER = "molsysmt.native.Topology.set_atom_molecules"


def _inconsistent(reason):
    raise StructuralInconsistencyError(reason=reason, caller=CALLER)


def _groups(topology):
    groups = topology.atoms["group_index"].to_numpy(dtype=np.int64, na_value=-1)
    if np.any(groups < -1) or np.any(groups >= topology.n_groups):
        _inconsistent("Atom group membership is outside the stable group inventory.")
    owners = topology.groups["molecule_index"].to_numpy(dtype=np.int64, na_value=-1)
    if np.any(owners < -1) or np.any(owners >= topology.n_molecules):
        _inconsistent(
            "Group molecule membership is outside the stable molecule inventory."
        )
    return groups, owners


def stored(topology, *, check_groups=True):
    """Return the optional canonical vector, rejecting stale index domains."""
    value = getattr(topology, "_atom_molecule_membership", None)
    if value is None:
        return None
    if (
        not isinstance(value, np.ndarray)
        or value.dtype != np.dtype("int64")
        or value.shape != (topology.n_atoms,)
        or np.any(value < -1)
        or np.any(value >= topology.n_molecules)
    ):
        _inconsistent(
            "Ungrouped molecule membership requires an aligned int64 vector of valid indices or -1."
        )
    if check_groups:
        groups, _ = _groups(topology)
        if np.any(value[groups >= 0] != -1):
            _inconsistent(
                "Grouped atoms cannot also store independent molecule membership."
            )
    return value


def resolve(topology):
    """Project disjoint grouped and ungrouped memberships as positional indices."""
    groups, owners = _groups(topology)
    direct = stored(topology)
    result = (
        np.full(topology.n_atoms, -1, dtype=np.int64)
        if direct is None
        else direct.copy()
    )
    grouped = groups >= 0
    result[grouped] = owners[groups[grouped]]
    return result


def compact(values):
    """Own a canonical vector only when it carries a known ungrouped owner."""
    if not np.any(values >= 0):
        return None
    result = np.array(values, dtype=np.int64, copy=True)
    result.flags.writeable = False
    return result


def prepare(topology, molecule_indices, atom_indices):
    """Stage a complete declaration without changing inventory or owner state."""
    indices = (
        atom_indices
        if isinstance(atom_indices, np.ndarray)
        and atom_indices.dtype == np.dtype("int64")
        and atom_indices.ndim == 1
        else flat_axis(atom_indices, "atom_indices", CALLER)
    )
    if is_all(indices):
        indices = np.arange(topology.n_atoms, dtype=np.int64)
    if (
        indices is None
        or isinstance(indices, str)
        or np.any(indices < 0)
        or np.any(indices >= topology.n_atoms)
        or len(np.unique(indices)) != len(indices)
    ):
        raise ArgumentError("atom_indices", value=atom_indices, caller=CALLER)
    if hasattr(molecule_indices, "unit") or hasattr(molecule_indices, "units"):
        raise ArgumentError("molecule_indices", value=molecule_indices, caller=CALLER)
    if molecule_indices is None:
        values = [-1] * len(indices)
    else:
        raw = np.asarray(molecule_indices, dtype=object)
        if raw.ndim == 0:
            raw = raw.reshape(1)
        if raw.ndim != 1 or len(raw) != len(indices):
            raise ArgumentError(
                "molecule_indices", value=molecule_indices, caller=CALLER
            )
        values = []
        for value in raw:
            if value is None or value is pd.NA:
                values.append(-1)
            elif (
                isinstance(value, (int, np.integer))
                and not isinstance(value, (bool, np.bool_))
                and 0 <= value <= np.iinfo(np.int64).max
            ):
                values.append(int(value))
            else:
                raise ArgumentError(
                    "molecule_indices", value=molecule_indices, caller=CALLER
                )
    values = np.asarray(values, dtype=np.int64)
    if np.any(values >= topology.n_molecules):
        _inconsistent("Molecule assignments must identify stored molecule indices.")
    groups, owners = _groups(topology)
    previous = stored(topology, check_groups=False)
    candidate = (
        np.full(topology.n_atoms, -1, dtype=np.int64)
        if previous is None
        else previous.copy()
    )
    selected_groups = groups[indices]
    grouped = selected_groups >= 0
    if np.any(values[grouped] != owners[selected_groups[grouped]]):
        _inconsistent("A grouped atom must retain its group's molecule assignment.")
    if np.any(
        (candidate[indices[grouped]] >= 0)
        & (candidate[indices[grouped]] != values[grouped])
    ):
        _inconsistent("Adding a group cannot discard a conflicting declared molecule.")
    candidate[indices] = values
    candidate[indices[grouped]] = -1
    if np.any(candidate[groups >= 0] != -1):
        _inconsistent(
            "Reconcile grouped molecule declarations explicitly before changing other atoms."
        )
    return compact(candidate)


def transport(topology, output_to_input_atom_indices):
    """Transport stored stable ownership through an already validated atom map.

    A negative source position denotes a new atom without declared ownership.
    Repeated source positions let a caller explicitly inherit a parent's stable
    molecule, for example when adding a terminal hydrogen. This reads no chemistry.
    """
    membership = stored(topology)
    if membership is None:
        return None
    indices = np.asarray(output_to_input_atom_indices, dtype=np.int64)
    known = indices >= 0
    result = np.full(len(indices), -1, dtype=np.int64)
    result[known] = membership[indices[known]]
    return compact(result)
