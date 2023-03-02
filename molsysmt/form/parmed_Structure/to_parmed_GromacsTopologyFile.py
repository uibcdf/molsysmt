from molsysmt._private.digestion import digest

@digest(form='parmed.Structure')
def to_parmed_GromacsTopologyFile(item, atom_indices='all'):

    from . import extract
    from parmed.gromacs import GromacsTopologyFile as GromacsTopologyFile

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)
    tmp_item = GromacsTopologyFile.from_structure(tmp_item)

    return tmp_item

def _to_parmed_GromacsTopologyFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_parmed_GromacsTopologyFile(item, atom_indices=atom_indices)

