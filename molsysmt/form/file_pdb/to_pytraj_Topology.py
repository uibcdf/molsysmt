from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw

@digest(form='file:pdb')
def to_pytraj_Topology(item, atom_indices='all', max_bond_distance=None, skip_digestion=False):

    try:
        from pytraj import load_topology
    except:
        raise LibraryNotFoundError('pytraj')

    from ..pytraj_Topology import extract as extract_pytraj_Topology

    option = ''
    if max_bond_distance is not None:
        value = puw.get_value(max_bond_distance, to_unit='nanometers')
        option = 'bondsearch {round(value, 3)}'

    tmp_item = load_topology(item, option)
    tmp_item = extract_pytraj_Topology(tmp_item, atom_indices=atom_indices,
                                       copy_if_all=False, skip_digestion=True)

    return tmp_item

