import os
import tempfile
import urllib.request

from pdbfixer.pdbfixer import proteinResidues, rnaResidues, dnaResidues

def tmp_filename(extension=None):

    if not extension.startswith("."):
        extension="."+extension

    filename=tempfile.NamedTemporaryFile(suffix=extension).name
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

def atom_indices2string(atom_indices):

    return ",".join([str(ii) for ii in atom_indices])

def strings_list2string(atom_indices):

    return ",".join([str(ii) for ii in atom_indices])

def atom_indices2AmberMask(atom_indices,num_atoms,inverse=False):

    from numpy import zeros as _zeros
    tmp_mask = _zeros(num_atoms,dtype=int)
    tmp_mask[atom_indices]=1
    if inverse:
        tmp_mask=1-tmp_mask
    return list(tmp_mask)

