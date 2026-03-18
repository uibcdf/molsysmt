from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('rdkit')
def to_rdkit_Mol(item, skip_digestion=False):

    from rdkit import Chem

    smiles = item[len('smiles:'):] if item.startswith('smiles:') else item

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        raise ValueError(f"Could not parse SMILES string: {smiles!r}")

    return mol
