import os
import tempfile
import urllib.request

from pdbfixer.pdbfixer import proteinResidues, rnaResidues, dnaResidues

def download_pdb(pdb_id=None, output_file=None):

    filetype='pdb'
    fullurl = 'https://files.rcsb.org/download/'+pdb_id.capitalize()+'.'+filetype

    # Esto lo haría mejor PyPDB, pero tengo que ponerlo en conda (https://github.com/williamgilpin/pypdb/)

    if output_file is None:
        filename=tempfile.NamedTemporaryFile(suffix=".pdb").name
        urllib.request.urlretrieve(fullurl, filename)
        return filename
    else:
        urllib.request.urlretrieve(fullurl, output_file)
        pass
