from molsysmt._private.argdigest import arg_digest


@arg_digest(form="file:gro")
def to_molsysmt_Topology(
    item,
    atom_indices="all",
    structure_indices="all",
    get_missing_bonds=True,
    skip_digestion=False,
):
    """
    Converting from file:gro to molsysmt.Topology.

    Infer candidate bonds from the complete first structure before selection.
    This does not certify complete chemistry. The converter closes the file
    handler it creates, including when conversion fails.


    Parameters
    ----------
    item : molecular system
        Path to a GRO file declaring atom/group labels, coordinates and box data.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source atom indices to retain after full-system connectivity inference.
        Defaults to 'all'.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Source structure indices to retain. Defaults to 'all'. Connectivity is
        inferred using the first structure before this selection.
    get_missing_bonds : bool, default=True
        Whether to infer candidate bonds using the existing native template and
        distance rules. GRO declares no bonds. Defaults to True.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.


    Examples
    --------
    >>> import molsysmt as msm
    >>> topology = msm.convert(msm.systems['nglview']['md_1u19.gro'],
    ...                        to_form='molsysmt.Topology', selection=[0, 1])
    >>> topology.n_atoms
    2

    .. admonition:: User guide

       See :ref:`user-foundations-native-world-file-handlers-molsysmt-grofilehandler`
       for connectivity and coordinate-reading limits.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.molsysmt_GROFileHandler.to_molsysmt_Topology import (
        to_molsysmt_Topology as molsysmt_GROFileHandler_to_molsysmt_Topology,
    )

    from .to_molsysmt_GROFileHandler import to_molsysmt_GROFileHandler

    tmp_item = to_molsysmt_GROFileHandler(item)
    try:
        return molsysmt_GROFileHandler_to_molsysmt_Topology(
            tmp_item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            get_missing_bonds=get_missing_bonds,
            skip_digestion=True,
        )
    finally:
        tmp_item.close()
