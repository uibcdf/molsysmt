from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('rdkit')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):
    """
    Converting from string:smiles to molsysmt.Topology.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
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

    from .to_rdkit_Mol import to_rdkit_Mol
    from molsysmt.form.rdkit_Mol.to_molsysmt_Topology import to_molsysmt_Topology as rdkit_to_topology

    tmp_item = to_rdkit_Mol(item, skip_digestion=True)

    return rdkit_to_topology(
        tmp_item,
        atom_indices=atom_indices,
        skip_digestion=True,
    )
