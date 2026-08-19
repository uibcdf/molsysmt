from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:alphafold_id')
def to_openmm_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):
    """
    Converting from string:alphafold_id to openmm.Topology.


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

    from .to_string_pdb_text import to_string_pdb_text
    from molsysmt.form.string_pdb_text.to_openmm_Topology import to_openmm_Topology as string_pdb_text_to_openmm_Topology

    tmp_item = to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    tmp_item = string_pdb_text_to_openmm_Topology(tmp_item, skip_digestion=True)

    return tmp_item

