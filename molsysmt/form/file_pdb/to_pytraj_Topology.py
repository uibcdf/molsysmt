from molsysmt._private.smonitor import LibraryNotFoundError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw

@arg_digest(form='file:pdb')
def to_pytraj_Topology(item, atom_indices='all', max_bond_length=None, skip_digestion=False):

    try:
        from pytraj import load_topology
    except Exception:
        raise LibraryNotFoundError('pytraj')

    from ..pytraj_Topology.extract import extract as extract_pytraj_Topology

    option = ''
    if max_bond_length is not None:
        value = puw.get_value(max_bond_length, to_unit='nanometers')
        option = 'bondsearch {round(value, 3)}'

    tmp_item = load_topology(item, option)
    tmp_item = extract_pytraj_Topology(tmp_item, atom_indices=atom_indices,
                                       copy_if_all=False, skip_digestion=True)

    return tmp_item

