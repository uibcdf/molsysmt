from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to parmed.Structure.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    parmed.Structure
        Resulting object in parmed.Structure form.


    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_parmed_Structure import to_parmed_Structure as molsysmt_Topology_to_parmed_Structure

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_parmed_Structure(tmp_item, skip_digestion=True)
    return tmp_item

