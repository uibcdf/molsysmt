from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:smi')
@dep_digest('rdkit')
def to_rdkit_Mol(item, atom_indices='all', skip_digestion=False):

    from rdkit import Chem
    from molsysmt._private.smonitor import FormatError
    from molsysmt._private.variables import is_all

    molecules = []
    with open(item, encoding='utf-8') as file:
        for line_number, line in enumerate(file, start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            fields = stripped.split(maxsplit=1)
            molecule = Chem.MolFromSmiles(fields[0])
            if molecule is None:
                raise FormatError(
                    reason=(
                        f'Could not parse the SMILES record at line {line_number} '
                        f'of {item!r}.'
                    ),
                    caller='molsysmt.form.file_smi.to_rdkit_Mol',
                )
            if len(fields) == 2:
                molecule.SetProp('_Name', fields[1])
                for atom in molecule.GetAtoms():
                    atom.SetProp('_MolSysMTSMILESRecordName', fields[1])
            molecules.append(molecule)

    if not molecules:
        raise FormatError(
            reason=f'The SMILES file {item!r} contains no molecule records.',
            caller='molsysmt.form.file_smi.to_rdkit_Mol',
        )

    output = molecules[0]
    for molecule in molecules[1:]:
        output = Chem.CombineMols(output, molecule)

    if not is_all(atom_indices):
        from molsysmt.form.rdkit_Mol.extract import extract

        output = extract(
            output,
            atom_indices=atom_indices,
            structure_indices='all',
            skip_digestion=True,
        )

    return output
