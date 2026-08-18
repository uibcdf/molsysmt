from molsysmt._private.argdigest import arg_digest

@arg_digest(form='pdbfixer.PDBFixer')
def to_string_amino_acids_3(item, atom_indices='all', skip_digestion=False):
    """
    Converting from pdbfixer.PDBFixer to string:amino_acids_3.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:amino_acids_3
        Resulting object in string:amino_acids_3 form.


    .. versionadded:: 1.0.0
    """

    from molsysmt.form.openmm_Topology.to_openmm_Topology import to_openmm_Topology

    tmp_item  = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    tmp_item = ''.join([ r.name for r in tmp_item.groups() ])

    return tmp_item

