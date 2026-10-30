import numpy as np
import pandas as pd

from molsysmt._private.argdigest import arg_digest


def _series_to_list(series):
    """Exporting nullable table scalars as ordinary JSON values."""
    return [
        None
        if pd.isna(value)
        else value.item()
        if isinstance(value, np.generic)
        else value
        for value in series
    ]


@arg_digest(form="molsysmt.Topology")
def to_molsysmt_ViewerJSON(item, skip_digestion=False):
    """
    Converting from molsysmt.Topology to molsysmt.ViewerJSON.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.ViewerJSON
        Graphics payload containing ordinary JSON scalars and containers.
        Missing table values become null; bond endpoints are positional indices.

    Notes
    -----
    Per-atom group_index, chain_index and entity_index columns retain distinct
    identities when labels repeat. ID columns remain strings; this graphics
    projection omits molecule metadata and is not a full topology archive.

    Examples
    --------
    >>> import json
    >>> from molsysmt.native import Topology
    >>> topology = Topology(n_atoms=2)
    >>> topology.add_bonds([[0, 1]])
    >>> payload = to_molsysmt_ViewerJSON(topology)
    >>> json.loads(payload.dumps())["bonds"]["atom_pairs"]
    [[0, 1]]

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_ViewerJSON._from_native import export_native

    return export_native(item, skip_digestion=True)
