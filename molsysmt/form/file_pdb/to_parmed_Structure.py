from molsysmt.dependencies import dep_digest
from molsysmt._private.digestion import arg_digest

@arg_digest(form='file:pdb')
@dep_digest('parmed')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from parmed import load_file

    from molsysmt.form.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=False)

    return tmp_item

