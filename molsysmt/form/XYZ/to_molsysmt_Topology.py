from molsysmt._private.argdigest import arg_digest

@arg_digest(form='XYZ')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from XYZ to molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native.topology import Topology
    from molsysmt._private.variables import is_all
    from . import get_n_atoms_from_system

    if is_all(atom_indices):
        n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        n_atoms = len(atom_indices)
    tmp_item = Topology(n_atoms=n_atoms)

    return tmp_item
