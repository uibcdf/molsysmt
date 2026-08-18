from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:smiles')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):
    """
    Extracting a subset of elements or structures from form string:smiles.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    string:smiles
        Resulting object in string:smiles form.


    .. versionadded:: 1.0.0
    """

    if is_all(atom_indices) and is_all(structure_indices):
        from copy import copy
        return copy(item)

    if not is_all(structure_indices):
        from molsysmt._private.smonitor import NotCompatibleConversionError

        raise NotCompatibleConversionError(
            'string:smiles',
            'string:smiles',
            {'structure_indices'},
            caller='molsysmt.form.string_smiles.extract',
            message='SMILES does not contain molecular structures.',
        )

    from .to_rdkit_Mol import to_rdkit_Mol
    from molsysmt.form.rdkit_Mol.extract import extract as extract_rdkit
    from molsysmt.form.rdkit_Mol.to_string_smiles import to_string_smiles

    molecule = to_rdkit_Mol(item, skip_digestion=True)
    molecule = extract_rdkit(
        molecule,
        atom_indices=atom_indices,
        structure_indices='all',
        skip_digestion=True,
    )
    return to_string_smiles(molecule, skip_digestion=True)
