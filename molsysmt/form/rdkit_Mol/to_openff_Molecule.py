from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('openff.toolkit')
def to_openff_Molecule(item, skip_digestion=False):

    from openff.toolkit.topology import Molecule

    return Molecule.from_rdkit(item)
