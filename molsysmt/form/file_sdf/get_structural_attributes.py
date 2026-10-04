"""Providing the direct structure-count route for index validation."""

from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:sdf")
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """Getting the supported SDF structure count.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF file; parsing verifies the one-record contract.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Structure indices (0-based). Only index 0 exists; an empty selection
        returns zero. Repeated indices count as repeated requested structures.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    int
        Number of requested structures from the supported single record.

    .. versionadded:: 1.0.0
    """
    from molsysmt._private.ctfile import read_sdf
    from molsysmt._private.smonitor import ArgumentError
    from molsysmt._private.variables import is_all

    read_sdf(item, allow_stereo=True)
    if structure_indices is None or is_all(structure_indices):
        return 1
    if any(index != 0 for index in structure_indices):
        raise ArgumentError(
            "structure_indices",
            value=structure_indices,
            caller="get_n_structures_from_system",
        )
    return len(structure_indices)
