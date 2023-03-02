from molsysmt._private.digestion import digest

@digest(form='molsysmt.Topology')
def to_file_pdb(item, coordinates, box, atom_indices='all', output_filename=None):

    from . import to_openmm_Topology
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, box, atom_indices=atom_indices)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates, output_filename=output_filename)

    return tmp_item

def _to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                      coordinates=True)
    box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)

    return to_file_pdb(item, coordinates, box, atom_indices=atom_indices, output_filename=output_filename)

