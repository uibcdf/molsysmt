from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openff.Topology to molsysmt.Structures.

    Parameters
    ----------
    item : openff.Topology
        Source item in openff.Topology form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import Structures

    tmp_item = Structures()
    return tmp_item
