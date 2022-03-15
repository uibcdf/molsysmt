
def is_biopython_SeqRecord(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'biopython.SeqRecord')

    return output

