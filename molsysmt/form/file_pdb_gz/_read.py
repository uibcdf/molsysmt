"""Decode one gzip input without temporary files or parser duplication."""

import gzip
import io
import zlib

from molsysmt._private.smonitor import FileContentError


def read_text(item):
    """Close the gzip stream on success and every read failure."""
    try:
        with gzip.open(item, "rt", encoding="utf-8") as source:
            return source.read()
    except (gzip.BadGzipFile, EOFError, zlib.error, UnicodeDecodeError) as error:
        raise FileContentError(
            reason="Invalid, truncated or non-UTF-8 gzip PDB input.",
            filename=str(item),
            caller="molsysmt.form.file_pdb_gz",
        ) from error


def read_handler(item):
    """Transfer ownership of a decoded buffer only after successful parsing."""
    from molsysmt.native import PDBFileHandler

    buffer = io.StringIO(read_text(item))
    try:
        return PDBFileHandler(buffer, io_mode="r")
    except BaseException:
        buffer.close()
        raise
