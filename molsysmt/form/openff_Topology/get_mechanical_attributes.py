"""Delivering complete partial-charge arrays from OpenFF topologies."""

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


def _partial_charges(item):
    molecules = list(item.molecules)
    if not molecules or any(
        molecule.partial_charges is None for molecule in molecules
    ):
        return None
    return np.concatenate(
        [
            molecule.partial_charges.m_as('elementary_charge')
            for molecule in molecules
        ]
    ).astype(np.float64, copy=False)


@arg_digest(form='openff.Topology')
def get_partial_charge_from_atom(
    item, indices='all', skip_digestion=False
):
    """Returning complete partial charges in elementary-charge units."""

    values = _partial_charges(item)
    if values is None:
        return None
    if not is_all(indices):
        values = values[indices]
    return puw.quantity(values, 'elementary_charge', standardized=True)


@arg_digest(form='openff.Topology')
def get_partial_charge_from_system(item, skip_digestion=False):
    """Returning all available partial charges in elementary-charge units."""

    return get_partial_charge_from_atom(item, skip_digestion=True)
