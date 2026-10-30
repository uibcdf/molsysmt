import pandas as pd
from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


def _openmm_element(atom_type, app):
    """Resolve direct symbols and unambiguous dotted Tripos atom types."""

    if atom_type is None or pd.isna(atom_type):
        return None
    value = str(atom_type).strip()
    candidates = [value]
    if "." in value:
        candidates.append(value.split(".", maxsplit=1)[0])
    for candidate in candidates:
        try:
            return app.Element.getBySymbol(candidate)
        except KeyError:
            continue
    return None


@arg_digest(form="molsysmt.Topology")
@dep_digest("openmm")
def to_openmm_Topology(item, box=None, atom_indices="all", skip_digestion=False):
    """
    Converting from molsysmt.Topology to openmm.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    box : object, default=None
        Argument box.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.openmm_Topology._from_native import export_native

    return export_native(item, atom_indices=atom_indices, box=box, skip_digestion=True)
