from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='openff.Molecule')
@dep_digest('rdkit')
def to_rdkit_Mol(item, skip_digestion=False):

    return item.to_rdkit()
