from molsysmt._private.digestion import digest_item, digest_atom_indices
from molsysmt._private.digestion import digest_coordinates, digest_box

def to_openmm_Modeller(item, atom_indices='all', coordinates=None, box=None):

    if check:

        digest_item(item, 'openmm.Topology')
        atom_indices = digest_atom_indices(atom_indices)
        coordinates = digest_coordinates(coordinates)
        box = digest_box(box)

    from . import extract
    from molsysmt import puw
    from openmm.app import Modeller

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False)
    positions = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    tmp_item = Modeller(tmp_item, positions)

    return tmp_item

