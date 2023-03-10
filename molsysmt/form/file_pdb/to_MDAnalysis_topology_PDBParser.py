from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='file:pdb')
def to_MDAnalysis_topology_PDBParser(item, atom_indices='all'):

    try:
        from MDAnalysis.topology import PDBParser
    except:
        raise LibraryNotFoundError('MDAnalysis')

    tmp_item = PDBParser.PDBParser(item)

    return tmp_item

