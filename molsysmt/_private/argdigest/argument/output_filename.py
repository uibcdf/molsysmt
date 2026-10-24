from os import PathLike
from pathlib import Path

from molsysmt._private.smonitor import ArgumentError


def digest_output_filename(output_filename, caller=None):
    """Normalize output paths on the host platform, retaining strings and None."""

    if isinstance(output_filename, PathLike):
        output_filename = str(Path(output_filename).absolute())

    if output_filename is None:
        return output_filename
    elif isinstance(output_filename, str):
        return output_filename

    raise ArgumentError(
        "output_filename", value=output_filename, caller=caller, message=None
    )
