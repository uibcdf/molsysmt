from molsysmt._private.argdigest import arg_digest

@arg_digest(form='mmcif.PdbxContainers.DataContainer')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if isinstance(item, str):
        from mmcif.io.PdbxReader import PdbxReader
        import gzip
        
        if item.endswith('.gz'):
            with gzip.open(item, 'rt') as f:
                reader = PdbxReader(f)
                data = []
                reader.read(data)
                tmp_item = data[0]
        else:
            with open(item, 'r') as f:
                reader = PdbxReader(f)
                data = []
                reader.read(data)
                tmp_item = data[0]
    else:
        tmp_item = item

    from molsysmt._private.variables import is_all
    if not (is_all(atom_indices) and is_all(structure_indices)):
        from .extract import extract
        tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, 
                           copy_if_all=copy_if_all, skip_digestion=True)

    return tmp_item
