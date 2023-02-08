def is_mdanalysis_coordinates_CRDReader(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'mdanalysis.coordinates.CRDReader')

    return output

