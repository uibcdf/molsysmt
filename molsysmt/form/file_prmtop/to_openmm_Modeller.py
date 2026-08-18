from molsysmt._private.argdigest import arg_digest

@arg_digest(form='file:prmtop')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None, skip_digestion=False):
    """
    Converting from file:prmtop to openmm.Modeller.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    coordinates : object, default=None
        Argument coordinates.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Modeller
        Resulting object in openmm.Modeller form.


    .. versionadded:: 1.0.0
    """

    from .to_openmm_Topology import to_openmm_Topology
    from molsysmt.form.openmm_Topology.to_openmm_Modeller import to_openmm_Modeller as openmm_Topology_to_openmm_Modeller

    tmp_item = to_openmm_Topology(item, skip_digestion=True)
    tmp_item = openmm_Topology_to_openmm_Modeller(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

