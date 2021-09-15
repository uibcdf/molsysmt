
def download(pdbid=None, output_filename=None, tempfile=False, wwPDB_Partner='RCSB PDB'):

    from molsysmt._private_tools.files_and_directories import temp_filename
    from urllib.request import urlretrieve

    output = None

    if tempfile:
        output_filename=tmp_filename(extension="pdb")

    if wwPDB_Partner=='RCSB PDB':

        filename = pdbid.capitalize()+'.pdb'
        fullurl = 'https://files.rcsb.org/download/'+filename

        if output_filename is None:
            output_filename = filename

        urlretrieve(fullurl, output_filename)

        output = output_filename

    else:

        raise NotImplementedError()

    return output

