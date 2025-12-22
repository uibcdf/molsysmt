from molsysmt._private.digestion import digest
from molsysmt._private.files_and_directories import temp_filename
from os import remove

@digest(form='string:pdb_id')
def to_mmcif_PdbxContainers_DataContainer(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    try:

        print('1')

        from .to_file_bcif_gz import to_file_bcif_gz
        from ..file_bcif_gz import to_mmcif_PdbxContainers_DataContainer as file_bcif_gz_to_mmcif_PdbxContainers_DataContainer
        output_filename = temp_filename(extension="bcif.gz")
        tmp_item = to_file_bcif_gz(item, output_filename=output_filename, skip_digestion=True)
        tmp_item = file_bcif_gz_to_mmcif_PdbxContainers_DataContainer(tmp_item, skip_digestion=True)
        remove(output_filename)

    except:

        try:

            print('2')

            from .to_file_bcif import to_file_bcif
            from ..file_bcif import to_mmcif_PdbxContainers_DataContainer as file_bcif_to_mmcif_PdbxContainers_DataContainer
            output_filename = temp_filename(extension="bcif")
            tmp_item = to_file_bcif(item, output_filename=output_filename, skip_digestion=True)
            tmp_item = file_bcif_to_mmcif_PdbxContainers_DataContainer(tmp_item, skip_digestion=True)
            remove(output_filename)

        except:

            try:

                print('3')

                from .to_file_cif_gz import to_file_cif_gz
                from ..file_cif_gz import to_mmcif_PdbxContainers_DataContainer as file_cif_gz_to_mmcif_PdbxContainers_DataContainer
                output_filename = temp_filename(extension="cif_gz")
                tmp_item = to_file_cif_gz(item, output_filename=output_filename, skip_digestion=True)
                tmp_item = file_cif_gz_to_mmcif_PdbxContainers_DataContainer(tmp_item, skip_digestion=True)
                remove(output_filename)

            except:

                try:

                    print('4')

                    from .to_file_cif import to_file_cif
                    from ..file_cif import to_mmcif_PdbxContainers_DataContainer as file_cif_to_mmcif_PdbxContainers_DataContainer
                    output_filename = temp_filename(extension="cif")
                    tmp_item = to_file_cif(item, output_filename=output_filename, skip_digestion=True)
                    tmp_item = file_cif_to_mmcif_PdbxContainers_DataContainer(tmp_item, skip_digestion=True)
                    remove(output_filename)

                except:

                    raise ImportError("PDB ID can not be convert to mmcif_PdbxContainers_DataContainer")

    return tmp_item

