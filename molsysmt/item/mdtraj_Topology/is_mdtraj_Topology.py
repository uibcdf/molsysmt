def is_mdtraj_Topology(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdtraj.core.topology.Topology')

    return output

