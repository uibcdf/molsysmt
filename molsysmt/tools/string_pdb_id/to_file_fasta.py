def to_file_fasta(item, atom_indices='all', structure_indices='all', output_filename=None, check_form=True):

    if check_form:
        from molsysmt.tools.string_pdb_id.is_string_pdb_id import _checking_form
        _checking_form(item, check_form=check_form)

    if output_filename is None:
        raise ValueError

    from molsysmt.api_forms.api_file_fasta import to_file_fasta as file_fasta_to_file_fasta

    tmp_item = item.split(':')[-1]
    url = 'https://www.rcsb.org/pdb/download/downloadFastaFiles.do?structureIdList='+tmp_item+'&compressionType=uncompressed'
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    fasta_txt = response.read().decode('utf-8')
    with open(output_filename,'w') as f:
        f.write(fasta_txt)
    f.close()
    tmp_item = output_filename
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None
    tmp_item, tmp_molecular_system= file_fasta_to_file_fasta(tmp_item, molecular_system=tmp_molecular_items, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, copy_if_all=False)

    return tmp_item

