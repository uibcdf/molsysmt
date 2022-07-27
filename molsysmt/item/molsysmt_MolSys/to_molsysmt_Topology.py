from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.variables import is_all

def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    if check:

        digest_item(item, 'molsysmt.MolSys')
        atom_indices = digest_atom_indices(atom_indices)
        structure_indices = digest_structure_indices(structure_indices)

    if is_all(atom_indices):

        tmp_item = item.topology.copy()

    else:

        from molsysmt.item.molsysmt_Topology import extract
        tmp_item = extract(item.topology, atom_indices=atom_indices)

    return tmp_item
