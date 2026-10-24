import tempfile
from contextlib import contextmanager
from os.path import samefile
from pathlib import Path, PosixPath

from molsysmt._private.smonitor import ArgumentError


def validate_copy_destination(source, destination, *, caller=None):
    """Validate a resolved destination independent of the source inode."""
    if destination is None:
        raise ArgumentError(
            "output_filename",
            caller=caller,
            message="A copy destination must resolve to an independent output_filename.",
        )
    source_path, destination_path = Path(source), Path(destination)
    if destination_path.is_dir():
        raise ArgumentError(
            "output_filename",
            value=destination,
            caller=caller,
            message="output_filename must name a file, not a directory.",
        )
    aliases_source = source_path.resolve() == destination_path.resolve()
    if not aliases_source:
        try:
            aliases_source = samefile(source_path, destination_path)
        except FileNotFoundError:
            pass
    if aliases_source:
        raise ArgumentError(
            "output_filename",
            value=destination,
            caller=caller,
            message="The output_filename must refer to a different file from the source.",
        )


@contextmanager
def file_copy_destination(source, destination, *, caller=None):
    """Manage a session destination, or retain the caller's persistent destination."""
    automatic = destination is None
    if automatic:
        from molsysmt._private.session_files import reserve_copy_path

        destination = reserve_copy_path(source)
    try:
        validate_copy_destination(source, destination, caller=caller)
        if not automatic:
            from molsysmt._private.session_files import make_persistent

            make_persistent(destination)
        yield destination
    except BaseException:
        if automatic:
            from molsysmt._private.session_files import discard_copy

            discard_copy(destination)
        raise


def copy_file(source, destination, *, caller=None):
    """Copy raw bytes to a session-owned or caller-owned independent file."""
    from shutil import SameFileError, copyfile, copymode

    with file_copy_destination(source, destination, caller=caller) as output:
        try:
            copyfile(source, output)
            if destination is not None:
                copymode(source, output)
            # Automatic reservations retain private read/write permissions,
            # including when their source is read-only.
        except SameFileError as error:
            raise ArgumentError(
                "output_filename",
                value=output,
                caller=caller,
                message="The output_filename must refer to a different file from the source.",
            ) from error
        return output


def temp_filename(dir=None, extension=None):

    if not extension.startswith("."):
        extension = "." + extension

    file = tempfile.NamedTemporaryFile(suffix=extension, dir=dir, delete=True)
    filename = file.name
    file.close()
    return filename


def temp_directory():

    return tempfile.mkdtemp()


def str_filename(filename):

    if isinstance(filename, PosixPath):
        return str(filename)
    else:
        return filename
