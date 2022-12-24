from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None, digest=True):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item =  to_openmm_Topology(item, box, atom_indices=atom_indices, digest=False)
    tmp_item =  openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates, digest=False)

    return tmp_item

