from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None, box=None):

    from . import extract
    from molsysmt import pyunitwizard as puw
    from openmm.app import Modeller

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)
    positions = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    tmp_item = Modeller(tmp_item, positions)

    return tmp_item

def _to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.basic import get

    coordinates = get(molecular_system, element='atom', indices=atom_indices, structure_indices=structure_indices,
                      coordinates=True)

    return to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates)

