from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.MolSys')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.MolSys to parmed.Structure.

    Parameters
    ----------
    item : molsysmt.MolSys
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.Structure
        Converted molecular system representation.
    """

    from .to_molsysmt_Topology import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology.to_parmed_Structure import to_parmed_Structure as molsysmt_Topology_to_parmed_Structure

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = molsysmt_Topology_to_parmed_Structure(tmp_item, skip_digestion=True)
    return tmp_item

