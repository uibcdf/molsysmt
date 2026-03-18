from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='openff.Molecule')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures

    tmp_item = Structures()
    # openff.Molecule does not store conformers in the same way as rdkit;
    # conformers are attached separately and not always present.
    return tmp_item
