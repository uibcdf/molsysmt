_item_fullname_='Bio.Seq.Seq'

def is_biopython_Seq(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

