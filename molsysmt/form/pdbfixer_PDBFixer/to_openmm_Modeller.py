from molsysmt._private.digestion import digest

@digest(form='pdbfixer.PDBFixer')
def to_openmm_Modeller(item, atom_indices='all', skip_digestion=False):

    from molsysmt import pyunitwizard as puw
    from . import to_openmm_Topology

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, skip_digestion=True)
    coordinates = get_coordinates_from_atom(tmp_item, indices=atom_indices, skip_digestion=True)
    coordinates = puw.convert(coordinates, to_units='nanometer', to_form='openmm.unit')
    tmp_item = openmm_Modeller(tmp_item, coordinates)

    return tmp_item

