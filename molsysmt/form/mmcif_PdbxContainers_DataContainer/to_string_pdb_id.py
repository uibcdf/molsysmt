from molsysmt._private.digestion import digest

@digest(form='mmcif.PdbxContainers.DataContainer')
def to_string_pdb_id(item, skip_digestion=False):

    return item.getObj('entry').getValue('id')

