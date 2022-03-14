
def is_pdbfixer_PDBFixer(item):

    item_fullname = item.__class__.__module__+'.'+item.__class__.__name__
    output = (item_fullname == 'pdbfixer.pdbfixer.PDBFixer')

    return output

