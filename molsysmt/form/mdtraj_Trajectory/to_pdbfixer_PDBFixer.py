from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mdtraj.Trajectory')
def to_pdbfixer_PDBFixer(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from mdtraj.Trajectory to pdbfixer.PDBFixer.

    Parameters
    ----------
    item : mdtraj.Trajectory
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    pdbfixer.PDBFixer
        Converted molecular system representation.
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt.form.openmm_Topology.to_pdbfixer_PDBFixer import to_pdbfixer_PDBFixer as openmm_Topology_to_pdbfixer_PDBFixer

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)
    tmp_item = openmm_Topology_to_pdbfixer_PDBFixer(tmp_item, coordinates=coordinates, skip_digestion=True)

    return tmp_item

