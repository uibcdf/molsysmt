from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all

@arg_digest()
def remove_bonds(molecular_system, bond_indices='all', in_place=True, skip_digestion=False):
    """Remove bonds from a molecular system by index.

    Parameters
    ----------
    molecular_system : molecular system
        System from which bonds will be removed.
    bond_indices : 'all' or array-like, default 'all'
        Bond indices to delete.
    in_place : bool, default True
        If `True`, modify in place; otherwise raise NotImplementedMethodError.
    skip_digestion : bool, default False
        Whether to skip argument digestion.
    """

    from molsysmt.basic import where_is_attribute
    from molsysmt.form import _dict_modules

    if in_place:

        item, form = where_is_attribute(molecular_system, 'bond_index', include_none=False,
                                        skip_digestion=True)

        remove_bonds_function = getattr(_dict_modules[form], f'remove_bonds')
        remove_bonds_function(item, bond_indices, skip_digestion=True)

    else:

        raise NotImplementedMethodError
