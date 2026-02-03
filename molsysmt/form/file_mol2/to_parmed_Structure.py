from molsysmt._private.digestion import arg_digest
from molsysmt.dependencies import requires

@arg_digest(form='file:mol2')
@requires('parmed')
def to_parmed_Structure(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from parmed import load_file

    from molsysmt.form.parmed_Structure import extract

    tmp_item = load_file(item)
    tmp_item = tmp_item.to_structure()
    tmp_item = extract(tmp_item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=False,
                       skip_digestion=True)

    return tmp_item

