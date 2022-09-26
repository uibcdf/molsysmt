def is_networkx_Graph(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'networkx.Graph')

    return output

