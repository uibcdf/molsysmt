"""Providing a direct size route for public index validation."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def get_n_atoms_from_system(item, skip_digestion=False):
    """Getting the explicit SDF atom count.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF file to inspect.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        Number of explicitly stored atoms, including source hydrogens.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import read_sdf

    return len(read_sdf(item, allow_stereo=True).atoms)
