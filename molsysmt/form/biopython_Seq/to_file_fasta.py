from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from depdigest import dep_digest

@arg_digest(form='biopython.Seq')
@dep_digest('Bio')
def to_file_fasta(item, output_filename=None, id='sequence', name='sequence', description='',
                  skip_digestion=False):

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.biopython_Seq.to_file_fasta',
                            message='output_filename is required to write a file:fasta.')

    from Bio.SeqRecord import SeqRecord
    from Bio import SeqIO

    record = SeqRecord(item, id=id, name=name, description=description)

    with open(output_filename, 'w') as fff:
        SeqIO.write(record, fff, 'fasta')

    return output_filename
