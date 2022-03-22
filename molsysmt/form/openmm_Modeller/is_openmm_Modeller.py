
def is_openmm_Modeller(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.Modeller')

    return output

