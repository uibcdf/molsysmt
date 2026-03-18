from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='biopython.Seq')
@dep_digest('Bio')
def to_file_pir(item, output_filename=None, id='sequence', name='sequence', description='',
                skip_digestion=False):

    if output_filename is None:
        raise ValueError("output_filename is required to write a file:pir.")

    from Bio.SeqRecord import SeqRecord
    from Bio import SeqIO

    record = SeqRecord(item, id=id, name=name, description=description)

    with open(output_filename, 'w') as fff:
        SeqIO.write(record, fff, 'pir')

    return output_filename
