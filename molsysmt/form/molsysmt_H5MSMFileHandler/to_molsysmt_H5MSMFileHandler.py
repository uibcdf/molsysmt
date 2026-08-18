import os
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_H5MSMFileHandler(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.H5MSMFileHandler to molsysmt.H5MSMFileHandler.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Resulting object in molsysmt.H5MSMFileHandler form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.native.h5msm_file_handler import H5MSMFileHandler
    from molsysmt._private.variables import is_all

    if isinstance(item, (str, os.PathLike)):
        tmp_item = H5MSMFileHandler(str(item))
    else:
        tmp_item = item

    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, 
                           copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item
