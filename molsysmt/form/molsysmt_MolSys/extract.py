from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

@arg_digest(form='molsysmt.MolSys')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from molsysmt.native import MolSys
    if not isinstance(item, MolSys):
        from molsysmt.basic import convert
        item = convert(item, to_form='molsysmt.MolSys', skip_digestion=True)

    return item.extract(atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all,
                        skip_digestion=True)
    
