from molsysmt._private.argdigest import arg_digest

@arg_digest(form='string:uniprot_id')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from string:uniprot_id to molsysmt.Topology.

    Parameters
    ----------
    item : string:uniprot_id
        Source item in string:uniprot_id form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Topology
        Resulting object in molsysmt.Topology form.

    .. versionadded:: 1.0.0
    """

    from .to_file_fasta import to_file_fasta
    from molsysmt.form.file_fasta.to_molsysmt_Topology import to_molsysmt_Topology as file_fasta_to_molsysmt_Topology

    tmp_item = to_file_fasta(item, skip_digestion=True)
    tmp_item = file_fasta_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item
