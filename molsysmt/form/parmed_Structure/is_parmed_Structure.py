
def is_parmed_Structure(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'parmed.structure.Structure')

    return output

