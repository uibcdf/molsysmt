from molsysmt._private.argdigest import arg_digest
import types

form = 'file:pdb'

@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form file:pdb.


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
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_n_atoms_from_system as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form file:pdb.


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
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_n_groups_from_system as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, skip_digestion=True)

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom id from atom in form file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_atom_id_from_atom as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom name from atom in form file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_atom_name_from_atom as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):
    """
    Getting group name from group in form file:pdb.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from .to_molsysmt_PDBFileHandler import to_molsysmt_PDBFileHandler
    from molsysmt.form.molsysmt_PDBFileHandler.get_topological_attributes import get_group_name_from_group as aux_get
    tmp_item = to_molsysmt_PDBFileHandler(item, skip_digestion=True)
    return aux_get(tmp_item, indices=indices, skip_digestion=True)

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
