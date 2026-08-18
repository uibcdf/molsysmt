from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openff.Molecule')
@dep_digest('rdkit')
def to_rdkit_Mol(
    item, atom_indices='all', structure_indices='all', skip_digestion=False
):
    """
    Converting from openff.Molecule to rdkit.Mol.

    Parameters
    ----------
    item : openff.Molecule
        Source item in openff.Molecule form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    rdkit.Mol
        Resulting object in rdkit.Mol form.

    .. versionadded:: 1.0.0
    """

    from molsysmt.form.rdkit_Mol.extract import extract

    molecule = item.to_rdkit()
    return extract(
        molecule,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
