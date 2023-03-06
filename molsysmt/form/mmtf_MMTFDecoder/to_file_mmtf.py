from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder')
def to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None):

    from . import extract
    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False)
    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)
    tmp_item = output_filename

    return tmp_item

def _to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None):

    return to_file_mmtf(item, atom_indices=atom_indices, structure_indices=structure_indices,
                        output_filename=output_filename)


