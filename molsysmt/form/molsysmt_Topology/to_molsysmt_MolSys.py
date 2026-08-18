from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.Topology")
def to_molsysmt_MolSys(
    item,
    coordinates=None,
    box=None,
    atom_indices="all",
    skip_digestion=False,
):
    """
    Converting from molsysmt.Topology to molsysmt.MolSys.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item in molsysmt.Topology form.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.native import MolSys, Structures

    from .extract import extract

    output = MolSys(skip_digestion=True)
    output.topology = extract(
        item,
        atom_indices=atom_indices,
        copy_if_all=True,
        skip_digestion=True,
    )

    if coordinates is not None and not is_all(atom_indices):
        coordinates = coordinates[:, atom_indices, :]
    output.structures = Structures(
        coordinates=coordinates,
        box=box,
        skip_digestion=True,
    )

    return output
