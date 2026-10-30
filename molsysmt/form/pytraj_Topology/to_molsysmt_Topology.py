from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest


def _element_symbol(atom):
    """Return an elemental symbol without reusing a force-field atom type."""

    if atom.atomic_number <= 0:
        return None
    from pytraj.core.elements import atomic_number_element_dict

    symbol = atomic_number_element_dict.get(atom.atomic_number, "")
    if symbol in {"??", "xp", ""}:
        return None
    return symbol.capitalize()


@arg_digest(form="pytraj.Topology")
@dep_digest("pytraj")
def to_molsysmt_Topology(item, atom_indices="all", skip_digestion=False):
    """
    Converting from pytraj.Topology to molsysmt.Topology.


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
