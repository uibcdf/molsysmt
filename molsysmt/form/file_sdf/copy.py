from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError


@arg_digest(form="file:sdf")
def copy(item, output_filename=None, skip_digestion=False):
    """Copying a supported SDF record without changing its source bytes.

    Parameters
    ----------
    item : str or pathlib.Path
        Single-record SDF source file.
    output_filename : str or pathlib.Path, default=None
        Required destination; no implicit temporary file is created.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    str or pathlib.Path
        Destination path, preserving source property blocks and syntax.

    .. versionadded:: 1.0.0
    """
    from pathlib import Path

    from .to_file_sdf import to_file_sdf

    if (
        output_filename is None
        or Path(item).resolve() == Path(output_filename).resolve()
    ):
        raise ArgumentError(
            "output_filename",
            value=output_filename,
            message="Copying SDF requires a distinct destination path.",
        )
    return to_file_sdf(item, output_filename=output_filename, skip_digestion=True)
