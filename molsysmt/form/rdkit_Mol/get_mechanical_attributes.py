"""Delivering optional per-atom mechanical metadata from RDKit molecules."""

import numpy as np

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw


_PARTIAL_CHARGE_PROPERTIES = (
    '_MolSysMTPartialCharge',
    'PartialCharge',
    '_GasteigerCharge',
    '_TriposPartialCharge',
)


def _get_partial_charges(item):
    """Return the first complete supported partial-charge property series."""

    atoms = list(item.GetAtoms())
    for property_name in _PARTIAL_CHARGE_PROPERTIES:
        if atoms and all(atom.HasProp(property_name) for atom in atoms):
            try:
                values = np.asarray(
                    [atom.GetDoubleProp(property_name) for atom in atoms],
                    dtype=np.float64,
                )
            except Exception:
                try:
                    values = np.asarray(
                        [float(atom.GetProp(property_name)) for atom in atoms],
                        dtype=np.float64,
                    )
                except (TypeError, ValueError):
                    continue
            if np.all(np.isfinite(values)):
                return values
    return None


@arg_digest(form='rdkit.Mol')
def get_partial_charge_from_atom(item, indices='all', skip_digestion=False):
    """Returning available partial charges in elementary-charge units."""

    values = _get_partial_charges(item)
    if values is None:
        return None
    if not is_all(indices):
        values = values[indices]
    return puw.quantity(values, 'elementary_charge', standardized=True)


@arg_digest(form='rdkit.Mol')
def get_partial_charge_from_system(item, skip_digestion=False):
    """Returning all available partial charges in elementary-charge units."""

    return get_partial_charge_from_atom(item, skip_digestion=True)
