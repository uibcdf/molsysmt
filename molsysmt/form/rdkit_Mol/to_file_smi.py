from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('rdkit')
def to_file_smi(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        raise ValueError("output_filename is required to write a file:smi.")

    from rdkit import Chem

    writer = Chem.SmilesWriter(output_filename, includeHeader=False)
    mols = item if isinstance(item, list) else [item]
    for mol in mols:
        writer.write(mol)
    writer.close()

    return output_filename
