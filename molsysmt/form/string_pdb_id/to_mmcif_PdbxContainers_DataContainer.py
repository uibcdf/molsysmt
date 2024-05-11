from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from mmcif.io.BinaryCifReader import BinaryCifReader


    tmp_item = item.split(':')[-1]
    url = f'https://models.rcsb.org/{tmp_item}.bcif.gz'

    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(url)

    if len(containers)>1:
        print('Warning! The PDB ID has more than a DataContainer')

    tmp_item = containers[0]

    return tmp_item


