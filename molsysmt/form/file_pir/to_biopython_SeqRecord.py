from molsysmt._private.arg_digestion import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_biopython_SeqRecord(item, skip_digestion=False):

    from Bio import SeqIO

    records = list(SeqIO.parse(item, 'pir'))

    if len(records) == 1:
        return records[0]

    return records
