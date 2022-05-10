from molsysmt._private.digestion import digest_item, digest_atom_indices, digest_structure_indices

def to_file_mmtf(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        digest_item(item, 'mmtf.MMTFDecoder')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    from . import extract
    from mmtf.api.default_api import write_mmtf, MMTFDecoder

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False, check=False)
    write_mmtf(output_filename, tmp_item, MMTFDecoder.pass_data_on)
    tmp_item = output_filename

    return tmp_item

