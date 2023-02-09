def is_MDAnalysis_coordinates_CRDReader(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'MDAnalysis.coordinates.CRD.CRDReader')

    return output

