from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_mdanalysis_topology_PDBParser(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:pdb')
        atom_indices = digest_atom_indices(atom_indices)

    try:
        from MDAnalysis.topology import PDBParser
    except:
        raise LibraryNotFoundError('MDAnalysis')

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

