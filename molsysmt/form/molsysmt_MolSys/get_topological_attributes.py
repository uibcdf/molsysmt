from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import numpy as np
import types

form = 'molsysmt.MolSys'


#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom

def _get_atom_state_attribute(item, attribute, indices='all'):
    from molsysmt.form import molsysmt_Topology

    getter = getattr(molsysmt_Topology, f'get_{attribute}_from_atom')
    return getter(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting formal charge from atom in form molsysmt.MolSys.


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
    return _get_atom_state_attribute(item, 'formal_charge', indices)


@arg_digest(form=form)
def get_formal_charge_from_system(item, skip_digestion=False):
    """
    Getting formal charge from system in form molsysmt.MolSys.


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
    return get_formal_charge_from_atom(item, skip_digestion=True)


@arg_digest(form=form)
def get_atom_is_aromatic_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom is aromatic from atom in form molsysmt.MolSys.


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
    return _get_atom_state_attribute(item, 'atom_is_aromatic', indices)


@arg_digest(form=form)
def get_n_unpaired_electrons_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting n unpaired electrons from atom in form molsysmt.MolSys.


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
    return _get_atom_state_attribute(item, 'n_unpaired_electrons', indices)


@arg_digest(form=form)
def get_n_implicit_hydrogens_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting n implicit hydrogens from atom in form molsysmt.MolSys.


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
    return _get_atom_state_attribute(item, 'n_implicit_hydrogens', indices)


@arg_digest(form=form)
def get_allows_implicit_hydrogens_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting allows implicit hydrogens from atom in form molsysmt.MolSys.


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
    return _get_atom_state_attribute(item, 'allows_implicit_hydrogens', indices)


@arg_digest(form=form)
def get_atom_stereochemistry_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting atom stereochemistry from atom in form molsysmt.MolSys.


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
    return _get_atom_state_attribute(item, 'atom_stereochemistry', indices)


def _get_chemical_state_system_attribute(item, attribute):
    from molsysmt.form import molsysmt_Topology

    getter = getattr(molsysmt_Topology, f'get_{attribute}_from_system')
    return getter(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_chemical_state_index_from_system(item, skip_digestion=False):
    """
    Getting chemical state index from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'chemical_state_index')


@arg_digest(form=form)
def get_chemical_state_id_from_system(item, skip_digestion=False):
    """
    Getting chemical state id from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'chemical_state_id')


@arg_digest(form=form)
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """
    Getting n chemical states from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'n_chemical_states')


@arg_digest(form=form)
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """
    Getting reference chemical state index from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'reference_chemical_state_index')


@arg_digest(form=form)
def get_connectivity_completeness_from_system(item, skip_digestion=False):
    """
    Getting connectivity completeness from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'connectivity_completeness')


@arg_digest(form=form)
def get_component_completeness_from_system(item, skip_digestion=False):
    """
    Getting component completeness from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'component_completeness')


@arg_digest(form=form)
def get_component_evidence_from_system(item, skip_digestion=False):
    """
    Getting component evidence from system in form molsysmt.MolSys.


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
    return _get_chemical_state_system_attribute(item, 'component_evidence')

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom id from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom name from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_isotope_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting isotope from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_isotope_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group id from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group name from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component id from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component name from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity id from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity name from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain id from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain name from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond type from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond order from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_inner_bond_index_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n groups from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n components from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n chains from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n entities from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n ions from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n waters from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from atom in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_atom as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From group


@arg_digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom index from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom id from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom name from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom type from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group index from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group id from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group name from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group type from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component index from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component id from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component name from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component type from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity index from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity id from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity name from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity type from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain index from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain id from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain name from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain type from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n groups from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n components from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n entities from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n chains from group in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_group as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From component


@arg_digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom index from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom id from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom name from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom type from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group index from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group id from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group name from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group type from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component index from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component id from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component name from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component type from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity index from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity id from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity name from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity type from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain index from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain id from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain name from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain type from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n groups from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n components from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n chains from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n entities from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n ions from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n waters from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from component in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_component as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From molecule


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom index from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom id from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom name from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom type from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group index from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group id from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group name from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group type from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component index from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component id from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component name from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component type from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity index from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity id from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity name from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity type from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain index from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain id from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain name from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain type from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n groups from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n components from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n chains from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n entities from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n ions from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n waters from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from molecule in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_molecule as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom index from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom id from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom name from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom type from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group index from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group id from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group name from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group type from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component index from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component id from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component name from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component type from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity index from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity id from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity name from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity type from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain index from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain id from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain name from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain type from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n groups from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n components from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n chains from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n entities from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n ions from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n waters from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from entity in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_entity as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From chain


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom index from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom id from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom name from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom type from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_atom_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group index from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group id from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group name from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group type from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_group_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component index from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component id from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component name from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component type from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_component_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_molecule_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity index from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity id from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity name from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity type from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_entity_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain index from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_index_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain id from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_id_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain name from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_name_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain type from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_chain_type_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n groups from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n components from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n chains from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n entities from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_inner_bonds_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n ions from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n waters from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from chain in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_chain as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From bond


def _get_bond_state_attribute(item, attribute, indices):
    """Delegate a canonical bond-state read to the native topology form."""

    from importlib import import_module

    topology_get = import_module(
        'molsysmt.form.molsysmt_Topology.get_topological_attributes'
    )
    function = getattr(topology_get, f'get_{attribute}_from_bond')
    return function(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond index from bond in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_id_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond id from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_id', indices)


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond order from bond in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_order_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond type from bond in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_type_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_fractional_bond_order_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting fractional bond order from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'fractional_bond_order', indices)


@arg_digest(form=form)
def get_bond_is_aromatic_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond is aromatic from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_is_aromatic', indices)


@arg_digest(form=form)
def get_bond_is_conjugated_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond is conjugated from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_is_conjugated', indices)


@arg_digest(form=form)
def get_bond_stereochemistry_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond stereochemistry from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_stereochemistry', indices)


@arg_digest(form=form)
def get_bond_stereo_atom_indices_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond stereo atom indices from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_stereo_atom_indices', indices)


@arg_digest(form=form)
def get_bond_donor_atom_index_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond donor atom index from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_donor_atom_index', indices)


@arg_digest(form=form)
def get_bond_acceptor_atom_index_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond acceptor atom index from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_acceptor_atom_index', indices)


@arg_digest(form=form)
def get_bond_joins_components_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond joins components from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_joins_components', indices)


@arg_digest(form=form)
def get_bond_evidence_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond evidence from bond in form molsysmt.MolSys.


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
    return _get_bond_state_attribute(item, 'bond_evidence', indices)


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from bond in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from bond in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from bond in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_bond as aux_get
    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    """
    Getting n atoms from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_atoms_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    """
    Getting n groups from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_groups_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    """
    Getting n components from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_components_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    """
    Getting n chains from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_chains_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    """
    Getting n molecules from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_molecules_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    """
    Getting n entities from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_entities_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    """
    Getting n bonds from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_bonds_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)

@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    """
    Getting n amino acids from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_amino_acids_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    """
    Getting n nucleotides from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_nucleotides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    """
    Getting n ions from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_ions_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    """
    Getting n waters from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_waters_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    """
    Getting n small molecules from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_small_molecules_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    """
    Getting n peptides from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_peptides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    """
    Getting n proteins from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_proteins_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    """
    Getting n dnas from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_dnas_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    """
    Getting n rnas from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_rnas_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)

@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    """
    Getting n lipids from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_lipids_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    """
    Getting n polysaccharides from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_polysaccharides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    """
    Getting n saccharides from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_n_saccharides_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    """
    Getting bond index from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bond_index_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atoms from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atoms_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atom pairs from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_inner_bonded_atom_pairs_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting bonded atoms from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bonded_atoms_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_system(item, skip_digestion=False):

    """
    Getting bonded atom pairs from system in form molsysmt.MolSys.


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
    from molsysmt.form.molsysmt_Topology import get_bonded_atom_pairs_from_system as aux_get
    return aux_get(item.topology, skip_digestion=True)


# List of functions to be imported


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
