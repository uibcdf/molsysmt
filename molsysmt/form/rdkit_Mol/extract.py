from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='rdkit.Mol')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):
        return item
    else:
        # Convert to MolSys, extract, and convert back to rdkit.Mol
        from molsysmt.basic import convert
        tmp_item = convert(item, to_form='molsysmt.MolSys', atom_indices=atom_indices, 
                           structure_indices=structure_indices, skip_digestion=True)
        return convert(tmp_item, to_form='rdkit.Mol', skip_digestion=True)
