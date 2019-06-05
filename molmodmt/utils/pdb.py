import tempfile
import urllib.request

from pdbfixer.pdbfixer import proteinResidues, rnaResidues, dnaResidues

def tmp_pdb_filename():

    filename=tempfile.NamedTemporaryFile(suffix=".pdb").name
    return filename


def download_pdb(pdb_id=None, output_file=None):

    filetype='pdb'
    fullurl = 'https://files.rcsb.org/download/'+pdb_id.capitalize()+'.'+filetype

    if output_file is None:
        filename=tmp_filename("pdb")
        urllib.request.urlretrieve(fullurl, filename)
        return filename
    else:
        urllib.request.urlretrieve(fullurl, output_file)
        pass


