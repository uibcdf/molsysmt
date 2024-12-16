from molsysmt._private.digestion import digest

@digest(form='file:cif.gz')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', skip_digestion=False):

    #from mmcif.io.BinaryCifReader import BinaryCifReader
    from bcifreader import BinaryCifReader

    binary_cif_reader = BinaryCifReader()
    containers = binary_cif_reader.deserialize(item)

    if len(containers)>1:
        print('Warning! The PDB ID has more than a DataContainer')

    tmp_item = containers[0]

    return tmp_item
