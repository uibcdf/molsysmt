from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError
from depdigest import dep_digest

@arg_digest(form='biopython.SeqRecord')
@dep_digest('Bio')
def to_file_pir(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        raise ArgumentError(argument='output_filename', caller='molsysmt.form.biopython_SeqRecord.to_file_pir',
                            message='output_filename is required to write a file:pir.')

    from Bio import SeqIO

    records = item if isinstance(item, list) else [item]

    with open(output_filename, 'w') as fff:
        SeqIO.write(records, fff, 'pir')

    return output_filename
