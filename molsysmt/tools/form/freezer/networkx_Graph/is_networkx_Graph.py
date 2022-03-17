_item_fullname_='networkx.Graph'

def is_networkx_Graph(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

