from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='string:smiles')
@dep_digest('openff.toolkit')
def to_openff_Molecule(item, skip_digestion=False):

    from openff.toolkit.topology import Molecule

    smiles = item[len('smiles:'):] if item.startswith('smiles:') else item
    return Molecule.from_smiles(smiles)
