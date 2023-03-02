from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def to_openmm_Modeller(item, atom_indices='all'):

    from molsysmt import pyunitwizard as puw
    from . import to_openmm_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices)
    coordinates = puw.convert(coordinates, to_units='nanometer', to_form='openmm.unit')
    tmp_item = openmm_Modeller(tmp_item, coordinates)

    return tmp_item

def _to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    return to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices)

