from molsysmt._private.digestion import digest

@digest(form='openmm.Topology')
def to_openmm_Modeller(item, atom_indices='all', coordinates=None, box=None, skip_digestion=False):

    from . import extract
    from molsysmt import pyunitwizard as puw
    from openmm.app import Modeller

    tmp_item = extract(item, atom_indices=atom_indices, copy_if_all=False, skip_digestion=True)
    positions = puw.convert(coordinates[0], 'nm', to_form='openmm.unit')
    tmp_item = Modeller(tmp_item, positions)

    return tmp_item

