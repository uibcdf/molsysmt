from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSysOld')
def to_molsysmt_TopologyOld(item, atom_indices='all', structure_indices='all'):

    if is_all(atom_indices):

        tmp_item = item.topology.copy()

    else:

        from molsysmt.form.molsysmt_TopologyOld import extract
        tmp_item = extract(item.topology, atom_indices=atom_indices)

    return tmp_item
