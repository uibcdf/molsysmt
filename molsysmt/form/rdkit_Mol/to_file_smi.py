from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from depdigest import dep_digest

@arg_digest(form='rdkit.Mol')
@dep_digest('rdkit')
def to_file_smi(item, output_filename=None, skip_digestion=False):
    """
    Converting from rdkit.Mol to file:smi.

    Parameters
    ----------
    item : rdkit.Mol
        Source item in rdkit.Mol form.
    output_filename : str or pathlib.Path
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:smi
        Resulting object in file:smi form.

    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.rdkit_Mol.to_file_smi',
                            message='output_filename is required to write a file:smi.')

    from rdkit import Chem

    writer = Chem.SmilesWriter(output_filename, includeHeader=False)
    mols = item if isinstance(item, list) else [item]
    for mol in mols:
        writer.write(mol)
    writer.close()

    return output_filename
