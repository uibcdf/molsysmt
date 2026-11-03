"""Converting an OpenFF molecule into normalized native chemical-state storage."""

from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


def _formal_charge_value(atom):
    charge = getattr(atom, "formal_charge", None)
    try:
        return int(charge.m)
    except Exception:
        try:
            return int(charge)
        except Exception:
            return None


def _fractional_order_value(bond):
    value = getattr(bond, "fractional_bond_order", None)
    if value is None:
        return None
    try:
        return float(value)
    except Exception:
        return None


@dep_digest("rdkit")
def _bond_stereo_metadata(item):
    """Return OpenFF E/Z labels with the reference atoms chosen by RDKit."""

    molecule = item.to_rdkit()
    metadata = {}
    for bond in molecule.GetBonds():
        stereo = str(bond.GetStereo())
        if stereo not in {"STEREOE", "STEREOZ"}:
            continue
        references = list(bond.GetStereoAtoms())
        if len(references) != 2:
            continue
        key = frozenset((bond.GetBeginAtomIdx(), bond.GetEndAtomIdx()))
        metadata[key] = (stereo[-1], references[0], references[1])
    return metadata


@arg_digest(form="openff.Molecule")
def to_molsysmt_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from openff.Molecule to molsysmt.Topology.


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
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from ._read_native import read_native

    return read_native(item, atom_indices=atom_indices, skip_digestion=True).topology
