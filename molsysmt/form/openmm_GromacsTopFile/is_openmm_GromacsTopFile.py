
def is_openmm_GromacsTopFile(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'openmm.GromacsTopFile')

    return output

