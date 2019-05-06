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

def atoms_list2string(atoms_list):

    return ",".join([str(ii) for ii in atoms_list])

def strings_list2string(atoms_list):

    return ",".join([str(ii) for ii in atoms_list])

def atoms_list2AmberMask(atoms_list,num_atoms,inverse=False):

    from numpy import zeros as _zeros
    tmp_mask = _zeros(num_atoms,dtype=int)
    tmp_mask[atoms_list]=1
    if inverse:
        tmp_mask=1-tmp_mask
    return list(tmp_mask)

