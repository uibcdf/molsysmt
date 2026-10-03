from pathlib import Path


def is_form(item):
    """Checking whether an item declares the file:pdbqt form.

    Parameters
    ----------
    item : object
        Candidate item; recognition does not parse its contents.

    Returns
    -------
    bool
        Whether the explicit prefix or filename extension matches.

    .. versionadded:: 1.0.0
    """
    return isinstance(item, (str, Path)) and str(item).lower().endswith(".pdbqt")
