from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest(form='molsysmt.MolSys')
def to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    if is_all(atom_indices):

        tmp_item = item.topology.copy()

    else:

        from molsysmt.form.molsysmt_Topology import extract
        tmp_item = extract(item.topology, atom_indices=atom_indices)

    return tmp_item

def _to_molsysmt_Topology(item, atom_indices='all', structure_indices='all'):

    return to_molsysmt_Topology(item, atom_indices=atom_indices)
