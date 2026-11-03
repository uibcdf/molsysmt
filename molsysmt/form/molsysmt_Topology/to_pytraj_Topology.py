import pandas as pd
from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


def _pytraj_residue_number(group_id, group_index):
    """Return a PyTraj-compatible integer residue number."""

    try:
        return int(group_id)
    except (TypeError, ValueError, OverflowError):
        return int(group_index) + 1


def _pytraj_chain_id(item, chain_index):
    """Return the textual chain identifier required by PyTraj."""

    if pd.isna(chain_index):
        return ""
    try:
        chain_index = int(chain_index)
    except (TypeError, ValueError, OverflowError):
        return ""
    if chain_index < 0 or chain_index >= item.n_chains:
        return ""
    chain_id = item.chains.iloc[chain_index]["chain_id"]
    return "" if pd.isna(chain_id) else str(chain_id)


def _pytraj_chain_index(chain_index):
    """Return the integer chain value required by legacy PyTraj builds."""

    if pd.isna(chain_index):
        return 0
    try:
        return int(chain_index)
    except (TypeError, ValueError, OverflowError):
        return 0


def _pytraj_uses_text_chain_id(residue_type):
    """Detect which incompatible PyTraj 2.0.6 residue ABI is installed."""

    try:
        residue_type("UNK", resid=0, icode=0, chainID="")
    except (AttributeError, TypeError):
        return False
    return True


@arg_digest(form="molsysmt.Topology")
@dep_digest("pytraj")
def to_pytraj_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.Topology to pytraj.Topology.


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
    pytraj.Topology
        Resulting object in pytraj.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.pytraj_Topology._from_native import export_native

    return export_native(item, atom_indices=atom_indices, skip_digestion=True)
