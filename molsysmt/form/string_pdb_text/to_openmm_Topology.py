from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:pdb_text')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:pdb_text to openmm.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openmm.Topology
        Resulting object in openmm.Topology form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_PDBFile.to_openmm_PDBFile import to_openmm_PDBFile
    from molsysmt.form.openmm_PDBFile.to_openmm_Topology import to_openmm_Topology as openmm_PDBFile_to_openmm_Topology

    tmp_item = to_openmm_PDBFile(item, skip_digestion=True)
    tmp_item = openmm_PDBFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices,
                                                 structure_indices=structure_indices, skip_digestion=True)

    return tmp_item

