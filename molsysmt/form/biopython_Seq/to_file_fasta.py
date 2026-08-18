from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from depdigest import dep_digest

@arg_digest(form='biopython.Seq')
@dep_digest('Bio')
def to_file_fasta(item, output_filename=None, id='sequence', name='sequence', description='',
                  skip_digestion=False):
    """
    Converting from biopython.Seq to file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    id : object, default='sequence'
        Argument id.
    name : object, default='sequence'
        Argument name.
    description : object, default=''
        Argument description.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:fasta
        Resulting object in file:fasta form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.biopython_Seq.to_file_fasta',
                            message='output_filename is required to write a file:fasta.')

    from Bio.SeqRecord import SeqRecord
    from Bio import SeqIO

    record = SeqRecord(item, id=id, name=name, description=description)

    with open(output_filename, 'w') as fff:
        SeqIO.write(record, fff, 'fasta')

    return output_filename
