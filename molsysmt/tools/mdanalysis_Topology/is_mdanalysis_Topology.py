_item_fullname_='MDAnalysis.core.topology.Topology'

def is_mdanalysis_Topology(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__

    return _item_fullname_==item_fullname

