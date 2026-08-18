from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from depdigest import dep_digest

@arg_digest(form='biopython.SeqRecord')
@dep_digest('Bio')
def to_file_fasta(item, output_filename=None, skip_digestion=False):
    """
    Converting from biopython.SeqRecord to file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:fasta
        Resulting object in file:fasta form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.biopython_SeqRecord.to_file_fasta',
                            message='output_filename is required to write a file:fasta.')

    from Bio import SeqIO

    records = item if isinstance(item, list) else [item]

    with open(output_filename, 'w') as fff:
        SeqIO.write(records, fff, 'fasta')

    return output_filename
