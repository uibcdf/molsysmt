from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from openmm.Modeller to molsysmt.Topology.

    Parameters
    ----------
    item : openmm.Modeller
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    molsysmt.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Topology.to_molsysmt_Topology import to_molsysmt_Topology as openmm_Topology_to_molsysmt_Topology

    tmp_item = item.getTopology()
    tmp_item = openmm_Topology_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

