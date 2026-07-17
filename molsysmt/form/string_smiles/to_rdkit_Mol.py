from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import FormatError
from molsysmt._private.variables import is_all
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('rdkit')
def to_rdkit_Mol(item, atom_indices='all', skip_digestion=False):

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
