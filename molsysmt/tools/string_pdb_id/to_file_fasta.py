from molsysmt.tools.string_pdb_id.is_string_pdb_id import is_string_pdb_id
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_structure_indices

def to_file_fasta(item, atom_indices='all', structure_indices='all', output_filename=None, check=True):

    if check:

        try:
            is_string_pdb_id(item)
        except:
            raise WrongFormError('string:pdb_id')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()


    from molsysmt.tools.file_fasta import extract as extract_file_fasta

    tmp_item = item.split(':')[-1]
    url = 'https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+tmp_item+'&compressionType=uncompressed'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    fasta_txt = response.read().decode('utf-8')
    with open(output_filename,'w') as f:
        f.write(fasta_txt)
    f.close()
    tmp_item = output_filename

    tmp_item = extract_file_fasta(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices,
            output_filename=output_filename, copy_if_all=False, check=False)

    return tmp_item

