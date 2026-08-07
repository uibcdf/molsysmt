from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:fasta')
@dep_digest('Bio')
def to_biopython_SeqRecord(item, skip_digestion=False):

    from Bio import SeqIO

    records = list(SeqIO.parse(item, 'fasta'))

    if len(records) == 1:
        return records[0]

    return records
