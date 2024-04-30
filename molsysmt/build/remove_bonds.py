from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all

@digest()
def remove_bonds(molecular_system, bond_indices='all', in_place=True, skip_digestion=False):

    from molsysmt.basic import where_is_attribute
    from molsysmt.form import _dict_modules

    if in_place:

        item, form = where_is_attribute(molecular_system, 'bond_index', check_if_None=False,
                                        skip_digestion=True)

        add_bonds_function = getattr(_dict_modules[form], f'remove_bonds')
        add_bonds_function(item, bond_indices, skip_digestion=True)

    else:

        raise NotImplementedMethodError

