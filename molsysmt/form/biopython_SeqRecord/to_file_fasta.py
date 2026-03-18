from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='biopython.SeqRecord')
@dep_digest('Bio')
def to_file_fasta(item, output_filename=None, skip_digestion=False):

    if output_filename is None:
        raise ValueError("output_filename is required to write a file:fasta.")

    from Bio import SeqIO

    records = item if isinstance(item, list) else [item]

    with open(output_filename, 'w') as fff:
        SeqIO.write(records, fff, 'fasta')

    return output_filename
