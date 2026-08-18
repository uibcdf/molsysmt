from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:mol2')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from file:mol2 to molsysmt.Topology.

    Parameters
    ----------
    item : file:mol2
        Source item in file:mol2 form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(tmp_item, skip_digestion=True)

    return tmp_item

