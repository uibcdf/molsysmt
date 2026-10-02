from pathlib import Path


def is_form(item):
    """Checking whether a path denotes an SDF file.

    Parameters
    ----------
    item : str or pathlib.Path
        Path to inspect; recognition does not read the file.

    Returns
    -------
    bool
        Whether the path has the SDF extension, ignoring case.

    .. versionadded:: 1.0.0
    """
    return isinstance(item, (str, Path)) and str(item).lower().endswith(".sdf")
