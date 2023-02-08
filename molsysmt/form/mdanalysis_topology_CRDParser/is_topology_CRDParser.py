def is_mdanalysis_topology_CRDParser(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdanalysis.topology.CRDParser')

    return output

