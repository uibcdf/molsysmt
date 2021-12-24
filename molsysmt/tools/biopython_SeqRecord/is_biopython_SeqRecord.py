def is_biopython_SeqRecord(item):

    try:
        output = (item.__class__.__name__=='SeqRecord') and (item.__class__.__module__=='Bio.SeqRecord')
    except:
        output = False

    return output

