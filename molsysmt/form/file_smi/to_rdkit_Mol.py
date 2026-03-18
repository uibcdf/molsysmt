from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:smi')
@dep_digest('rdkit')
def to_rdkit_Mol(item, skip_digestion=False):

    from rdkit import Chem

    supplier = Chem.SmilesMolSupplier(item, delimiter=' ', nameColumn=1, titleLine=False)
    mols = [mol for mol in supplier if mol is not None]

    if len(mols) == 1:
        return mols[0]

    return mols
