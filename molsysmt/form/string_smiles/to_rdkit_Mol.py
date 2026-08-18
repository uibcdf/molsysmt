from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import FormatError
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('rdkit')
def to_rdkit_Mol(item, atom_indices='all', skip_digestion=False):
    """
    Converting from string:smiles to rdkit.Mol.

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
    rdkit.Mol
        Resulting object in rdkit.Mol form.

    .. versionadded:: 1.0.0
    """

    from rdkit import Chem

    smiles = item[len('smiles:'):] if item.startswith('smiles:') else item

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        raise FormatError(reason=f"Could not parse SMILES string: {smiles!r}",
                          caller='molsysmt.form.string_smiles.to_rdkit_Mol')

    if not is_all(atom_indices):
        from molsysmt.form.rdkit_Mol.extract import extract

        mol = extract(
            mol,
            atom_indices=atom_indices,
            structure_indices='all',
            skip_digestion=True,
        )

    return mol
