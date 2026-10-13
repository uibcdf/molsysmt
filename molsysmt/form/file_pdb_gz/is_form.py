"""Recognize compressed PDB paths without opening them."""

import os


def is_form(item):
    """Checking whether an item names a gzip PDB input.

    Parameters
    ----------
    item : molecular system
        String or path-like input to inspect without reading its contents.

    Returns
    -------
    bool
        Whether the path ends in .pdb.gz, case-insensitively.
    """
    if isinstance(item, os.PathLike):
        item = os.fspath(item)
    return (
        isinstance(item, str)
        and "\n" not in item
        and "\r" not in item
        and item.lower().endswith(".pdb.gz")
    )
