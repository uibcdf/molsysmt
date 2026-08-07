from molsysmt._private.argdigest import arg_digest
from depdigest import dep_digest

@arg_digest(form='file:pir')
@dep_digest('Bio')
def to_string_amino_acids_1(item, skip_digestion=False):

    from .to_biopython_SeqRecord import to_biopython_SeqRecord

    tmp_item = to_biopython_SeqRecord(item, skip_digestion=True)

    if isinstance(tmp_item, list):
        return [str(record.seq) for record in tmp_item]

    return str(tmp_item.seq)
