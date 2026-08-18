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
        Source item to convert.
    skip_digestion : bool, default=False
        Whether to skip argument validation.

    Returns
    -------
    rdkit.Mol
        Converted molecular system representation.
    """

    from molsysmt.form.rdkit_Mol.extract import extract

    molecule = item.to_rdkit()
    return extract(
        molecule,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
