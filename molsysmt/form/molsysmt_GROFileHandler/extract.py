from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.GROFileHandler")
def extract(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    copy_if_all=True,
    skip_digestion=False,
):
    """
    Extracting a subset of elements or structures from form molsysmt.GROFileHandler.


    Parameters
    ----------
    item : molecular system
        Source object or file in the form named by this adapter.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    copy_if_all : bool, default=True
        Whether a complete selection requests an independently owned result.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.GROFileHandler
        Resulting object in molsysmt.GROFileHandler form.


    Notes
    -----
    Only complete-handler extraction is supported. With copy_if_all=True,
    returns an independently owned resident buffer and parsed entry. False
    explicitly permits returning the original handler. Subsets and output-file
    serialization raise NotImplementedMethodError without changing the source.

    .. versionadded:: 1.0.0
    """

    if output_filename is not None or not (
        is_all(atom_indices) and is_all(structure_indices)
    ):
        raise NotImplementedMethodError(
            caller="molsysmt.form.molsysmt_GROFileHandler.extract"
        )
    if copy_if_all:
        from .copy import copy

        return copy(item, skip_digestion=True)
    return item
