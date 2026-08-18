from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt.attribute import bonds_are_required_to_get_attribute
import types

form = 'string:smiles'


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom id from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom id from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom id from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom id from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom id from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom id from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom name from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom name from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom name from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom name from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom name from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom name from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('atom_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond index from bond in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'bond')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    """
    Getting bond index from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_index', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond order from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond order from bond in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'bond')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond order from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond order from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond order from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond order from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond order from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_order', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond type from bond in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'bond')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bond_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from bond in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'bond')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):

    """
    Getting bonded atom pairs from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atom_pairs', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from bond in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'bond')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting bonded atoms from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('bonded_atoms', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain id from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain id from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain id from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain id from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain id from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain id from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain name from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain name from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain name from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain name from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain name from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain name from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('chain_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component id from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component id from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component id from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component id from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component id from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component id from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component name from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component name from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component name from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component name from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component name from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component name from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_component_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('component_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity id from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity id from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity id from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity id from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity id from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity id from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity name from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity name from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity name from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity name from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity name from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity name from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('entity_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group id from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group id from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group id from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group id from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group id from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group id from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group name from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group name from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group name from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group name from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group name from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group name from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_group_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('group_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_system(item, skip_digestion=False):

    """
    Getting inner bond index from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bond_index', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atom pairs from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atom_pairs', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atoms from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('inner_bonded_atoms', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_id', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_index', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_name', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('molecule_type', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    """
    Getting n amino acids from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_amino_acids', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    """
    Getting n atoms from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_atoms', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from bond in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_bond as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'bond')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    """
    Getting n bonds from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_bonds', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n chains from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n chains from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n chains from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n chains from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n chains from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n chains from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    """
    Getting n chains from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_chains', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n components from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n components from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n components from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n components from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n components from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n components from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    """
    Getting n components from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_components_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_components', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    """
    Getting n dnas from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_dnas', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n entities from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n entities from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n entities from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n entities from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n entities from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n entities from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    """
    Getting n entities from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_entities', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n groups from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n groups from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n groups from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n groups from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n groups from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n groups from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    """
    Getting n groups from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_groups', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_inner_bonds', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n ions from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n ions from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n ions from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n ions from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n ions from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n ions from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    """
    Getting n ions from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_ions', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    """
    Getting n lipids from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_lipids', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    """
    Getting n molecules from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_molecules', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    """
    Getting n nucleotides from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_nucleotides', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    """
    Getting n peptides from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_peptides', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    """
    Getting n polysaccharides from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_polysaccharides', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    """
    Getting n proteins from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_proteins', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    """
    Getting n rnas from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_rnas', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    """
    Getting n saccharides from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_saccharides', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    """
    Getting n small molecules from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_small_molecules', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n waters from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n waters from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n waters from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n waters from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n waters from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n waters from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    """
    Getting n waters from system in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_system as aux_get

    bonds_required = bonds_are_required_to_get_attribute('n_waters', 'system')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_amino_acids_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_amino_acids', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_amino_acids_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_amino_acids', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_amino_acids_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_amino_acids', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_amino_acids_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_amino_acids', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_amino_acids_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_amino_acids', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_amino_acids_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_amino_acids', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_atoms_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_atoms', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_atoms_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_atoms', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_atoms_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_atoms', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_atoms_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_atoms', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_atoms_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_atoms', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_atoms_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_atoms', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_bonds_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_bonds', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_bonds_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_bonds', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_bonds_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_bonds', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_bonds_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_bonds', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_bonds_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_bonds', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_bonds_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_bonds', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_chains_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_chains', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_chains_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_chains', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_chains_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_chains', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_chains_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_chains', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_chains_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_chains', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_chains_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_chains', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_components_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n components from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_components_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_components', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_components_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n components from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_components_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_components', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_components_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n components from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_components_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_components', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_components_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n components from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_components_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_components', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_components_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n components from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_components_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_components', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_components_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n components from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_components_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_components', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_dnas_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_dnas', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_dnas_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_dnas', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_dnas_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_dnas', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_dnas_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_dnas', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_dnas_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_dnas', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_dnas_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_dnas', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_entities_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_entities', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_entities_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_entities', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_entities_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_entities', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_entities_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_entities', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_entities_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_entities', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_entities_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_entities', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_groups_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_groups', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_groups_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_groups', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_groups_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_groups', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_groups_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_groups', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_groups_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_groups', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_groups_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_groups', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_inner_bonds_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_inner_bonds', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_inner_bonds_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_inner_bonds', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_inner_bonds_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_inner_bonds', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_inner_bonds_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_inner_bonds', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_inner_bonds_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_inner_bonds', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_inner_bonds_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_inner_bonds', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_ions_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_ions_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_ions', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_ions_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_ions_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_ions', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_ions_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_ions_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_ions', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_ions_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_ions_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_ions', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_ions_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_ions_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_ions', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_ions_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_ions', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_lipids_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_lipids', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_lipids_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_lipids', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_lipids_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_lipids', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_lipids_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_lipids', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_lipids_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_lipids', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_lipids_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_lipids', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_molecules_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_molecules', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_molecules_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_molecules', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_molecules_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_molecules', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_molecules_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_molecules', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_molecules_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_molecules', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_molecules_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_molecules', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_nucleotides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_nucleotides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_nucleotides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_nucleotides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_nucleotides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_nucleotides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_nucleotides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_nucleotides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_nucleotides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_nucleotides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_nucleotides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_nucleotides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_peptides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_peptides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_peptides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_peptides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_peptides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_peptides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_peptides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_peptides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_peptides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_peptides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_peptides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_peptides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_polysaccharides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_polysaccharides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_polysaccharides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_polysaccharides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_polysaccharides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_polysaccharides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_polysaccharides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_polysaccharides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_polysaccharides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_polysaccharides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_polysaccharides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_polysaccharides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_proteins_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_proteins', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_proteins_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_proteins', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_proteins_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_proteins', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_proteins_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_proteins', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_proteins_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_proteins', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_proteins_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_proteins', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_rnas_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_rnas', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_rnas_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_rnas', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_rnas_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_rnas', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_rnas_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_rnas', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_rnas_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_rnas', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_rnas_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_rnas', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_saccharides_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_saccharides', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_saccharides_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_saccharides', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_saccharides_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_saccharides', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_saccharides_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_saccharides', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_saccharides_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_saccharides', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_saccharides_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_saccharides', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_small_molecules_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_small_molecules', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_small_molecules_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_small_molecules', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_small_molecules_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_small_molecules', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_small_molecules_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_small_molecules', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_small_molecules_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_small_molecules', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_small_molecules_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_small_molecules', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_waters_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from atom in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_waters_from_atom as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_waters', 'atom')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_waters_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from chain in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_waters_from_chain as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_waters', 'chain')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_waters_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from component in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_waters_from_component as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_waters', 'component')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_waters_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from entity in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_waters_from_entity as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_waters', 'entity')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_waters_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from group in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_waters_from_group as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_waters', 'group')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_total_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from molecule in form string:smiles.

    Parameters
    ----------
    item : string:smiles
        Source item in string:smiles form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.string_smiles.to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_total_n_waters_from_molecule as aux_get

    bonds_required = bonds_are_required_to_get_attribute('total_n_waters', 'molecule')
    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]