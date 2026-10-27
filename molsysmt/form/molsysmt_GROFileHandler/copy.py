from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@arg_digest(form="molsysmt.GROFileHandler")
def copy(item, output_filename=None, skip_digestion=False):
    """
    Creating a copy of an item of form molsysmt.GROFileHandler.


    Parameters
    ----------
    item : molecular system
        Source object or file in the form named by this adapter.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.GROFileHandler
        Resulting object in molsysmt.GROFileHandler form.


    Notes
    -----
    Copies the complete resident StringIO buffer and parsed entry independently.
    Source cursor and mutable arrays are preserved, and closing the result does
    not close the source. Output-file serialization is not implemented and
    rejects an explicit output_filename before writing anything.

    .. versionadded:: 1.0.0
    """

    if output_filename is not None:
        raise NotImplementedMethodError(
            caller="molsysmt.form.molsysmt_GROFileHandler.copy"
        )
    from copy import deepcopy

    return deepcopy(item)
