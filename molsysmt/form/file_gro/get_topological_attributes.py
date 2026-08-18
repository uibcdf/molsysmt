from molsysmt._private.argdigest import arg_digest
import types

form = 'file:gro'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:gro.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolSys.get_topological_attributes import get_n_atoms_from_system as aux_get
    from molsysmt.basic import convert
    tmp_item = convert(item, to_form='molsysmt.MolSys', skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
