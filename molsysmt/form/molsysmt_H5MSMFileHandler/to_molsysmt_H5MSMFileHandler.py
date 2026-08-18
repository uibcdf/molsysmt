import os
from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_H5MSMFileHandler(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):
    """
    Converting from molsysmt.H5MSMFileHandler to molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.H5MSMFileHandler
        Converted molecular system representation.
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
