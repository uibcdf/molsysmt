from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='openff.Molecule')
@dep_digest('rdkit')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of elements or structures from form openff.Molecule.

    Parameters
    ----------
    item : openff.Molecule
        Source item in openff.Molecule form.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    copy_if_all : object
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    openff.Molecule
        Resulting object in openff.Molecule form.

    .. versionadded:: 1.0.0
    """

    from openff.toolkit import Molecule
    from .to_rdkit_Mol import to_rdkit_Mol

    rdkit_molecule = to_rdkit_Mol(
        item,
        atom_indices=atom_indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    return Molecule.from_rdkit(rdkit_molecule, allow_undefined_stereo=True)
