def is_MDAnalysis_topology_CRDParser(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'MDAnalysis.topology.CRDParser.CRDParser')

    return output

