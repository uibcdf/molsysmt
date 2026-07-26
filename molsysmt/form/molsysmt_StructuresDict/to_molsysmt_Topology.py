from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.StructuresDict')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from molsysmt.native.topology import Topology
    from molsysmt._private.variables import is_all
    from . import get_n_atoms_from_system

    if is_all(atom_indices):
        n_atoms = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        n_atoms = len(atom_indices)
    tmp_item = Topology(n_atoms=n_atoms)

    return tmp_item
