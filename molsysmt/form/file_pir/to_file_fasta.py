from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import ArgumentError
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_file_fasta(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.file_pir.to_file_fasta',
                            message='output_filename is required to write a file:fasta.')

    from Bio import SeqIO

    records = list(SeqIO.parse(item, 'pir'))

    with open(output_filename, 'w') as fff:
        SeqIO.write(records, fff, 'fasta')

    return output_filename
