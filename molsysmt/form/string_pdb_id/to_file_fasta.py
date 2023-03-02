from molsysmt._private.digestion import digest

@digest(form='string:pdb_id')
def to_file_fasta(item, atom_indices='all', output_filename=None):

    from ..file_fasta import extract as extract_file_fasta

    tmp_item = item.split(':')[-1]
    url = 'https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+tmp_item+'&compressionType=uncompressed'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    fasta_txt = response.read().decode('utf-8')
    with open(output_filename,'w') as f:
        f.write(fasta_txt)
    f.close()
    tmp_item = output_filename

    tmp_item = extract_file_fasta(tmp_item, atom_indices=atom_indices,
            output_filename=output_filename, copy_if_all=False)

    return tmp_item

def _to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from sabueso.tools.string_pdb_id import to_file_fasta as string_pdb_id_to_file_fasta
    from sabueso.tools.file_fasta import extract as extract_file_fasta
    from sabueso.basic import get
    import numpy as np

    tmp_item = string_pdb_id_to_file_fasta(item)
    group_indices = get(molecular_system, element='atom', indices=atom_indices, group_index=True)
    group_indices = np.unique(group_indices)
    return extract_file_fasta(tmp_item, group_indices=group_indices, output_filename=output_filename, copy_if_all=False)

