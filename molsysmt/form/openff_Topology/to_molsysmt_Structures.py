from molsysmt._private.argdigest import arg_digest

@arg_digest(form='openff.Topology')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures

    tmp_item = Structures()
    return tmp_item
