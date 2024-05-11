def download(pdb_id=None, output_filename=None, tempfile=False, wwPDB_Partner='RCSB PDB', skip_digestion=False):

    from molsysmt._private.files_and_directories import temp_filename
    from urllib.request import urlretrieve

    output = None

    if tempfile:
        output_filename=temp_filename(extension="bcif")

    if wwPDB_Partner=='RCSB PDB':

        filename = pdb_id+'.bcif'
        fullurl = 'https://models.rcsb.org/'+filename

        if output_filename is None:
            output_filename = filename

        urlretrieve(fullurl, output_filename)

        output = output_filename

    else:

        raise NotImplementedError()

    return output

