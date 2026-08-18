from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openmm.Modeller')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from openmm.Modeller to openmm.Topology.

    Parameters
    ----------
    item : openmm.Modeller
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    openmm.Topology
        Converted molecular system representation.
    """

    from ..openmm_Topology.extract import extract as extract_openmm_Topology

    tmp_item = item.getTopology()
    tmp_item = extract_openmm_Topology(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
                                       skip_digestion=True)

    return tmp_item


