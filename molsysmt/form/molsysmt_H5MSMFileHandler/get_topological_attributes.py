from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np
import pandas as pd
from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
import types
from networkx import Graph
from collections import defaultdict
from itertools import chain, compress

form='molsysmt.H5MSMFileHandler'


def _get_atom_state_attribute(item, attribute, indices='all'):
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from molsysmt.form.molsysmt_Topology import get_topological_attributes

    topology = to_molsysmt_Topology(item, skip_digestion=True)
    function = getattr(
        get_topological_attributes, f'get_{attribute}_from_atom'
    )
    return function(topology, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting formal charge from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    Getting formal charge from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
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
    Getting atom is aromatic from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    Getting n unpaired electrons from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    Getting n implicit hydrogens from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    Getting allows implicit hydrogens from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    Getting atom stereochemistry from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_atom_state_attribute(item, 'atom_stereochemistry', indices)


def _get_state_metadata(item):
    if item.format_version == '0.3':
        membership = item.file['topology']['atoms']['component_index'][:]
        component_completeness = 'partial' if np.any(membership < 0) else 'complete'
        return {
            'chemical_state_index': [0],
            'chemical_state_id': [None],
            'n_chemical_states': 1,
            'reference_chemical_state_index': 0,
            'connectivity_completeness': ['complete'],
            'component_completeness': [component_completeness],
            'component_evidence': ['unknown'],
        }

    states = item.file['topology']['chemical_states']
    n_states = int(states.attrs['n_chemical_states'])
    reference_index = int(states.attrs['reference_chemical_state_index'])
    state_groups = [states[str(index)] for index in range(n_states)]
    return {
        'chemical_state_index': list(range(n_states)),
        'chemical_state_id': [group.attrs.get('state_id') for group in state_groups],
        'n_chemical_states': n_states,
        'reference_chemical_state_index': None if reference_index < 0 else reference_index,
        'connectivity_completeness': [
            group.attrs['connectivity_completeness'] for group in state_groups
        ],
        'component_completeness': [
            group.attrs['component_completeness'] for group in state_groups
        ],
        'component_evidence': [group.attrs['component_evidence'] for group in state_groups],
    }


def _get_state_metadata_attribute(item, attribute):
    return _get_state_metadata(item)[attribute]


@arg_digest(form=form)
def get_chemical_state_index_from_system(item, skip_digestion=False):
    """
    Getting chemical state index from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'chemical_state_index')


@arg_digest(form=form)
def get_chemical_state_id_from_system(item, skip_digestion=False):
    """
    Getting chemical state id from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'chemical_state_id')


@arg_digest(form=form)
def get_n_chemical_states_from_system(item, skip_digestion=False):
    """
    Getting n chemical states from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'n_chemical_states')


@arg_digest(form=form)
def get_reference_chemical_state_index_from_system(item, skip_digestion=False):
    """
    Getting reference chemical state index from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'reference_chemical_state_index')


@arg_digest(form=form)
def get_connectivity_completeness_from_system(item, skip_digestion=False):
    """
    Getting connectivity completeness from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'connectivity_completeness')


@arg_digest(form=form)
def get_component_completeness_from_system(item, skip_digestion=False):
    """
    Getting component completeness from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'component_completeness')


@arg_digest(form=form)
def get_component_evidence_from_system(item, skip_digestion=False):
    """
    Getting component evidence from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return _get_state_metadata_attribute(item, 'component_evidence')

#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_atoms_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom id from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['atoms']['atom_id'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['atom_id'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom name from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['atoms']['atom_name'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['atom_name'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['atoms']['atom_type'][:].astype('str')
    else:
        output = item.file['topology']['atoms']['atom_type'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_isotope_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting isotope from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atoms = item.file['topology']['atoms']
    if 'isotope' not in atoms:
        n_values = get_n_atoms_from_system(item, skip_digestion=True)
        values = np.zeros(n_values, dtype=np.uint16)
        if indices != 'all':
            values = values[indices]
    elif indices == 'all':
        values = atoms['isotope'][:]
    else:
        values = atoms['isotope'][indices]

    return [None if value == 0 else int(value) for value in values]


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['atoms']['group_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['group_index'][indices].astype('int')

    return output.tolist()


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group id from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_id_from_group = item.file['topology']['groups']['group_id'][:].astype('str')

    if indices=='all':
        output = group_id_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output = group_id_from_group[aux].tolist()

    del group_index_from_atom, group_id_from_group

    return output


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group name from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_name_from_group = item.file['topology']['groups']['group_name'][:].astype('str')

    if indices=='all':
        output = group_name_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output = group_name_from_group[aux].tolist()

    del group_index_from_atom, group_name_from_group

    return output


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_type_from_group = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = group_type_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output = group_type_from_group[aux].tolist()

    del group_index_from_atom, group_type_from_group

    return output


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom].tolist()
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux].tolist()
        del aux

    del group_index_from_atom, molecule_index_from_group

    return output


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_id_from_molecule = item.file['topology']['molecules']['molecule_id'][:].astype('str')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = molecule_id_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_name_from_molecule = item.file['topology']['molecules']['molecule_name'][:].astype('str')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = molecule_name_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_type_from_molecule = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = molecule_type_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity id from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_id_from_entity = item.file['topology']['entities']['entity_id'][:].astype('str')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output]
    output = entity_id_from_entity[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity name from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_name_from_entity = item.file['topology']['entities']['entity_name'][:].astype('str')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output]
    output = entity_name_from_entity[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_type_from_entity = item.file['topology']['entities']['entity_type'][:].astype('str')

    if indices == 'all':
        output = molecule_index_from_group[group_index_from_atom]
    else:
        aux = group_index_from_atom[indices]
        output  = molecule_index_from_group[aux]
        del aux

    output = entity_index_from_molecule[output]
    output = entity_type_from_entity[output].tolist()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['atoms']['component_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['component_index'][indices].astype('int')

    return output.tolist()


@arg_digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component id from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_id_from_component = item.file['topology']['components']['component_id'][:].astype('str')

    if indices=='all':
        output = component_id_from_component[component_index_from_atom].tolist()
    else:
        aux = component_index_from_atom[indices]
        output = component_id_from_component[aux].tolist()

    del component_index_from_atom, component_id_from_component

    return output


@arg_digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component name from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_name_from_component =  item.file['topology']['components']['component_name'][:].astype('str')

    if indices=='all':
        output = component_name_from_component[component_index_from_atom].tolist()
    else:
        aux = component_index_from_atom[indices]
        output = component_name_from_component[aux].tolist()

    del component_index_from_atom, component_name_from_component

    return output


@arg_digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_type_from_component =  item.file['topology']['components']['component_type'][:].astype('str')

    if indices=='all':
        output = component_type_from_component[component_index_from_atom].tolist()
    else:
        aux = component_index_from_atom[indices]
        output = component_type_from_component[aux].tolist()

    del component_index_from_atom, component_type_from_component

    return output


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['atoms']['chain_index'][:].astype('int')
    else:
        output = item.file['topology']['atoms']['chain_index'][indices].astype('int')

    return output.tolist()


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain id from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_id_from_chain =  item.file['topology']['chains']['chain_id'][:].astype('str')

    if indices=='all':
        output = chain_id_from_chain[chain_index_from_atom].tolist()
    else:
        aux = chain_index_from_atom[indices]
        output = chain_id_from_chain[aux].tolist()

    del chain_index_from_atom, chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain name from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_name_from_chain =  item.file['topology']['chains']['chain_name'][:].astype('str')

    if indices=='all':
        output = chain_name_from_chain[chain_index_from_atom].tolist()
    else:
        aux = chain_index_from_atom[indices]
        output = chain_name_from_chain[aux].tolist()

    del chain_index_from_atom, chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_type_from_chain =  item.file['topology']['chains']['chain_type'][:].astype('str')

    if indices=='all':
        output = chain_type_from_chain[chain_index_from_atom].tolist()
    else:
        aux = chain_index_from_atom[indices]
        output = chain_type_from_chain[aux].tolist()

    del chain_index_from_atom, chain_type_from_chain

    return output


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices=='all':

        indices = get_atom_index_from_atom(item, skip_digestion=True)

    output = []

    for ii in indices:
        if ii in G:
            output.append([n['index'] for n in G[ii].values()])
        else:
            output.append([])

    del G, edges, edge_indices

    return output


@arg_digest(form=form)
def get_bond_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond type from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    values = get_bond_type_from_bond(item, skip_digestion=True)
    return [[values[bond_index] for bond_index in atom_bonds] for atom_bonds in aux_indices]


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond order from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    aux_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    values = get_bond_order_from_bond(item, skip_digestion=True)
    return [[values[bond_index] for bond_index in atom_bonds] for atom_bonds in aux_indices]


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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

    if indices=='all':

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
def get_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = None

    if indices=='all':

        output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) | np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if indices=='all':

        indices = get_atom_index_from_atom(item, skip_digestion=True)

    else:

        G = G.subgraph(indices)

    output = []

    for ii in indices:
        if ii in G:
            output.append([n['index'] for n in G[ii].values()])
        else:
            output.append([])

    del G, edges, edge_indices

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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

    if not indices=='all':

        G = G.subgraph(indices)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = None

    if indices=='all':

        output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    else:

        pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
        pairs = np.array(pairs)
        mask = np.isin(pairs[:,0], indices) * np.isin(pairs[:,1], indices)
        output = pairs[mask,:].tolist()

        del pairs, mask

    return output


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_atoms_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n groups from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_groups_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_groups_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_molecules_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n entities from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_entities_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n components from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_components_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n components from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n chains from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_chains_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_chains_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).shape[0]
        del bond_indices

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    inner_bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        bond_indices = get_inner_bond_index_from_atom(item, indices, skip_digestion=True)
        output = np.unique(np.concatenate(bond_indices)).size
        del bond_indices

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='amino acid')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='amino acid')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_amino_acids_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='nucleotide')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='nucleotide')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_nucleotides_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n ions from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='ion')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='ion')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_ions_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_ions_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n waters from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='water')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='water')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_waters_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_waters_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='small molecule')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='small molecule')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_small_molecules_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='lipid')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='lipid')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_lipids_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_type_from_groups = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(group_type_from_groups=='saccharide')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        output = np.count_nonzero(group_type_from_groups[aux]=='saccharide')
        del group_indices_from_atoms, aux

    del group_type_from_groups

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_saccharides_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_type_from_molecules = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='peptide')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        molecule_indices_from_groups = item.file['topology']['groups']['molecule_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='peptide')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_peptides_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_type_from_molecules = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='protein')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        molecule_indices_from_groups = item.file['topology']['groups']['molecule_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='protein')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_proteins_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_type_from_molecules = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='dna')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        molecule_indices_from_groups = item.file['topology']['groups']['molecule_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='dna')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_dnas_from_atom(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_type_from_molecules = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='rna')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        molecule_indices_from_groups = item.file['topology']['groups']['molecule_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='rna')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_atom(item, indices=indices, skip_digestion=True)



@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_type_from_molecules = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices=='all':
        output = np.count_nonzero(molecule_type_from_molecules=='polysaccharide')
    else:
        group_indices_from_atoms = item.file['topology']['atoms']['group_index'][:].astype('int')
        molecule_indices_from_groups = item.file['topology']['groups']['molecule_index'][:].astype('int')
        aux = np.unique(group_indices_from_atoms[indices])
        aux = np.unique(molecule_indices_from_groups[aux])
        output = np.count_nonzero(molecule_type_from_molecules[aux]=='polysaccharide')
        del group_indices_from_atoms, molecule_indices_from_groups, aux

    del molecule_type_from_molecules

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from atom in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_atom(item, indices=indices, skip_digestion=True)


## From group


@arg_digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom id from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    atom_id_from_atom = item.file['topology']['atoms']['atom_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom name from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    atom_name_from_atom = item.file['topology']['atoms']['atom_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    atom_type_from_atom = item.file['topology']['atoms']['atom_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_groups_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group id from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['groups']['group_id'][:].astype('str')
    else:
        output = item.file['topology']['groups']['group_id'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group name from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['groups']['group_name'][:].astype('str')
    else:
        output = item.file['topology']['groups']['group_name'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['groups']['group_type'][:].astype('str')
    else:
        output = item.file['topology']['groups']['group_type'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')

    if indices=='all':
        output = molecule_index_from_group.tolist()
    else:
        output = molecule_index_from_group[indices].tolist()

    del molecule_index_from_group

    return output


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_id_from_molecule = item.file['topology']['molecules']['molecule_id'][:].astype('str')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_id_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_name_from_molecule = item.file['topology']['molecules']['molecule_name'][:].astype('str')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_name_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_type_from_molecule = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_type_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity id from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_id_from_entity = item.file['topology']['entities']['entity_id'][:].astype('str')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_id_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity name from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_name_from_entity = item.file['topology']['entities']['entity_name'][:].astype('str')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_name_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_type_from_entity = item.file['topology']['entities']['entity_type'][:].astype('str')

    if indices=='all':
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_type_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')

    if indices =='all':

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

    del group_index_from_atom, component_index_from_atom, aux_dict

    output = [ next(iter(ii)) if len(ii) == 1 else list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component id from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_id_from_component = item.file['topology']['components']['component_id'][:].astype('str')

    if indices =='all':

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

    output = [ component_id_from_component[next(iter(ii))] if len(ii) == 1 else
               component_id_from_component[list(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, component_id_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component name from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_name_from_component = item.file['topology']['components']['component_name'][:].astype('str')

    if indices =='all':

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

    output = [ component_name_from_component[next(iter(ii))] if len(ii) == 1 else
               component_name_from_component[list(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_type_from_component = item.file['topology']['components']['component_type'][:].astype('str')

    if indices =='all':

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

    output = [ component_type_from_component[next(iter(ii))] if len(ii) == 1 else
               component_type_from_component[list(ii)].tolist() for ii in output]

    del group_index_from_atom, component_index_from_atom, component_type_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, chain_index_from_atom, aux_dict

    output = [ next(iter(ii)) if len(ii) == 1 else list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain id from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_id_from_chain =  item.file['topology']['chains']['chain_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_id_from_chain[next(iter(ii))] if len(ii) == 1 else
               chain_id_from_chain[list(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain name from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_name_from_chain = item.file['topology']['chains']['chain_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_name_from_chain[next(iter(ii))] if len(ii) == 1 else
               chain_name_from_chain[list(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_type_from_chain = item.file['topology']['chains']['chain_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, group_index in enumerate(group_index_from_atom):
            aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, group_index in enumerate(group_index_from_atom):
            if group_index in aux_dict:
                aux_dict[group_index].add(chain_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ chain_type_from_chain[next(iter(ii))] if len(ii) == 1 else
               chain_type_from_chain[list(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_group = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_group:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_group, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond type from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond order from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_group = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_group:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_group, bonded_atom_pairs, bond_indices_from_atom, pairs

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_group(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_atom_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_group(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n groups from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_groups_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_molecules_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n entities from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_entities_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n components from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_components_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n components from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
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
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n chains from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_chain_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_group(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_indices = get_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@arg_digest(form=form)
def get_total_n_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_bonds_from_atom(item, indices=atom_indices, skip_digestion=True)
        del atom_indices

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    inner_bond_indices = get_inner_bond_index_from_group(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in inner_bond_indices]
    del inner_bond_indices

    return output


@arg_digest(form=form)
def get_total_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
        atom_indices = list(chain.from_iterable(atom_indices))
        output = get_total_n_inner_bonds_from_atom(item, indices=atom_indices, skip_digestion=True)
        del atom_indices

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('amino acid')

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_amino_acids_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('nucleotide')

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_nucleotides_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n ions from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('ion')

    return output


@arg_digest(form=form)
def get_total_n_ions_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_ions_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n waters from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('water')

    return output


@arg_digest(form=form)
def get_total_n_waters_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_waters_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('small molecule')

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_small_molecules_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('lipid')

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_lipids_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count('saccharide')

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_saccharides_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_peptides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('peptide')

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_peptides_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_proteins_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('protein')

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_proteins_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_dnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('dna')

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_dnas_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_rnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('rna')

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_group(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_polysaccharides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('polysaccharide')

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from group in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_group(item, indices=indices, skip_digestion=True)


## From molecule


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group =  item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, molecule_index_from_group, molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom id from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group =  item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    atom_id_from_atom = item.file['topology']['atoms']['atom_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in sorted(aux_dict.keys())]

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom name from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group =  item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    atom_name_from_atom = item.file['topology']['atoms']['atom_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict[m] for m in sorted(aux_dict.keys())]

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group =  item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    atom_type_from_atom = item.file['topology']['atoms']['atom_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict[m] for m in sorted(aux_dict.keys())]

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_index)

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group id from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    group_id_from_group = item.file['topology']['groups']['group_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_id_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_id_from_group[group_index])

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, group_id_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group name from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    group_name_from_group = item.file['topology']['groups']['group_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_name_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_name_from_group[group_index])

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, group_name_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    group_type_from_group = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            aux_dict[molecule_index].append(group_type_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, molecule_index in enumerate(molecule_index_from_group):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(group_type_from_group[group_index])

        output = [aux_dict[m] for m in indices]

    del molecule_index_from_group, group_type_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_molecules_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['molecules']['molecule_id'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['molecule_id'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['molecules']['molecule_name'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['molecule_name'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['molecules']['molecule_type'][:].astype('str')
    else:
        output = item.file['topology']['molecules']['molecule_type'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')

    if indices=='all':
        output = entity_index_from_molecule.tolist()
    else:
        output = entity_index_from_molecule[indices].tolist()

    del entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity id from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_id_from_entity = item.file['topology']['entities']['entity_id'][:].astype('str')

    if indices=='all':
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_id_from_entity[output].tolist()

    del entity_index_from_molecule, entity_id_from_entity

    return output

@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity name from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_name_from_entity = item.file['topology']['entities']['entity_name'][:].astype('str')

    if indices=='all':
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_name_from_entity[output].tolist()

    del entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_type_from_entity = item.file['topology']['entities']['entity_type'][:].astype('str')

    if indices=='all':
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_type_from_entity[output].tolist()

    del entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')

    if indices =='all':

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

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@arg_digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component id from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_id_from_component = item.file['topology']['components']['component_id'][:].astype('str')

    if indices =='all':

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

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, component_id_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component name from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_name_from_component = item.file['topology']['components']['component_name'][:].astype('str')

    if indices =='all':

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

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_type_from_component = item.file['topology']['components']['component_type'][:].astype('str')

    if indices =='all':

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

    output = [component_type_from_component[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, component_index_from_atom, component_type_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index_from_atom[atom_index]].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain id from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_id_from_chain =  item.file['topology']['chains']['chain_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_id_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain name from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_name_from_chain = item.file['topology']['chains']['chain_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_name_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_type_from_chain = item.file['topology']['chains']['chain_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_type_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii))
        for ii in output
    ]

    return output


@arg_digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_molecule = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_molecule:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_molecule, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond type from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond order from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_molecule = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_molecule:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_molecule, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_molecule(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_molecule(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_atom_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n groups from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_group_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_n_groups_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_molecules_from_molecule(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n entities from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_entities_from_molecule(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n components from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_components_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n components from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
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
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n chains from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_chain_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_molecule(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False): 

    """
    Getting n bonds from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_molecule(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n ions from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n waters from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('peptide')

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_n_peptides_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('protein')

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_n_proteins_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('polysaccharide')

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_n_polysaccharides_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('dna')

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_n_dnas_from_molecule(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    output = molecule_types.count('rna')

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from molecule in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_n_rnas_from_molecule(item, indices=indices, skip_digestion=True)

    return output


## From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom id from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_id_from_atom = item.file['topology']['atoms']['atom_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom name from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_name_from_atom = item.file['topology']['atoms']['atom_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom =  item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_type_from_atom = item.file['topology']['atoms']['atom_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_index)

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group id from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]
    group_id_from_group = item.file['topology']['groups']['group_id'][:].astype('str')

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_id_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_id_from_group[group_index])

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group name from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]
    group_name_from_group = item.file['topology']['groups']['group_name'][:].astype('str')

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_name_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_name_from_group[group_index])

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    entity_index_from_group   = entity_index_from_molecule[molecule_index_from_group]
    group_type_from_group = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices == 'all':

        aux_dict = defaultdict(list)
        for group_index, entity_index in enumerate(entity_index_from_group):
            aux_dict[entity_index].append(group_type_from_group[group_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for group_index, entity_index in enumerate(entity_index_from_group):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(group_type_from_group[group_index])

        output = [aux_dict[ii] for ii in indices]

    del molecule_index_from_group, entity_index_from_molecule, entity_index_from_group, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_index)

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_id_from_molecule = item.file['topology']['molecules']['molecule_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_id_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_id_from_molecule[molecule_index])

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_name_from_molecule = item.file['topology']['molecules']['molecule_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_name_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_name_from_molecule[molecule_index])

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_type_from_molecule = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_type_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(molecule_type_from_molecule[molecule_index])

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_entities_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity id from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['entities']['entity_id'][:].astype('str')
    else:
        output = item.file['topology']['entities']['entity_id'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity name from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['entities']['entity_name'][:].astype('str')
    else:
        output = item.file['topology']['entities']['entity_name'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['entities']['entity_type'][:].astype('str')
    else:
        output = item.file['topology']['entities']['entity_type'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')

    if indices =='all':

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
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@arg_digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component id from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_id_from_component = item.file['topology']['components']['component_id'][:].astype('str')

    if indices =='all':

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
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict
    del component_id_from_component

    return output


@arg_digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component name from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_name_from_component = item.file['topology']['components']['component_name'][:].astype('str')

    if indices =='all':

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
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict
    del component_name_from_component

    return output


@arg_digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_type_from_component = item.file['topology']['components']['component_type'][:].astype('str')

    if indices =='all':

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
    del molecule_index_from_atom, entity_index_from_atom, component_index_from_atom, aux_dict
    del component_type_from_component

    return output


@arg_digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict

    output = [list(np.unique(ii)) for ii in output] 

    return output


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain id from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_id_from_chain =  item.file['topology']['chains']['chain_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_id_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict
    del chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain name from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_name_from_chain = item.file['topology']['chains']['chain_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_name_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict
    del chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom     = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_type_from_chain = item.file['topology']['chains']['chain_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, entity_index in enumerate(entity_index_from_atom):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(chain_index_from_atom[atom_index])

        output = [aux_dict[ii] for ii in indices]

    output = [chain_type_from_chain[np.unique(ii)].tolist() for ii in output] 

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule
    del molecule_index_from_atom, entity_index_from_atom, chain_index_from_atom, aux_dict
    del chain_type_from_chain

    return output


@arg_digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_entity = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_entity:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_entity, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond type from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond order from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_entity = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_entity:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_entity, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_entity(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_entity(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_atom_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n groups from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_group_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_n_groups_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_molecule_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        aux = get_n_molecules_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n entities from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_entities_from_molecule(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n components from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_components_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n components from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
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
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n chains from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_chain_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        aux = get_chain_index_from_entity(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_bonds_from_system(item, skip_digestion=True)

    else:

        atom_indices = get_atom_index_from_entity(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n ions from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n waters from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('peptide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_peptides_from_system(item, skip_digestion=True)

    else:

        output = get_n_peptides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('protein') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_proteins_from_system(item, skip_digestion=True)

    else:

        output = get_n_proteins_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('polysaccharide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_polysaccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_polysaccharides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('dna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_dnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_dnas_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ ii.count('rna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from entity in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_rnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_rnas_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


## From component


@arg_digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, component_index in enumerate(component_index_from_atom):
            aux_dict[component_index].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, component_index in enumerate(component_index_from_atom):
            if component_index in aux_dict:
                aux_dict[component_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del component_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom id from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    atom_id_from_atom = item.file['topology']['atoms']['atom_id'][:].astype('str')

    if indices =='all':

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
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom name from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    atom_name_from_atom = item.file['topology']['atoms']['atom_name'][:].astype('str')

    if indices =='all':

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
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    atom_type_from_atom = item.file['topology']['atoms']['atom_type'][:].astype('str')

    if indices =='all':

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
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')

    if indices =='all':

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

    del group_index_from_atom, component_index_from_atom, aux_dict

    output = [list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group id from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_id_from_group = item.file['topology']['groups']['group_id'][:].astype('str')

    if indices =='all':

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
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group name from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_name_from_group = item.file['topology']['groups']['group_name'][:].astype('str')

    if indices =='all':

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
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_type_from_group = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices =='all':

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
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    if indices =='all':

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

    output = [ next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_id_from_molecule = item.file['topology']['molecules']['molecule_id'][:].astype('str')

    if indices =='all':

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

    output = [ molecule_id_from_molecule[next(iter(ii))] if len(ii) == 1 else molecule_id_from_molecule[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_id_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_name_from_molecule = item.file['topology']['molecules']['molecule_name'][:].astype('str')

    if indices =='all':

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

    output = [ molecule_name_from_molecule[next(iter(ii))] if len(ii) == 1 else molecule_name_from_molecule[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_name_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_type_from_molecule = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices =='all':

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

    output = [ molecule_type_from_molecule[next(iter(ii))] if len(ii) == 1 else molecule_type_from_molecule[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_type_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

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

    output = [ next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]

    del component_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity id from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_id_from_entity = item.file['topology']['entities']['entity_id'][:].astype('str')

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

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

    output = [ entity_id_from_entity[next(iter(ii))] if len(ii) == 1 else entity_id_from_entity[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, entity_index_from_atom, entity_id_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity name from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_name_from_entity = item.file['topology']['entities']['entity_name'][:].astype('str')

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

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

    output = [ entity_name_from_entity[next(iter(ii))] if len(ii) == 1 else entity_name_from_entity[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, entity_index_from_atom, entity_name_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_type_from_entity = item.file['topology']['entities']['entity_type'][:].astype('str')

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

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

    output = [ entity_type_from_entity[next(iter(ii))] if len(ii) == 1 else entity_type_from_entity[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, entity_index_from_atom, entity_type_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_components_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component id from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['components']['component_id'][:].astype('str')
    else:
        output = item.file['topology']['components']['component_id'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component name from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['components']['component_name'][:].astype('str')
    else:
        output = item.file['topology']['components']['component_name'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['components']['component_type'][:].astype('str')
    else:
        output = item.file['topology']['components']['component_type'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')

    if indices =='all':

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

    output = [ next(iter(ii)) if len(ii) == 1 else sorted(ii) for ii in output]

    del component_index_from_atom, chain_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain id from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_id_from_chain =  item.file['topology']['chains']['chain_id'][:].astype('str')

    if indices =='all':

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

    output = [ chain_id_from_chain[next(iter(ii))] if len(ii) == 1 else chain_id_from_chain[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain name from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_name_from_chain = item.file['topology']['chains']['chain_name'][:].astype('str')

    if indices =='all':

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

    output = [ chain_name_from_chain[next(iter(ii))] if len(ii) == 1 else chain_name_from_chain[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    chain_type_from_chain = item.file['topology']['chains']['chain_type'][:].astype('str')

    if indices =='all':

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

    output = [ chain_type_from_chain[next(iter(ii))] if len(ii) == 1 else chain_type_from_chain[sorted(ii)].tolist() for ii in output]

    del component_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_component = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_component:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_component, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond type from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_type = get_bond_type_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_type[jj] for jj in ii]
        output.append(aux_vals)

    del bond_type, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond order from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bond_order = get_bond_order_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bond_order[jj] for jj in ii]
        output.append(aux_vals)

    del bond_order, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals))))

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii in bond_indices:
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(aux_vals)

    del bonded_atom_pairs, bond_indices, aux_vals, ii

    return output


@arg_digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_component = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_component:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_component, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices = get_bond_index_from_component(item, indices=indices, skip_digestion=True)
    atom_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)

    output = []
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_component(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_atom_index_from_component(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_component(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n groups from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_groups_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
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
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n entities from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n components from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_components_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n components from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n chains from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_chains_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
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
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_component(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n ions from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n waters from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_component(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_component(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_polysaccharides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('polysaccharide')

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_component(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_peptides_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('peptide')

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_proteins_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('protein')

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_dnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('dna')

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_rnas_from_system(item, skip_digestion=True)
    else:
        molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        molecule_indices = np.unique(molecule_indices).tolist()
        molecule_type = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
        output = molecule_type.count('rna')

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from component in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_component(item, indices=indices, skip_digestion=True)


## From chain


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index_from_atom[atom_index]].append(atom_index)

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_index)

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom id from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    atom_id_from_atom = item.file['topology']['atoms']['atom_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_id_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_id_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, atom_id_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom name from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    atom_name_from_atom = item.file['topology']['atoms']['atom_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, atom_name_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    atom_type_from_atom = item.file['topology']['atoms']['atom_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(list)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: [] for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del chain_index_from_atom, atom_type_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, chain_index_from_atom, aux_dict

    output = [list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group id from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_id_from_group = item.file['topology']['groups']['group_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_id_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, group_id_from_group
    del aux_dict

    return output

@arg_digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group name from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_name_from_group = item.file['topology']['groups']['group_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_name_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, group_name_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    group_type_from_group = item.file['topology']['groups']['group_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [group_type_from_group[sorted(ii)].tolist() for ii in output]

    del group_index_from_atom, chain_index_from_atom, group_type_from_group
    del aux_dict

    return output


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [sorted(ii) for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_id_from_molecule = item.file['topology']['molecules']['molecule_id'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_id_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_id_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_name_from_molecule = item.file['topology']['molecules']['molecule_name'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_name_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_name_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    molecule_type_from_molecule = item.file['topology']['molecules']['molecule_type'][:].astype('str')

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ molecule_type_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_type_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [ sorted(ii) for ii in output]

    del chain_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity id from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_id_from_entity = item.file['topology']['entities']['entity_id'][:].astype('str')

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [entity_id_from_entity[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, entity_index_from_atom, entity_id_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity name from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_name_from_entity = item.file['topology']['entities']['entity_name'][:].astype('str')

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [entity_name_from_entity[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, entity_index_from_atom, entity_name_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    group_index_from_atom = item.file['topology']['atoms']['group_index'][:].astype('int')
    molecule_index_from_group = item.file['topology']['groups']['molecule_index'][:].astype('int')
    entity_index_from_molecule = item.file['topology']['molecules']['entity_index'][:].astype('int')
    molecule_index_from_atom = molecule_index_from_group[group_index_from_atom]
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_type_from_entity = item.file['topology']['entities']['entity_type'][:].astype('str')

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices =='all':

        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = list(aux_dict.values())

    else:

        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index])

        output = [aux_dict[m] for m in indices]

    output = [entity_type_from_entity[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, entity_index_from_atom, entity_type_from_entity, aux_dict

    return output


@arg_digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')

    if indices =='all':

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
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component id from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_id_from_component = item.file['topology']['components']['component_id'][:].astype('str') 

    if indices =='all':

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

    del chain_index_from_atom, component_index_from_atom, component_id_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component name from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_name_from_component = item.file['topology']['components']['component_name'][:].astype('str') 

    if indices =='all':

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

    output = [component_name_from_component[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, component_index_from_atom, component_name_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.file['topology']['atoms']['chain_index'][:].astype('int')
    component_index_from_atom = item.file['topology']['atoms']['component_index'][:].astype('int')
    component_type_from_component = item.file['topology']['components']['component_type'][:].astype('str') 

    if indices =='all':

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

    del chain_index_from_atom, component_index_from_atom, component_type_from_component, aux_dict

    return output


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_chains_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain id from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output =  item.file['topology']['chains']['chain_id'][:].astype('str')
    else:
        output =  item.file['topology']['chains']['chain_id'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain name from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['chains']['chain_name'][:].astype('str')
    else:
        output = item.file['topology']['chains']['chain_name'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = item.file['topology']['chains']['chain_type'][:].astype('str')
    else:
        output = item.file['topology']['chains']['chain_type'][indices].astype('str')

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_chain = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_chain:
        if len(jj):
            output.append(sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj]))))
        else:
            output.append([])

    del atom_indices_from_chain, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond type from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond order from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    atom_indices_from_chain = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    bonded_atom_pairs = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    bond_indices_from_atom = get_bond_index_from_atom(item, indices='all', skip_digestion=True)

    output = []
    for jj in atom_indices_from_chain:
        aux = sorted(set(chain.from_iterable([bond_indices_from_atom[ii] for ii in jj])))
        if len(aux):
            pairs = np.array([bonded_atom_pairs[ii] for ii in aux])
            mask = np.isin(pairs[:,0], jj) & np.isin(pairs[:,1], jj)
            aux = list(compress(aux, mask))
        else:
            aux=[]
        output.append(aux)

    del atom_indices_from_chain, bonded_atom_pairs, bond_indices_from_atom

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
    for ii,jj in zip(bond_indices, atom_indices):
        aux_vals = [bonded_atom_pairs[jj] for jj in ii]
        output.append(sorted(set(chain.from_iterable(aux_vals)).intersection(set(jj))))

    del bonded_atom_pairs, bond_indices, atom_indices, aux_vals, ii, jj

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    bonded_atom_pairs = get_bonded_atom_pairs_from_chain(item, indices=indices, skip_digestion=True)

    if indices=='all':

        output = bonded_atom_pairs
    
    else:

        atom_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)

        output = []

        for ii,jj in zip(atom_indices, bonded_atom_pairs):
            if len(jj) == 0:
                output.append([])
            else:
                jj = np.array(jj)
                mask = np.isin(jj[:,0], ii) | np.isin(jj[:,1], ii)
                output.append(jj[mask,:].tolist())

    return output


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_atom_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n atoms from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        aux = get_n_atoms_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n groups from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n groups from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        aux = get_group_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n molecules from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        aux = get_molecule_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output


@arg_digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n entities from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_entities_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n entities from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        aux = get_entity_index_from_chain(item, indices, skip_digestion=True)
        output = set()
        for ii in aux:
            if isinstance(ii, list):
                output.update(ii)
            else:
                output.add(ii)
        output = len(output)

    return output

@arg_digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n components from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_components_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n components from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
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
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n chains from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n chains from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_n_chains_from_chain(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n bonds from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
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
def get_total_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n inner bonds from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        atom_indices = get_atom_index_from_chain(item, indices, skip_digestion=True)
        indices = np.concatenate(atom_indices).tolist()
        output = get_total_n_inner_bonds_from_atom(item, indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('amino acid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n amino acids from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_amino_acids_from_system(item, skip_digestion=True)

    else:

        output = get_n_amino_acids_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('nucleotide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n nucleotides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_nucleotides_from_system(item, skip_digestion=True)

    else:

        output = get_n_nucleotides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n ions from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('ion') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n ions from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_ions_from_system(item, skip_digestion=True)

    else:

        output = get_n_ions_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n waters from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('water') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n waters from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_waters_from_system(item, skip_digestion=True)

    else:

        output = get_n_waters_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('small molecule') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n small molecules from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_small_molecules_from_system(item, skip_digestion=True)

    else:

        output = get_n_small_molecules_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('lipid') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n lipids from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_lipids_from_system(item, skip_digestion=True)

    else:

        output = get_n_lipids_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('saccharide') for ii in group_types ]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n saccharides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_saccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_saccharides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('polysaccharide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n polysaccharides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_polysaccharides_from_system(item, skip_digestion=True)

    else:

        output = get_n_polysaccharides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('peptide') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n peptides from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_peptides_from_system(item, skip_digestion=True)

    else:

        output = get_n_peptides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('protein') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n proteins from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_proteins_from_system(item, skip_digestion=True)

    else:

        output = get_n_proteins_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('dna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n dnas from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_dnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_dnas_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = get_molecule_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ ii.count('rna') for ii in molecule_types ]

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting total n rnas from chain in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':

        output = get_n_rnas_from_system(item, skip_digestion=True)

    else:

        output = get_n_rnas_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


## From bond


def _get_v04_bond_attribute(item, attribute, indices):
    """Read a canonical 0.4 bond attribute without rebuilding a topology."""

    from molsysmt._private.smonitor import StructuralInconsistencyError

    states = item.file['topology']['chemical_states']
    reference_index = int(states.attrs['reference_chemical_state_index'])
    if reference_index < 0:
        raise StructuralInconsistencyError(
            reason='The H5MSM topology has no reference chemical state.',
            caller='molsysmt.form.molsysmt_H5MSMFileHandler.get',
        )
    bonds = states[str(reference_index)]['bonds']
    storage_names = {
        'bond_is_aromatic': 'is_aromatic',
        'bond_is_conjugated': 'is_conjugated',
        'bond_stereochemistry': 'stereochemistry',
        'bond_donor_atom_index': 'donor_atom_index',
        'bond_acceptor_atom_index': 'acceptor_atom_index',
        'bond_joins_components': 'joins_components',
        'bond_evidence': 'evidence',
    }

    if attribute == 'bond_stereo_atom_indices':
        atom1 = _get_v04_bond_column(bonds, 'stereo_atom1_index', indices)
        atom2 = _get_v04_bond_column(bonds, 'stereo_atom2_index', indices)
        return [[value1, value2] for value1, value2 in zip(atom1, atom2)]
    return _get_v04_bond_column(bonds, storage_names.get(attribute, attribute), indices)


def _get_v04_bond_column(bonds, name, indices):
    """Read one nullable bond column from a version 0.4 state group."""

    n_bonds = len(bonds['atom1_index'])
    selected = np.arange(n_bonds, dtype=np.int64) if is_all(indices) else np.asarray(indices)
    if name not in bonds:
        return [None] * len(selected)

    dataset = bonds[name]
    values = dataset.asstr()[:] if dataset.dtype.kind in {'O', 'S', 'U'} else dataset[:]
    null_name = f'{name}__is_null'
    nulls = bonds[null_name][:].astype(bool) if null_name in bonds else np.zeros(n_bonds, dtype=bool)
    output = []
    for index in selected:
        if nulls[index]:
            output.append(None)
        else:
            value = values[index]
            output.append(value.item() if isinstance(value, np.generic) else value)
    return output


def _missing_bond_attribute(item, indices, pair=False):
    n_values = get_n_bonds_from_system(item, skip_digestion=True) if is_all(indices) else len(indices)
    return [[None, None] for _ in range(n_values)] if pair else [None] * n_values


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond index from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_bond_id_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond id from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_id', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond order from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_order', indices)

    if 'order' in item.file['topology']['bonds']:
        if  item.file['topology']['bonds']['order'].size > 0:
            if indices=='all':
                output = item.file['topology']['bonds']['order'][:].astype('str').tolist()
            else:
                output = item.file['topology']['bonds']['order'][indices].astype('str').tolist()
            return [None if value == '<NA>' else value for value in output]

    if indices=='all':
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        return [None] * n_aux
    else:
        return [None] * len(indices)


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond type from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_type', indices)

    if 'type' in item.file['topology']['bonds']:
        if  item.file['topology']['bonds']['type'].size > 0:
            if indices=='all':
                output = item.file['topology']['bonds']['type'][:].astype('str').tolist()
            else:
                output = item.file['topology']['bonds']['type'][indices].astype('str').tolist()
            return [None if value == '<NA>' else value for value in output]

    if indices=='all':
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        return [None] * n_aux
    else:
        return [None] * len(indices)


@arg_digest(form=form)
def get_fractional_bond_order_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting fractional bond order from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'fractional_bond_order', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_is_aromatic_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond is aromatic from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_is_aromatic', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_is_conjugated_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond is conjugated from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_is_conjugated', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_stereochemistry_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond stereochemistry from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_stereochemistry', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_stereo_atom_indices_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond stereo atom indices from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_stereo_atom_indices', indices)
    return _missing_bond_attribute(item, indices, pair=True)


@arg_digest(form=form)
def get_bond_donor_atom_index_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond donor atom index from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_donor_atom_index', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_acceptor_atom_index_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond acceptor atom index from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_acceptor_atom_index', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_joins_components_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond joins components from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_joins_components', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bond_evidence_from_bond(item, indices='all', skip_digestion=False):
    """
    Getting bond evidence from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if item.format_version == '0.4':
        return _get_v04_bond_attribute(item, 'bond_evidence', indices)
    return _missing_bond_attribute(item, indices)


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    tmp_out = None

    if indices=='all':

        atom1_index = item.file['topology']['bonds']['atom1_index'][:].astype('int')
        atom2_index = item.file['topology']['bonds']['atom2_index'][:].astype('int')

    else:

        atom1_index = item.file['topology']['bonds']['atom1_index'][indices].astype('int')
        atom2_index = item.file['topology']['bonds']['atom2_index'][indices].astype('int')

    tmp_out = np.unique([atom1_index, atom2_index]).tolist()

    return tmp_out


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    tmp_out = None

    if indices=='all':

        atom1_index = item.file['topology']['bonds']['atom1_index'][:].astype('int')
        atom2_index = item.file['topology']['bonds']['atom2_index'][:].astype('int')

    else:

        atom1_index = item.file['topology']['bonds']['atom1_index'][indices].astype('int')
        atom2_index = item.file['topology']['bonds']['atom2_index'][indices].astype('int')

    tmp_out = np.column_stack([atom1_index, atom2_index]).tolist()

    return tmp_out


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from bond in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    indices : str, list, tuple, or numpy.ndarray, default='all'
        0-based element indices to extract.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    if indices=='all':
        output = get_n_bonds_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


## From system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    """
    Getting n atoms from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_atoms']
    
    if output==0:
        output = item.file['structures'].attrs['n_atoms']

    return output


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    """
    Getting n groups from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_groups']

    return output


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    """
    Getting n molecules from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_molecules']

    return output


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    """
    Getting n entities from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_entities']

    return output


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    """
    Getting n components from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_components']

    return output


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    """
    Getting n chains from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_chains']

    return output

@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    """
    Getting n bonds from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    output = item.file['topology'].attrs['n_bonds']

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    """
    Getting n amino acids from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('amino acid')
    del group_types

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    """
    Getting n nucleotides from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('nucleotide')
    del group_types

    return output


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    """
    Getting n ions from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('ion')
    del group_types

    return output


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    """
    Getting n waters from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('water')
    del group_types

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    """
    Getting n small molecules from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('small molecule')
    del group_types

    return output


@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    """
    Getting n lipids from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('lipid')
    del group_types

    return output


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    """
    Getting n saccharides from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    group_types = item.file['topology']['groups']['group_type'][:].astype('str').tolist()
    output = group_types.count('saccharide')
    del group_types

    return output


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    """
    Getting n peptides from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = item.file['topology']['molecules']['molecule_type'][:].astype('str').tolist()
    output = molecule_types.count('peptide')
    del molecule_types

    return output


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    """
    Getting n proteins from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = item.file['topology']['molecules']['molecule_type'][:].astype('str').tolist()
    output = molecule_types.count('protein')
    del molecule_types

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    """
    Getting n polysaccharides from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = item.file['topology']['molecules']['molecule_type'][:].astype('str').tolist()
    output = molecule_types.count('polysaccharide')
    del molecule_types

    return output


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    """
    Getting n dnas from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = item.file['topology']['molecules']['molecule_type'][:].astype('str').tolist()
    output = molecule_types.count('dna')
    del molecule_types

    return output


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    """
    Getting n rnas from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    molecule_types = item.file['topology']['molecules']['molecule_type'][:].astype('str').tolist()
    output = molecule_types.count('rna')
    del molecule_types

    return output


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    """
    Getting bond index from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_bond_index_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atoms from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
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
    Getting inner bonded atom pairs from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_bonded_atom_pairs_from_bond(item, skip_digestion=True)


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting bonded atoms from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
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
    Getting bonded atom pairs from system in form molsysmt.H5MSMFileHandler.

    Parameters
    ----------
    item : molsysmt.H5MSMFileHandler
        Source item in molsysmt.H5MSMFileHandler form.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.

    .. versionadded:: 1.0.0
    """
    return get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
