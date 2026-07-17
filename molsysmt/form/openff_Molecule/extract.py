from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='openff.Molecule')
@dep_digest('rdkit')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):

    from openff.toolkit import Molecule
    from .to_rdkit_Mol import to_rdkit_Mol

    rdkit_molecule = to_rdkit_Mol(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return Molecule.from_rdkit(rdkit_molecule, allow_undefined_stereo=True)
