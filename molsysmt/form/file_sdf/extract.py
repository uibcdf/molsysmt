from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from molsysmt._private.variables import is_all


@arg_digest(form="file:sdf")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):
    """Extracting an SDF subset into an explicitly named destination.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF file to extract.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include in native MolSys extraction order.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include; only zero exists.
    output_filename : str or pathlib.Path, default=None
        Destination path; required for a copy or subset. Public extract can also
        request a native to_form to avoid file output.
    copy_if_all : bool, default=True
        Whether to copy a complete selection. False returns the original path.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or pathlib.Path
        Destination, or source for an explicitly shared full selection.

    .. versionadded:: 1.0.0
    """
    from .to_file_sdf import to_file_sdf

    if output_filename is None and (
        copy_if_all or not is_all(atom_indices) or not is_all(structure_indices)
    ):
        raise ArgumentError(
            "output_filename",
            message="SDF extraction requires a destination path or a native to_form.",
        )
    return to_file_sdf(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        output_filename=output_filename,
        skip_digestion=True,
    )
