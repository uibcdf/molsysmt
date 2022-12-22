def download(pdb_id=None, output_filename=None, tempfile=False, wwPDB_Partner='RCSB PDB', digest=True):

    from molsysmt._private.files_and_directories import temp_filename
    from urllib.request import urlretrieve

    output = None

    if tempfile:
        output_filename=temp_filename(extension="pdb")

    if wwPDB_Partner=='RCSB PDB':

        filename = pdb_id+'.pdb'
        fullurl = 'https://files.rcsb.org/download/'+filename

        if output_filename is None:
            output_filename = filename

        urlretrieve(fullurl, output_filename)

        output = output_filename

    else:

        raise NotImplementedError()

    return output

