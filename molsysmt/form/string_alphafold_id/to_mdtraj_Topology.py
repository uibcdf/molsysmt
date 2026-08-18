from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:alphafold_id to mdtraj.Topology.

    Parameters
    ----------
    item : string:alphafold_id
        Source item in string:alphafold_id form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    mdtraj.Topology
        Resulting object in mdtraj.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_molsysmt_MolSys import to_molsysmt_MolSys
    from molsysmt.form.molsysmt_MolSys.to_mdtraj_Topology import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    tmp_item = molsysmt_MolSys_to_mdtraj_Topology(tmp_item, atom_indices=atom_indices,
            structure_indices=structure_indices, skip_digestion=True)

    return tmp_item


