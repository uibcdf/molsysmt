"""Providing the direct structure-count route for index validation."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def get_n_structures_from_system(item, skip_digestion=False):
    """Getting the supported SDF structure count.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF file; parsing verifies the one-record contract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        One for a supported molecular record.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import read_sdf

    read_sdf(item, allow_stereo=True)
    return 1
