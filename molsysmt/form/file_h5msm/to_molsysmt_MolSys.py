from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from file:h5msm to molsysmt.MolSys.

    Parameters
    ----------
    item : file:h5msm
        Source item in file:h5msm form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_MolSys import to_molsysmt_MolSys as molsysmt_H5MSMFileHandler_to_molsysmt_MolSys

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_MolSys(handler, atom_indices=atom_indices,
                                                           structure_indices=structure_indices,
                                                           skip_digestion=True)
    handler.close()

    return tmp_item
