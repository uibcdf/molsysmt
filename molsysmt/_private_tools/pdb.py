def download_pdb(pdb_id=None, output_file=None):

    from molsysmt._private_tools.files_and_directories import tmp_filename
    from urllib.request import urlretrieve

    filetype='pdb'
    fullurl = 'https://files.rcsb.org/download/'+pdb_id.capitalize()+'.'+filetype

    if output_file is None:
        output_file=tmp_filename(extension="pdb")

    urlretrieve(fullurl, output_file)
    return output_file


