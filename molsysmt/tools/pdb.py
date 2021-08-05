import tempfile
import urllib.request
import re
from pdbfixer.pdbfixer import proteinResidues, rnaResidues, dnaResidues

def tmp_pdb_filename():

    filename=tempfile.NamedTemporaryFile(suffix=".pdb").name
    return filename


def download_pdb(pdb_id=None, output_filepath=None):

    filetype='pdb'
    fullurl = 'https://files.rcsb.org/download/'+pdb_id.capitalize()+'.'+filetype

    if output_file is None:
        filename=tmp_pdb_filename()
        urllib.request.urlretrieve(fullurl, filename)
        return filename
    else:
        urllib.request.urlretrieve(fullurl, output_filepath)
        pass

def replace_HETATM_from_capping_atoms(item):

    from molsysmt import get_form

    form_in = get_form(item)

    if form_in == 'string:pdb':

        tmp_item = re.sub(r'HETATM+(\s+\d+\s+\w+\s+(ACE||NME)+\s+\w+\s)', r'ATOM  \1', item)

    elif form_in == 'file:pdb':

        with open(item, 'r+') as f:
            text = f.read()
            out = re.sub(r'HETATM+(\s+\d+\s+\w+\s+(ACE||NME)+\s+\w+\s)', r'ATOM  \1', text)
            f.seek(0)
            f.write(out)
            f.truncate()

        tmp_item=item

    return tmp_item

