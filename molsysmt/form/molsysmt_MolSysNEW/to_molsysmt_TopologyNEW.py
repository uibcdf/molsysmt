from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSysNEW')
def to_molsysmt_TopologyNEW(item, atom_indices='all', structure_indices='all'):

    if is_all(atom_indices):

        tmp_item = item.topology.copy()

    else:

        from molsysmt.form.molsysmt_TopologyNEW import extract
        tmp_item = extract(item.topology, atom_indices=atom_indices)

    return tmp_item
