from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:h5msm')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:h5msm to molsysmt.Topology.

    Parameters
    ----------
    item : file:h5msm
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_H5MSMFileHandler_to_molsysmt_Topology

    handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    tmp_item = molsysmt_H5MSMFileHandler_to_molsysmt_Topology(handler, atom_indices=atom_indices, skip_digestion=True)
    handler.close()

    return tmp_item
