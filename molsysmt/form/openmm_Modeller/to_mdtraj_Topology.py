from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Modeller to mdtraj.Topology.

    Parameters
    ----------
    item : openmm.Modeller
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    mdtraj.Topology
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_mdtraj_Topology import to_mdtraj_Topology as openmm_Topology_to_mdtraj_Topology

    tmp_item = to_openmm_Topology(item,  atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = openmm_Topology_to_mdtraj_Topology(tmp_item, skip_digestion=True)

    return tmp_item

