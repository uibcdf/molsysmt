from molsysmt._private.digestion import digest
from os import remove

@digest(form='string:pdb_id')
def to_bcifreader_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from bcifreader import BinaryCifReader
    from ..file_bcif_gz import download

    if item.startswith('pdb_id:'):
        tmp_item = item.split(':')[-1]
    elif item.startswith('pdb_'):
        tmp_item = item[-4:]
    else:
        tmp_item = item

    tempfile = download(tmp_item, tempfile=True)
    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(tempfile)

    #url = f'https://models.rcsb.org/{tmp_item}.bcif.gz'
    #binary_cif_reader = BinaryCifReader()
    #containers = binary_cif_reader.deserialize(url)

    if len(containers)>1:
        print('Warning! The PDB ID has more than a DataContainer')

    if len(containers)==0:
        raise ValueError('The PDB ID does not have any DataContainer')

    tmp_item = containers[0]

    remove(tempfile)

    return tmp_item


