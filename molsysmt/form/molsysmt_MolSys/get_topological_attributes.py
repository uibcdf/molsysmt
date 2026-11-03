import types
from collections import defaultdict
from itertools import chain, compress

import numpy as np
import pandas as pd
from networkx import Graph

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.native._topology_infer import (
    molecule_indices_from_atoms as _molecule_indices_from_atoms,
)

form = "molsysmt.MolSys"


#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom


def _get_atom_state_attribute(item, attribute, indices="all"):
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    getter = getattr(molsysmt_ChemicalStates, f"get_{attribute}_from_atom")
    return getter(item.chemical_states, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_formal_charge_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_formal_charge_from_system(
        item.chemical_states, skip_digestion=True
    )


@arg_digest(form=form)
def get_atom_is_aromatic_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_atom_is_aromatic_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_unpaired_electrons_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_unpaired_electrons_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_implicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_implicit_hydrogens_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_explicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting bracket-declared hydrogen counts from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Molecular system supplying the declared chemical state.
    indices : object, default='all'
        Atom indices whose coordinate-free explicit hydrogen counts are requested.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Declared per-atom hydrogen counts, preserving unknown values and requested order.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_explicit_hydrogens_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_allows_implicit_hydrogens_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_allows_implicit_hydrogens_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_atom_stereochemistry_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_atom_stereochemistry_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_chemical_state_index_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_chemical_state_id_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_chemical_states_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_reference_chemical_state_index_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    return (
        None
        if item.chemical_states is None
        else item.chemical_states._resolve_chemical_state().connectivity_completeness
    )


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
    return (
        None
        if item.chemical_states is None
        else item.chemical_states._resolve_chemical_state().component_completeness
    )


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
    return (
        None
        if item.chemical_states is None
        else item.chemical_states._resolve_chemical_state().component_evidence
    )


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
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

    if item.topology is None:
        n_atoms = item._get_n_atoms()
        if n_atoms is None:
            return None
        return list(range(n_atoms)) if is_all(indices) else list(indices)
    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices="all", skip_digestion=False):
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
def get_atom_name_from_atom(item, indices="all", skip_digestion=False):
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
def get_atom_type_from_atom(item, indices="all", skip_digestion=False):
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
def get_isotope_from_atom(item, indices="all", skip_digestion=False):
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
def get_group_index_from_atom(item, indices="all", skip_digestion=False):
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
def get_group_id_from_atom(item, indices="all", skip_digestion=False):
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
def get_group_name_from_atom(item, indices="all", skip_digestion=False):
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
def get_group_type_from_atom(item, indices="all", skip_digestion=False):
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
def get_component_index_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_index_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_id_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_id_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_name_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_name_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_type_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_type_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices="all", skip_digestion=False):
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
def get_molecule_id_from_atom(item, indices="all", skip_digestion=False):
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
def get_molecule_name_from_atom(item, indices="all", skip_digestion=False):
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
def get_molecule_type_from_atom(item, indices="all", skip_digestion=False):
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
def get_entity_index_from_atom(item, indices="all", skip_digestion=False):
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
def get_entity_id_from_atom(item, indices="all", skip_digestion=False):
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
def get_entity_name_from_atom(item, indices="all", skip_digestion=False):
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
def get_entity_type_from_atom(item, indices="all", skip_digestion=False):
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
def get_chain_index_from_atom(item, indices="all", skip_digestion=False):
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
def get_chain_id_from_atom(item, indices="all", skip_digestion=False):
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
def get_chain_name_from_atom(item, indices="all", skip_digestion=False):
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
def get_chain_type_from_atom(item, indices="all", skip_digestion=False):
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
def get_bond_index_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_index_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_type_from_atom(item, indices="all", skip_digestion=False):
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
    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux_indices:
        aux_vals = get_bond_type_from_bond(item, indices=ii, skip_digestion=True)
        output.append(aux_vals)
    return output


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices="all", skip_digestion=False):
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
    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = []
    for ii in aux_indices:
        aux_vals = get_bond_order_from_bond(item, indices=ii, skip_digestion=True)
        output.append(aux_vals)
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices="all", skip_digestion=False):
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
    output = None
    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    G.add_edges_from(edges)
    if indices == "all":
        indices = get_atom_index_from_atom(item, skip_digestion=True)
    output = []
    for ii in indices:
        if ii in G:
            output.append(list(G.neighbors(ii)))
        else:
            output.append([])
    del G, edges
    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bonded_atom_pairs_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_inner_bond_index_from_atom(item, indices="all", skip_digestion=False):
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
    output = None
    G = Graph()
    edges = np.asarray(
        get_bonded_atom_pairs_from_bond(item, skip_digestion=True), dtype=np.int64
    ).reshape(-1, 2)
    n_bonds = len(edges)
    edge_indices = np.array([{"index": ii} for ii in range(n_bonds)]).reshape(
        [n_bonds, 1]
    )
    G.add_edges_from(np.hstack([edges, edge_indices]))
    if indices == "all":
        indices = get_atom_index_from_atom(item)
    else:
        G = G.subgraph(indices)
    output = []
    for ii in indices:
        if ii in G:
            output.append([n["index"] for n in G[ii].values()])
        else:
            output.append([])
    del G, edges, edge_indices
    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices="all", skip_digestion=False):
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
    output = None
    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    G.add_edges_from(edges)
    if not indices == "all":
        G = G.subgraph(indices)
    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))
    del G, edges
    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_inner_bonded_atom_pairs_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_groups_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_components_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_components_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_chains_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_entities_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_bonds_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_bonds_from_atom(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices="all", skip_digestion=False):
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
    inner_bond_indices = get_inner_bond_index_from_atom(
        item, indices, skip_digestion=True
    )
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices
    return output


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_nucleotides_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_ions_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_waters_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_small_molecules_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_small_molecules_from_atom as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_proteins_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_dnas_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_rnas_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_lipids_from_atom(item, indices="all", skip_digestion=False):
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
def get_n_polysaccharides_from_atom(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_polysaccharides_from_atom as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices="all", skip_digestion=False):
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
def get_atom_index_from_group(item, indices="all", skip_digestion=False):
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
def get_atom_id_from_group(item, indices="all", skip_digestion=False):
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
def get_atom_name_from_group(item, indices="all", skip_digestion=False):
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
def get_atom_type_from_group(item, indices="all", skip_digestion=False):
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
def get_group_index_from_group(item, indices="all", skip_digestion=False):
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
def get_group_id_from_group(item, indices="all", skip_digestion=False):
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
def get_group_name_from_group(item, indices="all", skip_digestion=False):
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
def get_group_type_from_group(item, indices="all", skip_digestion=False):
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
def get_component_index_from_group(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    if indices == "all":
        from molsysmt.form.molsysmt_MolSys.get_topological_attributes import (
            get_n_groups_from_system,
        )

        n_groups = get_n_groups_from_system(item)
        indices = range(n_groups)
    aux_dict = {ii: set() for ii in indices}
    for atom_index, group_index in enumerate(group_index_from_atom):
        if group_index in aux_dict:
            aux_dict[group_index].add(component_index_from_atom[atom_index])
    output = []
    for ii in indices:
        val = aux_dict[ii]
        clean_val = [int(jj) for jj in val if jj is not None and (not pd.isna(jj))]
        if clean_val:
            output.append(clean_val[0])
        else:
            output.append(None)
    return output


@arg_digest(form=form)
def get_component_id_from_group(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_id_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_id"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        component_id_from_component[next(iter(ii))]
        if len(ii) == 1
        else component_id_from_component[list(ii)].tolist()
        for ii in output
    ]
    del (
        group_index_from_atom,
        component_index_from_atom,
        component_id_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_component_name_from_group(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_name_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_name"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        component_name_from_component[next(iter(ii))]
        if len(ii) == 1
        else component_name_from_component[list(ii)].tolist()
        for ii in output
    ]
    del (
        group_index_from_atom,
        component_index_from_atom,
        component_name_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_component_type_from_group(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_type_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_type"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        component_type_from_component[next(iter(ii))]
        if len(ii) == 1
        else component_type_from_component[list(ii)].tolist()
        for ii in output
    ]
    del (
        group_index_from_atom,
        component_index_from_atom,
        component_type_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices="all", skip_digestion=False):
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
def get_molecule_id_from_group(item, indices="all", skip_digestion=False):
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
def get_molecule_name_from_group(item, indices="all", skip_digestion=False):
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
def get_molecule_type_from_group(item, indices="all", skip_digestion=False):
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
def get_entity_index_from_group(item, indices="all", skip_digestion=False):
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
def get_entity_id_from_group(item, indices="all", skip_digestion=False):
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
def get_entity_name_from_group(item, indices="all", skip_digestion=False):
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
def get_entity_type_from_group(item, indices="all", skip_digestion=False):
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
def get_chain_index_from_group(item, indices="all", skip_digestion=False):
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
def get_chain_id_from_group(item, indices="all", skip_digestion=False):
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
def get_chain_name_from_group(item, indices="all", skip_digestion=False):
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
def get_chain_type_from_group(item, indices="all", skip_digestion=False):
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
def get_n_atoms_from_group(item, indices="all", skip_digestion=False):
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
def get_n_groups_from_group(item, indices="all", skip_digestion=False):
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
def get_n_components_from_group(item, indices="all", skip_digestion=False):
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
    output = get_component_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]
    return output


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices="all", skip_digestion=False):
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
def get_n_entities_from_group(item, indices="all", skip_digestion=False):
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
def get_n_chains_from_group(item, indices="all", skip_digestion=False):
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


@arg_digest(form=form)
def get_n_bonds_from_group(item, indices="all", skip_digestion=False):
    """Getting unique incident bond counts for selected groups.

    Parameters
    ----------
    item : molsysmt.MolSys
        Molecular system containing group membership and chemical-state bonds.
    indices : list of int or 'all', default='all'
        Group indices in the requested output order. An empty list selects no groups.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int
        Number of distinct bonds incident on each selected group. A bond between
        groups contributes once to each group; an internal bond is counted once.

    Notes
    -----
    Delegation to the topology facade preserves the chemical state selected by
    ``molsysmt.get``. No independent bond storage is created.

    Examples
    --------
    >>> import molsysmt as msm
    >>> builder = msm.MolSysBuilder()
    >>> a = builder.add_atom(atom_name='C', atom_type='C')
    >>> b = builder.add_atom(atom_name='C', atom_type='C')
    >>> group = builder.add_group([a, b], group_name='X', group_type='unknown')
    >>> bond = builder.add_bond(a, b)
    >>> msm.get(builder.build(), element='group', n_bonds=True)
    [1]

    .. versionadded:: 1.0.0
    """
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices
    return output


# From component


@arg_digest(form=form)
def get_atom_index_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_atom_index_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_atom_id_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    atom_id_from_atom = item.topology.atoms["atom_id"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_id_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_id_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    del component_index_from_atom, atom_id_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_atom_name_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    atom_name_from_atom = item.topology.atoms["atom_name"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_name_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_name_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    del component_index_from_atom, atom_name_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_atom_type_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    atom_type_from_atom = item.topology.atoms["atom_type"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_type_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_type_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    del component_index_from_atom, atom_type_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_group_index_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            component_index = component_index_from_atom[atom_index]
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    del group_index_from_atom, component_index_from_atom, aux_dict
    output = [list(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_group_id_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    group_id_from_group = item.topology.groups["group_id"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [group_id_from_group[sorted(ii)].tolist() for ii in output]
    del group_index_from_atom, component_index_from_atom, group_id_from_group
    del aux_dict
    return output


@arg_digest(form=form)
def get_group_name_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    group_name_from_group = item.topology.groups["group_name"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [group_name_from_group[sorted(ii)].tolist() for ii in output]
    del group_index_from_atom, component_index_from_atom, group_name_from_group
    del aux_dict
    return output


@arg_digest(form=form)
def get_group_type_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    group_type_from_group = item.topology.groups["group_type"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(group_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [group_type_from_group[sorted(ii)].tolist() for ii in output]
    del group_index_from_atom, component_index_from_atom, group_type_from_group
    del aux_dict
    return output


@arg_digest(form=form)
def get_component_index_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_index_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_id_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_id_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_name_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_name_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_component_type_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_component_type_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_molecule_index_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]
    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_molecule_id_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    molecule_id_from_molecule = item.topology.molecules["molecule_id"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        molecule_id_from_molecule[next(iter(ii))]
        if len(ii) == 1
        else molecule_id_from_molecule[sorted(ii)].tolist()
        for ii in output
    ]
    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_id_from_molecule, aux_dict
    return output


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    molecule_name_from_molecule = item.topology.molecules["molecule_name"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        molecule_name_from_molecule[next(iter(ii))]
        if len(ii) == 1
        else molecule_name_from_molecule[sorted(ii)].tolist()
        for ii in output
    ]
    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_name_from_molecule, aux_dict
    return output


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[
        group_index_from_atom.astype(int)
    ]
    molecule_type_from_molecule = item.topology.molecules["molecule_type"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(molecule_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        molecule_type_from_molecule[next(iter(ii))]
        if len(ii) == 1
        else molecule_type_from_molecule[sorted(ii)].tolist()
        for ii in output
    ]
    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_type_from_molecule, aux_dict
    return output


@arg_digest(form=form)
def get_entity_index_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]
    del component_index_from_atom, entity_index_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_entity_id_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_id_from_entity = item.topology.entities["entity_id"].to_numpy()
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        entity_id_from_entity[next(iter(ii))]
        if len(ii) == 1
        else entity_id_from_entity[sorted(ii)].tolist()
        for ii in output
    ]
    del (
        component_index_from_atom,
        entity_index_from_atom,
        entity_id_from_entity,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_entity_name_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_name_from_entity = item.topology.entities["entity_name"].to_numpy()
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        entity_name_from_entity[next(iter(ii))]
        if len(ii) == 1
        else entity_name_from_entity[sorted(ii)].tolist()
        for ii in output
    ]
    del (
        component_index_from_atom,
        entity_index_from_atom,
        entity_name_from_entity,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_entity_type_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_type_from_entity = item.topology.entities["entity_type"].to_numpy()
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(entity_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        entity_type_from_entity[next(iter(ii))]
        if len(ii) == 1
        else entity_type_from_entity[sorted(ii)].tolist()
        for ii in output
    ]
    del (
        component_index_from_atom,
        entity_index_from_atom,
        entity_type_from_entity,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_chain_index_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]
    del component_index_from_atom, chain_index_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_chain_id_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    chain_id_from_chain = item.topology.chains["chain_id"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        chain_id_from_chain[next(iter(ii))]
        if len(ii) == 1
        else chain_id_from_chain[sorted(ii)].tolist()
        for ii in output
    ]
    del component_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict
    return output


@arg_digest(form=form)
def get_chain_name_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    chain_name_from_chain = item.topology.chains["chain_name"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        chain_name_from_chain[next(iter(ii))]
        if len(ii) == 1
        else chain_name_from_chain[sorted(ii)].tolist()
        for ii in output
    ]
    del (
        component_index_from_atom,
        chain_index_from_atom,
        chain_name_from_chain,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_chain_type_from_component(item, indices="all", skip_digestion=False):
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
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    chain_type_from_chain = item.topology.chains["chain_type"].to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].add(chain_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [
        chain_type_from_chain[next(iter(ii))]
        if len(ii) == 1
        else chain_type_from_chain[sorted(ii)].tolist()
        for ii in output
    ]
    del (
        component_index_from_atom,
        chain_index_from_atom,
        chain_type_from_chain,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_atoms_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_groups_from_component(item, indices="all", skip_digestion=False):
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
    output = get_group_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]
    return output


@arg_digest(form=form)
def get_n_components_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_components_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_molecules_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = np.unique(output).size
    return output


@arg_digest(form=form)
def get_n_chains_from_component(item, indices="all", skip_digestion=False):
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
    output = get_chain_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]
    return output


@arg_digest(form=form)
def get_n_entities_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = np.unique(output).size
    return output


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_n_bonds_from_component(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices="all", skip_digestion=False):
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
    output = get_bond_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("amino acid") for ii in group_types]
    return output


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("nucleotide") for ii in group_types]
    return output


@arg_digest(form=form)
def get_n_ions_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("ion") for ii in group_types]
    return output


@arg_digest(form=form)
def get_n_waters_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("water") for ii in group_types]
    return output


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("small molecule") for ii in group_types]
    return output


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_peptides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(
            item, indices=molecule_indices, skip_digestion=True
        )
        output = molecule_type.count("peptide")
    return output


@arg_digest(form=form)
def get_n_proteins_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_proteins_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(
            item, indices=molecule_indices, skip_digestion=True
        )
        output = molecule_type.count("protein")
    return output


@arg_digest(form=form)
def get_n_dnas_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_dnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(
            item, indices=molecule_indices, skip_digestion=True
        )
        output = molecule_type.count("dna")
    return output


@arg_digest(form=form)
def get_n_rnas_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_rnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(
            item, indices=molecule_indices, skip_digestion=True
        )
        output = molecule_type.count("rna")
    return output


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("lipid") for ii in group_types]
    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_polysaccharides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(
            item, indices=molecule_indices, skip_digestion=True
        )
        output = molecule_type.count("polysaccharide")
    return output


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices="all", skip_digestion=False):
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
    group_types = get_group_type_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("saccharide") for ii in group_types]
    return output


# From molecule


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices="all", skip_digestion=False):
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
def get_atom_id_from_molecule(item, indices="all", skip_digestion=False):
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
def get_atom_name_from_molecule(item, indices="all", skip_digestion=False):
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
def get_atom_type_from_molecule(item, indices="all", skip_digestion=False):
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
def get_group_index_from_molecule(item, indices="all", skip_digestion=False):
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
def get_group_id_from_molecule(item, indices="all", skip_digestion=False):
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
def get_group_name_from_molecule(item, indices="all", skip_digestion=False):
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
def get_group_type_from_molecule(item, indices="all", skip_digestion=False):
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
def get_component_index_from_molecule(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    del (
        group_index_from_atom,
        molecule_index_from_atom,
        component_index_from_atom,
        aux_dict,
    )
    output = [list(np.unique(ii)) for ii in output]
    return output


@arg_digest(form=form)
def get_component_id_from_molecule(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_id_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_id"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    output = [component_id_from_component[np.unique(ii)].tolist() for ii in output]
    del (
        group_index_from_atom,
        molecule_index_from_atom,
        component_index_from_atom,
        component_id_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_component_name_from_molecule(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_name_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_name"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    output = [component_name_from_component[np.unique(ii)].tolist() for ii in output]
    del (
        group_index_from_atom,
        molecule_index_from_atom,
        component_index_from_atom,
        component_name_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_component_type_from_molecule(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    item.topology.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_name_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_type"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    output = [component_name_from_component[np.unique(ii)].tolist() for ii in output]
    del (
        group_index_from_atom,
        molecule_index_from_atom,
        component_index_from_atom,
        component_name_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_molecule_index_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices="all", skip_digestion=False):
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
def get_molecule_name_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_molecule_name_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_molecule_type_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_entity_index_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices="all", skip_digestion=False):
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
def get_entity_name_from_molecule(item, indices="all", skip_digestion=False):
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
def get_entity_type_from_molecule(item, indices="all", skip_digestion=False):
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
def get_chain_index_from_molecule(item, indices="all", skip_digestion=False):
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
def get_chain_id_from_molecule(item, indices="all", skip_digestion=False):
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
def get_chain_name_from_molecule(item, indices="all", skip_digestion=False):
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
def get_chain_type_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_atoms_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_groups_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_components_from_molecule(item, indices="all", skip_digestion=False):
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
    output = get_component_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]
    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_chains_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_entities_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_bonds_from_molecule(item, indices="all", skip_digestion=False):
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
    output = get_bond_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices="all", skip_digestion=False):
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
    output = get_inner_bond_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_amino_acids_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_nucleotides_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_waters_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_small_molecules_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_small_molecules_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_proteins_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_dnas_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_rnas_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_lipids_from_molecule(item, indices="all", skip_digestion=False):
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
def get_n_polysaccharides_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_polysaccharides_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_saccharides_from_molecule as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


# From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices="all", skip_digestion=False):
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
def get_atom_id_from_entity(item, indices="all", skip_digestion=False):
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
def get_atom_name_from_entity(item, indices="all", skip_digestion=False):
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
def get_atom_type_from_entity(item, indices="all", skip_digestion=False):
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
def get_group_index_from_entity(item, indices="all", skip_digestion=False):
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
def get_group_id_from_entity(item, indices="all", skip_digestion=False):
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
def get_group_name_from_entity(item, indices="all", skip_digestion=False):
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
def get_group_type_from_entity(item, indices="all", skip_digestion=False):
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
def get_component_index_from_entity(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        component_index_from_atom,
        aux_dict,
    )
    output = [list(np.unique(ii)) for ii in output]
    return output


@arg_digest(form=form)
def get_component_id_from_entity(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_id_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_id"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    output = [component_id_from_component[np.unique(ii)].tolist() for ii in output]
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        component_index_from_atom,
        aux_dict,
    )
    del component_id_from_component
    return output


@arg_digest(form=form)
def get_component_name_from_entity(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_name_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_name"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    output = [component_name_from_component[np.unique(ii)].tolist() for ii in output]
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        component_index_from_atom,
        aux_dict,
    )
    del component_name_from_component
    return output


@arg_digest(form=form)
def get_component_type_from_entity(item, indices="all", skip_digestion=False):
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
    group_index_from_atom = item.topology.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.topology.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.topology.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item.topology)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_type_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_type"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(component_index_from_atom[atom_index])
        output = [aux_dict[ii] for ii in indices]
    output = [component_type_from_component[np.unique(ii)].tolist() for ii in output]
    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        component_index_from_atom,
        aux_dict,
    )
    del component_type_from_component
    return output


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_molecule_index_from_entity as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_id_from_entity(item, indices="all", skip_digestion=False):
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
def get_molecule_name_from_entity(item, indices="all", skip_digestion=False):
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
def get_molecule_type_from_entity(item, indices="all", skip_digestion=False):
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
def get_entity_index_from_entity(item, indices="all", skip_digestion=False):
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
def get_entity_id_from_entity(item, indices="all", skip_digestion=False):
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
def get_entity_name_from_entity(item, indices="all", skip_digestion=False):
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
def get_entity_type_from_entity(item, indices="all", skip_digestion=False):
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
def get_chain_index_from_entity(item, indices="all", skip_digestion=False):
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
def get_chain_id_from_entity(item, indices="all", skip_digestion=False):
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
def get_chain_name_from_entity(item, indices="all", skip_digestion=False):
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
def get_chain_type_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_atoms_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_groups_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_components_from_entity(item, indices="all", skip_digestion=False):
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
    output = get_component_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]
    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_chains_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_entities_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_bonds_from_entity(item, indices="all", skip_digestion=False):
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
    output = get_bond_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices="all", skip_digestion=False):
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
    output = get_inner_bond_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_nucleotides_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_ions_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_waters_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_small_molecules_from_entity(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_small_molecules_from_entity as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_proteins_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_dnas_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_rnas_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_lipids_from_entity(item, indices="all", skip_digestion=False):
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
def get_n_polysaccharides_from_entity(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_polysaccharides_from_entity as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices="all", skip_digestion=False):
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
def get_atom_index_from_chain(item, indices="all", skip_digestion=False):
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
def get_atom_id_from_chain(item, indices="all", skip_digestion=False):
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
def get_atom_name_from_chain(item, indices="all", skip_digestion=False):
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
def get_atom_type_from_chain(item, indices="all", skip_digestion=False):
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
def get_group_index_from_chain(item, indices="all", skip_digestion=False):
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
def get_group_id_from_chain(item, indices="all", skip_digestion=False):
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
def get_group_name_from_chain(item, indices="all", skip_digestion=False):
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
def get_group_type_from_chain(item, indices="all", skip_digestion=False):
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
def get_component_index_from_chain(item, indices="all", skip_digestion=False):
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
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [sorted(ii) for ii in output]
    del chain_index_from_atom, component_index_from_atom, aux_dict
    return output


@arg_digest(form=form)
def get_component_id_from_chain(item, indices="all", skip_digestion=False):
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
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_id_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_id"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [component_id_from_component[sorted(ii)].tolist() for ii in output]
    del (
        chain_index_from_atom,
        component_index_from_atom,
        component_id_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_component_name_from_chain(item, indices="all", skip_digestion=False):
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
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_name_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_name"]
        .to_numpy()
    )
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            chain_index = chain_index_from_atom[atom_index]
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [component_name_from_component[sorted(ii)].tolist() for ii in output]
    del (
        chain_index_from_atom,
        component_index_from_atom,
        component_name_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_component_type_from_chain(item, indices="all", skip_digestion=False):
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
    chain_index_from_atom = item.topology.atoms["chain_index"].to_numpy()
    component_index_from_atom = item.chemical_states._get_component_indices().to_numpy()
    component_type_from_component = (
        item.chemical_states._resolve_chemical_state()
        .components["component_type"]
        .to_numpy()
    )
    item.topology.atoms.shape[0]
    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = list(aux_dict.values())
    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(component_index_from_atom[atom_index])
        output = [aux_dict[m] for m in indices]
    output = [component_type_from_component[sorted(ii)].tolist() for ii in output]
    del (
        chain_index_from_atom,
        component_index_from_atom,
        component_type_from_component,
        aux_dict,
    )
    return output


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices="all", skip_digestion=False):
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
def get_molecule_id_from_chain(item, indices="all", skip_digestion=False):
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
def get_molecule_name_from_chain(item, indices="all", skip_digestion=False):
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
def get_molecule_type_from_chain(item, indices="all", skip_digestion=False):
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
def get_entity_index_from_chain(item, indices="all", skip_digestion=False):
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
def get_entity_id_from_chain(item, indices="all", skip_digestion=False):
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
def get_entity_name_from_chain(item, indices="all", skip_digestion=False):
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
def get_entity_type_from_chain(item, indices="all", skip_digestion=False):
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
def get_chain_index_from_chain(item, indices="all", skip_digestion=False):
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
def get_chain_id_from_chain(item, indices="all", skip_digestion=False):
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
def get_chain_name_from_chain(item, indices="all", skip_digestion=False):
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
def get_chain_type_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_atoms_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_groups_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_components_from_chain(item, indices="all", skip_digestion=False):
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
    aux = get_component_index_from_chain(item, indices, skip_digestion=True)
    output = []
    for ii in aux:
        try:
            output.append(len(ii))
        except Exception:
            output.append(1)
    return output


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_chains_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_entities_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_bonds_from_chain(item, indices="all", skip_digestion=False):
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
    output = get_bond_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices="all", skip_digestion=False):
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
    output = get_bond_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]
    return output


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_nucleotides_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_ions_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_waters_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_small_molecules_from_chain(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_small_molecules_from_chain as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_proteins_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_dnas_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_rnas_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_lipids_from_chain(item, indices="all", skip_digestion=False):
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
def get_n_polysaccharides_from_chain(item, indices="all", skip_digestion=False):
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
    from molsysmt.form.molsysmt_Topology import (
        get_n_polysaccharides_from_chain as aux_get,
    )

    return aux_get(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices="all", skip_digestion=False):
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
        "molsysmt.form.molsysmt_Topology.get_topological_attributes"
    )
    function = getattr(topology_get, f"get_{attribute}_from_bond")
    return function(item.topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_index_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_id_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_id_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_order_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_type_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_fractional_bond_order_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_fractional_bond_order_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_is_aromatic_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_is_aromatic_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_is_conjugated_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_is_conjugated_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_stereochemistry_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_stereochemistry_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_stereo_atom_indices_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_stereo_atom_indices_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_donor_atom_index_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_donor_atom_index_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_acceptor_atom_index_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_acceptor_atom_index_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_joins_components_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_joins_components_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bond_evidence_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_evidence_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bonded_atoms_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices="all", skip_digestion=False):
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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bonded_atom_pairs_from_bond(
        item.chemical_states, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices="all", skip_digestion=False):
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
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        output = len(indices)
    return output


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
    return item.get_n_atoms()


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None or not item.chemical_states.n_chemical_states:
        return None
    return molsysmt_ChemicalStates.get_n_components_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None or not item.chemical_states.n_chemical_states:
        return None
    return molsysmt_ChemicalStates.get_n_bonds_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    from molsysmt.form.molsysmt_Topology import (
        get_n_small_molecules_from_system as aux_get,
    )

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
    from molsysmt.form.molsysmt_Topology import (
        get_n_polysaccharides_from_system as aux_get,
    )

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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bond_index_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    return get_bonded_atoms_from_bond(item, skip_digestion=True)


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_inner_bonded_atom_pairs_from_system(
        item.chemical_states, skip_digestion=True
    )


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
    return get_bonded_atoms_from_bond(item, skip_digestion=True)


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
    from molsysmt.form import molsysmt_ChemicalStates

    if item.chemical_states is None:
        return None
    return molsysmt_ChemicalStates.get_bonded_atom_pairs_from_system(
        item.chemical_states, skip_digestion=True
    )


@arg_digest(form=form)
def get_total_n_components_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n components from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_components_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_bonds_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n bonds from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices
    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n inner bonds from atom in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        bond_indices = get_inner_bond_index_from_atom(
            item, indices, skip_digestion=True
        )
        output = np.unique(np.concatenate(bond_indices)).size
        del bond_indices
    return output


@arg_digest(form=form)
def get_bond_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting bond index from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_group = get_atom_index_from_group(
        item, indices=indices, skip_digestion=True
    )
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_group:
        if len(jj):
            output.append(
                sorted(
                    set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
                )
            )
        else:
            output.append([])
    del atom_indices_from_group, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_bond_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting bond type from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)
    del bond_type, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bond_order_from_group(item, indices="all", skip_digestion=False):
    """
    Getting bond order from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)
    del bond_order, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_group(item, indices="all", skip_digestion=False):
    """
    Getting bonded atoms from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices="all", skip_digestion=False):
    """
    Getting bonded atom pairs from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting inner bond index from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_group = get_atom_index_from_group(
        item, indices=indices, skip_digestion=True
    )
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_group:
        aux = sorted(
            set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
        )
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:, 0], jj) & np.isin(pairs[:, 1], jj)
            aux = list(compress(aux, mask))
        else:
            aux = []
        output.append(aux)
    del atom_indices_from_group, bonded_atom_pairs, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atoms from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    output = []
    for ii, jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))
    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj
    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atom pairs from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_group(
        item, indices=indices, skip_digestion=True
    )
    if indices == "all":
        output = bonded_atom_pairs
    else:
        atom_indices = get_atom_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        output = []
        for ii, jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:, 0], ii) | np.isin(jj[:, 1], ii)
                output.append(jj[mask, :].tolist())
    return output


@arg_digest(form=form)
def get_total_n_components_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n components from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_group(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)
    return output


@arg_digest(form=form)
def get_total_n_bonds_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n bonds from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_bonds_from_atom(
            item, indices=atom_indices, skip_digestion=True
        )
        del atom_indices
    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n inner bonds from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    inner_bond_indices = get_inner_bond_index_from_group(
        item, indices=indices, skip_digestion=True
    )
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices
    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n inner bonds from group in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_inner_bonds_from_atom(
            item, indices=atom_indices, skip_digestion=True
        )
        del atom_indices
    return output


@arg_digest(form=form)
def get_bond_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting bond index from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_molecule = get_atom_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_molecule:
        if len(jj):
            output.append(
                sorted(
                    set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
                )
            )
        else:
            output.append([])
    del atom_indices_from_molecule, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_bond_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting bond type from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)
    del bond_type, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bond_order_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting bond order from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)
    del bond_order, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting bonded atoms from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting bonded atom pairs from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting inner bond index from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_molecule = get_atom_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_molecule:
        aux = sorted(
            set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
        )
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:, 0], jj) & np.isin(pairs[:, 1], jj)
            aux = list(compress(aux, mask))
        else:
            aux = []
        output.append(aux)
    del atom_indices_from_molecule, bonded_atom_pairs, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atoms from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    atom_indices = get_atom_index_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii, jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))
    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj
    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(
    item, indices="all", skip_digestion=False
):
    """
    Getting inner bonded atom pairs from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    if indices == "all":
        output = bonded_atom_pairs
    else:
        atom_indices = get_atom_index_from_molecule(
            item, indices=indices, skip_digestion=True
        )
        output = []
        for ii, jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:, 0], ii) | np.isin(jj[:, 1], ii)
                output.append(jj[mask, :].tolist())
    return output


@arg_digest(form=form)
def get_total_n_components_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n components from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_molecule(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)
    return output


@arg_digest(form=form)
def get_total_n_bonds_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n bonds from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n inner bonds from molecule in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_bond_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting bond index from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_entity = get_atom_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_entity:
        if len(jj):
            output.append(
                sorted(
                    set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
                )
            )
        else:
            output.append([])
    del atom_indices_from_entity, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_bond_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting bond type from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)
    del bond_type, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bond_order_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting bond order from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)
    del bond_order, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting bonded atoms from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting bonded atom pairs from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting inner bond index from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_entity = get_atom_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_entity:
        aux = sorted(
            set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
        )
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:, 0], jj) & np.isin(pairs[:, 1], jj)
            aux = list(compress(aux, mask))
        else:
            aux = []
        output.append(aux)
    del atom_indices_from_entity, bonded_atom_pairs, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atoms from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    atom_indices = get_atom_index_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii, jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))
    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj
    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atom pairs from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_entity(
        item, indices=indices, skip_digestion=True
    )
    if indices == "all":
        output = bonded_atom_pairs
    else:
        atom_indices = get_atom_index_from_entity(
            item, indices=indices, skip_digestion=True
        )
        output = []
        for ii, jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:, 0], ii) | np.isin(jj[:, 1], ii)
                output.append(jj[mask, :].tolist())
    return output


@arg_digest(form=form)
def get_total_n_components_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n components from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_entity(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)
    return output


@arg_digest(form=form)
def get_total_n_bonds_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n bonds from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n inner bonds from entity in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_bond_index_from_component(item, indices="all", skip_digestion=False):
    """
    Getting bond index from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_component = get_atom_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_component:
        if len(jj):
            output.append(
                sorted(
                    set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
                )
            )
        else:
            output.append([])
    del atom_indices_from_component, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_bond_type_from_component(item, indices="all", skip_digestion=False):
    """
    Getting bond type from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)
    del bond_type, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bond_order_from_component(item, indices="all", skip_digestion=False):
    """
    Getting bond order from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)
    del bond_order, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_component(item, indices="all", skip_digestion=False):
    """
    Getting bonded atoms from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices="all", skip_digestion=False):
    """
    Getting bonded atom pairs from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_component(item, indices="all", skip_digestion=False):
    """
    Getting inner bond index from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_component = get_atom_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_component:
        aux = sorted(
            set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
        )
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:, 0], jj) & np.isin(pairs[:, 1], jj)
            aux = list(compress(aux, mask))
        else:
            aux = []
        output.append(aux)
    del atom_indices_from_component, bonded_atom_pairs, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atoms from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    atom_indices = get_atom_index_from_component(
        item, indices=indices, skip_digestion=True
    )
    output = []
    for ii, jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))
    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj
    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_component(
    item, indices="all", skip_digestion=False
):
    """
    Getting inner bonded atom pairs from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_component(
        item, indices=indices, skip_digestion=True
    )
    if indices == "all":
        output = bonded_atom_pairs
    else:
        atom_indices = get_atom_index_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = []
        for ii, jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:, 0], ii) | np.isin(jj[:, 1], ii)
                output.append(jj[mask, :].tolist())
    return output


@arg_digest(form=form)
def get_total_n_atoms_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n atoms from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_component(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux
    return output


@arg_digest(form=form)
def get_total_n_groups_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n groups from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_group_index_from_component(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)
    return output


@arg_digest(form=form)
def get_total_n_molecules_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n molecules from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_molecules_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_entities_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n entities from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_entities_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_components_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n components from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_components_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_chains_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n chains from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_component(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)
    return output


@arg_digest(form=form)
def get_total_n_bonds_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n bonds from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n inner bonds from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n amino acids from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_amino_acids_from_system(item, skip_digestion=True)
    else:
        output = get_n_amino_acids_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n nucleotides from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_nucleotides_from_system(item, skip_digestion=True)
    else:
        output = get_n_nucleotides_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_ions_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n ions from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_ions_from_system(item, skip_digestion=True)
    else:
        output = get_n_ions_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_waters_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n waters from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_waters_from_system(item, skip_digestion=True)
    else:
        output = get_n_waters_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_component(
    item, indices="all", skip_digestion=False
):
    """
    Getting total n small molecules from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_small_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_n_small_molecules_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_lipids_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n lipids from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_lipids_from_system(item, skip_digestion=True)
    else:
        output = get_n_lipids_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n saccharides from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_saccharides_from_system(item, skip_digestion=True)
    else:
        output = get_n_saccharides_from_component(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)
    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_component(
    item, indices="all", skip_digestion=False
):
    """
    Getting total n polysaccharides from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_component(
        item, indices=indices, skip_digestion=True
    )


@arg_digest(form=form)
def get_total_n_peptides_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n peptides from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_peptides_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_proteins_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n proteins from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_proteins_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_dnas_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n dnas from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_dnas_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_total_n_rnas_from_component(item, indices="all", skip_digestion=False):
    """
    Getting total n rnas from component in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_bond_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting bond index from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_chain = get_atom_index_from_chain(
        item, indices=indices, skip_digestion=True
    )
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_chain:
        if len(jj):
            output.append(
                sorted(
                    set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
                )
            )
        else:
            output.append([])
    del atom_indices_from_chain, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_bond_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting bond type from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)
    del bond_type, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bond_order_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting bond order from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)
    del bond_order, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atoms_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting bonded atoms from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting bonded atom pairs from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)
    del bonded_atom_pairs, bond_indices, aux_vals, ii
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting inner bond index from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_indices_from_chain = get_atom_index_from_chain(
        item, indices=indices, skip_digestion=True
    )
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(
        item, indices="all", skip_digestion=True
    )
    output = []
    for jj in atom_indices_from_chain:
        aux = sorted(
            set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))
        )
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:, 0], jj) & np.isin(pairs[:, 1], jj)
            aux = list(compress(aux, mask))
        else:
            aux = []
        output.append(aux)
    del atom_indices_from_chain, bonded_atom_pairs, bond_indices_from_atom
    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atoms from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_chain(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    output = []
    for ii, jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))
    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj
    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting inner bonded atom pairs from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_chain(
        item, indices=indices, skip_digestion=True
    )
    if indices == "all":
        output = bonded_atom_pairs
    else:
        atom_indices = get_atom_index_from_chain(
            item, indices=indices, skip_digestion=True
        )
        output = []
        for ii, jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:, 0], ii) | np.isin(jj[:, 1], ii)
                output.append(jj[mask, :].tolist())
    return output


@arg_digest(form=form)
def get_total_n_components_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n components from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        aux = get_component_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)
    return output


@arg_digest(form=form)
def get_total_n_bonds_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n bonds from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n inner bonds from chain in form molsysmt.MolSys.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if indices == "all":
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_system(item, skip_digestion=False):
    """
    Getting inner bond index from system in form molsysmt.MolSys.


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
    return get_bond_index_from_bond(item, skip_digestion=True)


# List of functions to be imported


__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]


def _get_optional_bond_attribute(item, column, indices):
    """Return one nullable canonical bond column without inferring values."""
    bonds = item.chemical_states._get_chemical_state_bonds()
    n_values = len(bonds) if is_all(indices) else len(indices)
    if column not in bonds:
        return [None] * n_values
    values = bonds[column] if is_all(indices) else bonds.iloc[indices][column]
    return values.to_list()


def _get_optional_bond_attribute(item, column, indices):
    """Return one nullable canonical bond column without inferring values."""
    bonds = item.chemical_states._get_chemical_state_bonds()
    n_values = len(bonds) if is_all(indices) else len(indices)
    if column not in bonds:
        return [None] * n_values
    values = bonds[column] if is_all(indices) else bonds.iloc[indices][column]
    return values.to_list()
