from molsysmt._private.argdigest import arg_digest

@arg_digest(form='molsysmt.Topology')
def to_parmed_Structure(item, atom_indices='all', skip_digestion=False):
    """
    Converting from molsysmt.Topology to parmed.Structure.

    Parameters
    ----------
    item : molsysmt.Topology
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    parmed.Structure
        Converted molecular system representation.
    """

    from molsysmt.form.molsysmt_Topology.to_openmm_Topology import to_openmm_Topology as molsysmt_Topology_to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_parmed_Structure import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item = molsysmt_Topology_to_openmm_Topology(item, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

