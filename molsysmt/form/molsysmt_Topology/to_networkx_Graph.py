import pandas as pd

from molsysmt._private.argdigest import arg_digest

_ATOM_STATE_NAMES = {
    "formal_charge": "formal_charge",
    "is_aromatic": "atom_is_aromatic",
    "n_unpaired_electrons": "n_unpaired_electrons",
    "n_implicit_hydrogens": "n_implicit_hydrogens",
    "n_explicit_hydrogens": "n_explicit_hydrogens",
    "allows_implicit_hydrogens": "allows_implicit_hydrogens",
    "stereochemistry": "atom_stereochemistry",
}
_BOND_NAMES = {
    "bond_id": "bond_id",
    "bond_order": "bond_order",
    "fractional_bond_order": "fractional_bond_order",
    "bond_type": "bond_type",
    "is_aromatic": "bond_is_aromatic",
    "is_conjugated": "bond_is_conjugated",
    "stereochemistry": "bond_stereochemistry",
    "donor_atom_index": "bond_donor_atom_index",
    "acceptor_atom_index": "bond_acceptor_atom_index",
    "joins_components": "bond_joins_components",
    "evidence": "bond_evidence",
}


def _plain_value(value):
    """Return a NetworkX-safe scalar or ``None`` for missing data."""

    if pd.isna(value):
        return None
    return value.item() if hasattr(value, "item") else value


@arg_digest(form="molsysmt.Topology")
def to_networkx_Graph(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.Topology to networkx.Graph.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    networkx.Graph
        Resulting object in networkx.Graph form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.networkx_Graph._from_native import export_native

    return export_native(item, atom_indices=atom_indices, skip_digestion=True)
