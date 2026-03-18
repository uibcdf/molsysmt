from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('rdkit')
def to_string_smiles(item, skip_digestion=False):

    from rdkit import Chem

    canonical = Chem.MolToSmiles(item)

    return 'smiles:' + canonical
