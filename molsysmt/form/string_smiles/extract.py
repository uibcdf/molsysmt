from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='string:smiles')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True,
            skip_digestion=False):

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
