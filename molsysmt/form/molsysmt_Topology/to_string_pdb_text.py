from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_string_pdb_text(item, atom_indices='all', coordinates=None, box=None):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_string_pdb_text as openmm_Topology_to_string_pdb_text

    tmp_item =  to_openmm_Topology(item, box, atom_indices=atom_indices)
    tmp_item =  openmm_Topology_to_string_pdb_text(tmp_item, coordinates=coordinates)

    return tmp_item

def _to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

    return to_string_pdb_text(item, coordinates=coordinates, box=box, atom_indices=atom_indices)


