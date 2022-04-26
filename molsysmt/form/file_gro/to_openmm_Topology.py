from molsysmt._private.digestion import digest_item, digest_atom_indices

def to_openmm_Topology(item, atom_indices='all', check=True):

    if check:

        digest_item(item, 'file:gro')
        atom_indices = digest_atom_indices(atom_indices)

    from . import to_openmm_GromacsGroFile
    from ..openmm_GromacsGroFile import to_openmm_Topology as openmm_GromacsGroFile_to_openmm_Topology

    tmp_item = to_openmm_GromacsGroFile(item, check=False)
    tmp_item = openmm_GromacsGroFile_to_openmm_Topology(tmp_item, atom_indices=atom_indices, check=False)

    return tmp_item

