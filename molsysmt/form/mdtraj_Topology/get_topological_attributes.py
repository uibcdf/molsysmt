#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################

from molsysmt._private.smonitor import NotImplementedMethodError, NotWithThisFormError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from networkx import Graph
import numpy as np
import pandas as pd
import types


form='mdtraj.Topology'


# -----------------------------------------------------------------------
# Private helpers — NOT exported (don't start with 'get_')
# -----------------------------------------------------------------------

def _count_group_type_per_element(item, element_group_indices, group_type_value):
    """Return per-element count of groups matching group_type_value.

    element_group_indices: list of lists (one inner list of group indices per element).
    """
    output = []
    for gidxs in element_group_indices:
        if gidxs:
            gtypes = get_group_type_from_group(item, indices=gidxs, skip_digestion=True)
            output.append(int((np.array(gtypes) == group_type_value).sum()))
        else:
            output.append(0)
    return output


def _count_molecule_type_per_element(item, element_molecule_indices, mol_type_value):
    """Return per-element count of molecules matching mol_type_value.

    element_molecule_indices: list of lists (one inner list of molecule indices per element).
    """
    output = []
    for midxs in element_molecule_indices:
        if midxs:
            mtypes = get_molecule_type_from_molecule(item, indices=midxs, skip_digestion=True)
            output.append(int((np.array(mtypes) == mol_type_value).sum()))
        else:
            output.append(0)
    return output


## From atom

@arg_digest(form=form)
def get_atom_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_atoms_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom id from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[str(item.atom(ii).serial) for ii in tmp_indices]
    return output


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom name from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).name for ii in tmp_indices]
    return output


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting atom type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output=[item.atom(ii).element.symbol for ii in tmp_indices]
    return output


@arg_digest(form=form)
def get_group_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output = [item.atom(ii).residue.index for ii in tmp_indices]
    return output


@arg_digest(form=form)
def get_group_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group id from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_group_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group name from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_group_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting group type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.component import get_component_index as _get

    return _get(item, element='atom', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_component_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component id from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component name from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting component type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.entity import get_entity_index as _get

    return _get(item, element='atom', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity id from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity name from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting entity type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_atom_index_from_atom(item, indices=indices, skip_digestion=True)
    output = [item.atom(ii).residue.chain.index for ii in tmp_indices]
    return output


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain id from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain name from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting chain type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

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
    Getting bond type from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_type_from_bond(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_order_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bond order from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_bond_order_from_bond(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bonded_atoms_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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

    if is_all(indices):

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
    Getting bonded atom pairs from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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

    if is_all(indices):

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
    Getting inner bond index from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    n_bonds = len(edges)
    edge_indices = np.array([{'index': ii} for ii in range(n_bonds)]).reshape([n_bonds, 1])
    G.add_edges_from(np.hstack([edges, edge_indices]))

    if is_all(indices):

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
    Getting inner bonded atoms from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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

    if not is_all(indices):

        G = G.subgraph(indices)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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

    if is_all(indices):

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
    Getting n atoms from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_atoms_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_groups_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n groups from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_components_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n components from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = get_component_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_entities_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n entities from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n chains from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_chains_from_system(item, skip_digestion=True)
    else:
        output = get_chain_index_from_atom(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_indices = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@arg_digest(form=form)
def get_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    bond_indices = get_inner_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    output = [len(ii) for ii in bond_indices]
    del bond_indices

    return output


@arg_digest(form=form)
def get_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n ions from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n waters from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'olicosaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_indices = get_group_index_from_atom(item, indices=indices, skip_digestion=True)
    group_indices = np.unique(group_indices)
    group_types = get_group_type_from_group(item, indices=group_indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_atom(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_atom(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From group


@arg_digest(form=form)
def get_atom_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_group_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_atom_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom id from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom name from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting atom type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_groups_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_group_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group id from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = np.arange(n_indices)

    output = [str(item.residue(ii).resSeq) for ii in indices]
    return output

@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group name from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_indices = get_n_groups_from_system(item, skip_digestion=True)
        indices = np.arange(n_indices)

    output = [item.residue(ii).name for ii in indices]
    return output

@arg_digest(form=form)
def get_group_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting group type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.group import get_group_type_from_group_name as aux_get

    output = get_group_name_from_group(item, indices=indices, skip_digestion=True)
    output = [aux_get(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_component_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_component_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_component_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component id from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component name from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_component_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting component type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_component_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_entity_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity id from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity name from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting entity type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_group(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain id from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain name from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_chain_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting chain type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_group(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond type from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bond order from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_group(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()



@arg_digest(form=form)
def get_n_atoms_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_groups_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n groups from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_groups_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_components_from_group(item, indices='all', skip_digestion=False):

    # Each group belongs to exactly one component
    """
    Getting n components from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    n = get_n_groups_from_system(item, skip_digestion=True) if is_all(indices) else len(indices)
    return [1] * n


@arg_digest(form=form)
def get_n_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_entities_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n entities from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_group(item, indices='all', skip_digestion=False):

    # Each group belongs to exactly one chain
    """
    Getting n chains from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    n = get_n_groups_from_system(item, skip_digestion=True) if is_all(indices) else len(indices)
    return [1] * n


@arg_digest(form=form)
def get_n_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n amino acids from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n nucleotides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n ions from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n waters from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n small molecules from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n lipids from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n polysaccharides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n saccharides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_group(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_group(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From component


@arg_digest(form=form)
def get_atom_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_component_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_atom_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom id from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom name from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting atom type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_component_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_group_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group id from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group name from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting group type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_components_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_component_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component id from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_component_index_from_component(item, indices=indices, skip_digestion=True)

    return output

@arg_digest(form=form)
def get_component_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component name from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_component_index_from_component(item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_component_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting component type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.component import get_component_type as _get

    return _get(item, element='component', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_molecule_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_molecule_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_molecule_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_molecule_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_entity_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity id from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity name from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting entity type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_component(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain id from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain name from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_chain_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting chain type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_component(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond type from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bond order from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_component(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_groups_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n groups from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_components_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n components from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_components_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_molecules_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_component(item, indices='all', skip_digestion=False):

    # Each component belongs to exactly one chain
    """
    Getting n chains from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    n = get_n_components_from_system(item, skip_digestion=True) if is_all(indices) else len(indices)
    return [1] * n


@arg_digest(form=form)
def get_n_entities_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n entities from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_component(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n amino acids from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'amino acid')


@arg_digest(form=form)
def get_n_nucleotides_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n nucleotides from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'nucleotide')


@arg_digest(form=form)
def get_n_ions_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n ions from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'ion')


@arg_digest(form=form)
def get_n_waters_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n waters from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'water')


@arg_digest(form=form)
def get_n_small_molecules_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n small molecules from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'small molecule')


@arg_digest(form=form)
def get_n_lipids_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n lipids from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'lipid')


@arg_digest(form=form)
def get_n_polysaccharides_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n polysaccharides from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'polysaccharide')


@arg_digest(form=form)
def get_n_saccharides_from_component(item, indices='all', skip_digestion=False):
    """
    Getting n saccharides from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_component(item, indices=indices, skip_digestion=True), 'saccharide')


@arg_digest(form=form)
def get_n_peptides_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n peptides from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n proteins from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n dnas from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_component(item, indices='all', skip_digestion=False):

    """
    Getting n rnas from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    molecule_indices = get_molecule_index_from_component(item, indices=indices, skip_digestion=True)
    molecule_indices = np.unique(molecule_indices)
    molecule_types = get_molecule_type_from_molecule(item, indices=molecule_indices, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


## From molecule


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_molecule_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_atom_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom id from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom name from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting atom type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_molecule_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_group_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group id from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group name from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting group type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_molecule_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_component_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component id from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component name from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting component type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_molecules_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.molecule import get_molecule_id as _get

    return _get(item, element='molecule', selection=indices, redefine_indices=True, skip_digestion=True)

@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.molecule import get_molecule_name as _get

    return _get(item, element='molecule', selection=indices, redefine_indices=True, skip_digestion=True)

@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.molecule import get_molecule_type as _get

    return _get(item, element='molecule', selection=indices, redefine_indices=True, skip_digestion=True)


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_entity_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity id from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity name from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting entity type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_molecule(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain id from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain name from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting chain type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond type from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bond order from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_groups_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n groups from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_components_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n components from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_molecules_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_entities_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n entities from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(item, indices=indices, skip_digestion=True)
        output = np.unique(output).shape[0]

    return output


@arg_digest(form=form)
def get_n_chains_from_molecule(item, indices='all', skip_digestion=False):

    # Each molecule belongs to exactly one chain
    """
    Getting n chains from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    n = get_n_molecules_from_system(item, skip_digestion=True) if is_all(indices) else len(indices)
    return [1] * n


@arg_digest(form=form)
def get_n_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_molecule(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n amino acids from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'amino acid')


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n nucleotides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'nucleotide')


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n ions from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'ion')


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n waters from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'water')


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n small molecules from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'small molecule')


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n lipids from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'lipid')


@arg_digest(form=form)
def get_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n polysaccharides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    mol_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    return int(sum(1 for t in mol_types if t == 'polysaccharide'))


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n saccharides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_molecule(item, indices=indices, skip_digestion=True), 'saccharide')


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n peptides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    mol_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    return int(sum(1 for t in mol_types if t == 'peptide'))


@arg_digest(form=form)
def get_n_proteins_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n proteins from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    mol_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    return int(sum(1 for t in mol_types if t == 'protein'))


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n dnas from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    mol_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    return int(sum(1 for t in mol_types if t == 'dna'))


@arg_digest(form=form)
def get_n_rnas_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting n rnas from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    mol_types = get_molecule_type_from_molecule(item, indices=indices, skip_digestion=True)
    return int(sum(1 for t in mol_types if t == 'rna'))


## From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_entity_index_from_atom(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_atom_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom id from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom name from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting atom type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_entity_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_group_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group id from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group name from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting group type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_entity_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_component_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component id from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component name from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting component type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_entity_index_from_molecule(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_molecule_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_molecule_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_entities_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity id from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.entity import get_entity_id as _get

    return _get(item, element='entity', selection=indices, redefine_indices=True, skip_digestion=True)

@arg_digest(form=form)
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity name from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.entity import get_entity_name as _get

    return _get(item, element='entity', selection=indices, redefine_indices=True, skip_digestion=True)

@arg_digest(form=form)
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting entity type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.entity import get_entity_type as _get

    return _get(item, element='entity', selection=indices, redefine_types=True, skip_digestion=True)

@arg_digest(form=form)
def get_chain_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_index_from_target = get_atom_index_from_entity(item, indices=indices, skip_digestion=True)
    first_atom_index_from_target = np.array([ii[0] for ii in atom_index_from_target])
    output = get_chain_index_from_atom(item, indices=first_atom_index_from_target, skip_digestion=True)

    del atom_index_from_target, first_atom_index_from_target

    return output


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain id from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_id_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain name from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting chain type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    aux_indices = get_chain_index_from_entity(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_new_indices = np.unique(aux_indices, return_inverse=True)
    aux_vals = get_chain_type_from_chain(item, indices=aux_unique_indices, skip_digestion=True)
    output = np.array(aux_vals)[aux_new_indices]

    del aux_indices, aux_unique_indices, aux_vals, aux_new_indices

    return output.tolist()


@arg_digest(form=form)
def get_bond_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond type from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bond order from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n groups from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_components_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n components from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_entities_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n entities from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_chains_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n chains from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    n = get_n_entities_from_system(item, skip_digestion=True) if is_all(indices) else len(indices)
    return [1] * n


@arg_digest(form=form)
def get_n_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_entity(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n amino acids from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'amino acid')


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n nucleotides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'nucleotide')


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n ions from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'ion')


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n waters from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'water')


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n small molecules from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'small molecule')


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n lipids from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'lipid')


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n polysaccharides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'polysaccharide')


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n saccharides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_entity(item, indices=indices, skip_digestion=True), 'saccharide')


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n peptides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_entity(item, indices=indices, skip_digestion=True), 'peptide')


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n proteins from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_entity(item, indices=indices, skip_digestion=True), 'protein')


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n dnas from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_entity(item, indices=indices, skip_digestion=True), 'dna')


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n rnas from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_entity(item, indices=indices, skip_digestion=True), 'rna')


## From chain


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_chain_index_from_atom(item)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_atom_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom id from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_id_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom name from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_name_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_atom_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting atom type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_atom_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_atom_type_from_atom(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_chain_index_from_group(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_group_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group id from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_id_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group name from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_name_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_group_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting group type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_group_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_group_type_from_group(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_chain_index_from_component(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_component_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component id from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_id_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component name from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_name_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_component_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting component type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_component_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_component_type_from_component(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_chain_index_from_molecule(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_molecule_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule id from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_id_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule name from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_name_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_molecule_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting molecule type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_molecule_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_molecule_type_from_molecule(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_index = get_chain_index_from_entity(item, skip_digestion=True)

    serie = pd.Series(target_index)
    groups_serie = serie.groupby(serie).apply(lambda x: x.index.tolist())
    if is_all(indices):
        output = [ii for ii in groups_serie]
    else:
        output = [groups_serie[ii] for ii in indices]

    return output


@arg_digest(form=form)
def get_entity_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity id from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_entity_id_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_entity_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity name from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_entity_name_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_entity_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting entity type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    target_indices = get_entity_index_from_chain(item, indices=indices, skip_digestion=True)
    aux_unique_indices, aux_indices = np.unique(np.concatenate(target_indices), return_inverse=True)
    aux_vals = get_entity_type_from_entity(item, indices=aux_unique_indices, skip_digestion=True)
    aux_output = np.array(aux_vals)[aux_indices]
    output = []
    ii = 0
    for aux in target_indices:
        jj = ii+len(aux)
        output.append(aux_output[ii:jj].tolist())
        ii = jj

    del aux_unique_indices, aux_vals, aux_output, target_indices

    return output


@arg_digest(form=form)
def get_chain_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_chains_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain id from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    chains = list(item.chains)
    if is_all(indices):
        output = [chain.chain_id for chain in chains]
    else:
        output = [chains[ii].chain_id for ii in indices]
    del chains

    return output


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain name from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting chain type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.element.chain import get_chain_type

    return get_chain_type(item, element='chain', selection=indices, redefine_types=True)


@arg_digest(form=form)
def get_bond_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond type from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_order_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bond order from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bond_index_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bond index from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atoms from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting inner bonded atom pairs from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n atoms from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n groups from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_components_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n components from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_component_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_molecules_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n molecules from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_entities_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n entities from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_n_chains_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n chains from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        output = get_n_chains_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_n_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_inner_bonds_from_chain(item, indices='all', skip_digestion=False):

    """
    Getting n inner bonds from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n amino acids from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'amino acid')


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n nucleotides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'nucleotide')


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n ions from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'ion')


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n waters from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'water')


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n small molecules from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'small molecule')


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n lipids from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'lipid')


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n polysaccharides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'polysaccharide')


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n saccharides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_group_type_per_element(item,
        get_group_index_from_chain(item, indices=indices, skip_digestion=True), 'saccharide')


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n peptides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_chain(item, indices=indices, skip_digestion=True), 'peptide')


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n proteins from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_chain(item, indices=indices, skip_digestion=True), 'protein')


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n dnas from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_chain(item, indices=indices, skip_digestion=True), 'dna')


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n rnas from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _count_molecule_type_per_element(item,
        get_molecule_index_from_chain(item, indices=indices, skip_digestion=True), 'rna')


## From bond


@arg_digest(form=form)
def get_bond_index_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond index from bond in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_bonds_from_system(item)
        output = np.arange(n_aux, dtype=int).tolist()
    else:
        output = indices.tolist()

    return output


@arg_digest(form=form)
def get_bond_order_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond order from bond in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bond_type_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bond type from bond in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    raise NotImplementedMethodError()


@arg_digest(form=form)
def get_bonded_atoms_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atoms from bond in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_bond_index_from_bond(item, indices=indices, skip_digestion=True)
    bond_list = list(item.bonds)
    atom_set = set()
    for ii in tmp_indices:
        atom_set.add(bond_list[ii].atom1.index)
        atom_set.add(bond_list[ii].atom2.index)
    return sorted(atom_set)


@arg_digest(form=form)
def get_bonded_atom_pairs_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting bonded atom pairs from bond in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    tmp_indices = get_bond_index_from_bond(item, indices=indices, skip_digestion=True)
    bond_list = list(item.bonds)
    output = [[bond_list[ii].atom1.index, bond_list[ii].atom2.index] for ii in tmp_indices]
    return output


@arg_digest(form=form)
def get_n_bonds_from_bond(item, indices='all', skip_digestion=False):

    """
    Getting n bonds from bond in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        n_aux = get_n_bonds_from_system(item, skip_digestion=True)
        output = list(range(n_aux))
    else:
        output = indices

    return output


## From system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):

    """
    Getting n atoms from system in form mdtraj.Topology.


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
    return item.n_atoms


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):

    """
    Getting n groups from system in form mdtraj.Topology.


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
    return item.n_residues


@arg_digest(form=form)
def get_n_components_from_system(item, skip_digestion=False):

    """
    Getting n components from system in form mdtraj.Topology.


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
    component_index_from_atom = get_component_index_from_atom(item, indices='all', skip_digestion=True)

    if component_index_from_atom[0] is None:
        return 0

    return int(np.unique(component_index_from_atom).shape[0])


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):

    """
    Getting n molecules from system in form mdtraj.Topology.


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
    molecule_index_from_atom = get_molecule_index_from_atom(item, indices='all', skip_digestion=True)

    if molecule_index_from_atom[0] is None:
        return 0

    return int(np.unique(molecule_index_from_atom).shape[0])


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):

    """
    Getting n entities from system in form mdtraj.Topology.


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
    entity_index_from_atom = get_entity_index_from_atom(item, indices='all', skip_digestion=True)

    if entity_index_from_atom[0] is None:
        return 0

    return int(np.unique(entity_index_from_atom).shape[0])


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):

    """
    Getting n chains from system in form mdtraj.Topology.


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
    return item.n_chains


@arg_digest(form=form)
def get_n_bonds_from_system(item, skip_digestion=False):

    """
    Getting n bonds from system in form mdtraj.Topology.


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
    return item.n_bonds


@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):

    """
    Getting n amino acids from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'amino acid').sum()

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):

    """
    Getting n nucleotides from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'nucleotide').sum()

    return output


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):

    """
    Getting n ions from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'ion').sum()

    return output


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):

    """
    Getting n waters from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'water').sum()

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):

    """
    Getting n small molecules from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'small molecule').sum()

    return output


@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):

    """
    Getting n lipids from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'lipid').sum()

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):

    """
    Getting n polysaccharides from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'polysaccharide').sum()

    return output


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):

    """
    Getting n saccharides from system in form mdtraj.Topology.


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
    group_types = get_group_type_from_group(item, skip_digestion=True)
    output = (np.array(group_types) == 'saccharide').sum()

    return output


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):

    """
    Getting n peptides from system in form mdtraj.Topology.


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
    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'peptide').sum()

    return output


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):

    """
    Getting n proteins from system in form mdtraj.Topology.


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
    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'protein').sum()

    return output


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):

    """
    Getting n dnas from system in form mdtraj.Topology.


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
    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'dna').sum()

    return output


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):

    """
    Getting n rnas from system in form mdtraj.Topology.


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
    molecule_types = get_molecule_type_from_molecule(item, skip_digestion=True)
    output = (np.array(molecule_types) == 'rna').sum()

    return output


@arg_digest(form=form)
def get_bond_index_from_system(item, skip_digestion=False):

    """
    Getting bond index from system in form mdtraj.Topology.


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
    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    output = list(range(n_bonds))

    return output


@arg_digest(form=form)
def get_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting bonded atoms from system in form mdtraj.Topology.


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
    Getting bonded atom pairs from system in form mdtraj.Topology.


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
    output = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
   
    return output


@arg_digest(form=form)
def get_inner_bond_index_from_system(item, skip_digestion=False):

    """
    Getting inner bond index from system in form mdtraj.Topology.


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
    n_bonds = get_n_bonds_from_system(item, skip_digestion=True)
    output = list(range(n_bonds))

    return output


@arg_digest(form=form)
def get_inner_bonded_atoms_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atoms from system in form mdtraj.Topology.


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
    output = None

    G = Graph()
    edges = get_bonded_atom_pairs_from_bond(item, skip_digestion=True)
    
    G.add_edges_from(edges)

    output = []
    for nodo in G.nodes():
        output.append(list(G.neighbors(nodo)))

    del G, edges

    return output


@arg_digest(form=form)
def get_inner_bonded_atom_pairs_from_system(item, skip_digestion=False):

    """
    Getting inner bonded atom pairs from system in form mdtraj.Topology.


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
    output = get_bonded_atom_pairs_from_bond(item)
   
    return output


## get_total_n_* functions
## Return the total count within the scope defined by the queried indices.
## Each function delegates to the per-element getter and sums or counts
## appropriately depending on how the element hierarchy relates to Y.

# --- From atom ---

@arg_digest(form=form)
def get_total_n_atoms_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n atoms from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_groups_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n groups from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_components_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n components from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_total_n_molecules_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n molecules from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_entities_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n entities from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_chains_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n chains from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_bonds_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n bonds from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    per_atom = get_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    unique_bonds = set()
    for bond_list in per_atom:
        unique_bonds.update(bond_list)
    return len(unique_bonds)

@arg_digest(form=form)
def get_total_n_inner_bonds_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n inner bonds from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    per_atom = get_inner_bond_index_from_atom(item, indices=indices, skip_digestion=True)
    unique_bonds = set()
    for bond_list in per_atom:
        unique_bonds.update(bond_list)
    return len(unique_bonds)

@arg_digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n amino acids from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_nucleotides_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n nucleotides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_ions_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n ions from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_waters_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n waters from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_small_molecules_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n small molecules from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_lipids_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n lipids from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_saccharides_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n saccharides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_peptides_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n peptides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_proteins_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n proteins from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_polysaccharides_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n polysaccharides from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_atom(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n dnas from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_rnas_from_atom(item, indices='all', skip_digestion=False):
    """
    Getting total n rnas from atom in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_atom(item, indices=indices, skip_digestion=True)


# --- From group ---

@arg_digest(form=form)
def get_total_n_atoms_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n atoms from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_atoms_from_group(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n groups from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_components_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n components from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return len(set(get_component_index_from_group(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n molecules from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_entities_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n entities from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_chains_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n chains from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return len(set(get_chain_index_from_group(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_amino_acids_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n amino acids from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_nucleotides_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n nucleotides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_ions_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n ions from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_waters_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n waters from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_small_molecules_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n small molecules from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_lipids_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n lipids from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_saccharides_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n saccharides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_peptides_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n peptides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_proteins_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n proteins from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_polysaccharides_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n polysaccharides from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_group(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n dnas from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_rnas_from_group(item, indices='all', skip_digestion=False):
    """
    Getting total n rnas from group in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_group(item, indices=indices, skip_digestion=True)


# --- From molecule ---

@arg_digest(form=form)
def get_total_n_atoms_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n atoms from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n groups from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_groups_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n components from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_components_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n molecules from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_entities_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n entities from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_chains_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n chains from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return len(set(get_chain_index_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n amino acids from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_amino_acids_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n nucleotides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_nucleotides_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_ions_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n ions from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_ions_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_waters_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n waters from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_waters_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_lipids_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n lipids from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_lipids_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n saccharides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_saccharides_from_molecule(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_peptides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n peptides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_peptides_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_proteins_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n proteins from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_proteins_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_polysaccharides_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n polysaccharides from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_polysaccharides_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_dnas_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n dnas from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_dnas_from_molecule(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_rnas_from_molecule(item, indices='all', skip_digestion=False):
    """
    Getting total n rnas from molecule in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_rnas_from_molecule(item, indices=indices, skip_digestion=True)


# --- From entity ---

@arg_digest(form=form)
def get_total_n_atoms_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n atoms from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_atoms_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n groups from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_groups_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n components from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_components_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n molecules from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_molecules_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_entities_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n entities from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_entities_from_entity(item, indices=indices, skip_digestion=True)

@arg_digest(form=form)
def get_total_n_chains_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n chains from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return len(set(get_chain_index_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n amino acids from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_amino_acids_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_nucleotides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n nucleotides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_nucleotides_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_ions_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n ions from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_ions_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_waters_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n waters from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_waters_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_lipids_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n lipids from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_lipids_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_saccharides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n saccharides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_saccharides_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_peptides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n peptides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_peptides_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_proteins_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n proteins from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_proteins_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_polysaccharides_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n polysaccharides from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_polysaccharides_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_dnas_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n dnas from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_dnas_from_entity(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_rnas_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting total n rnas from entity in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_rnas_from_entity(item, indices=indices, skip_digestion=True)))


# --- From component ---

@arg_digest(form=form)
def get_total_n_atoms_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n atoms from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_atoms_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n groups from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_groups_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n components from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_total_n_molecules_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n molecules from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_total_n_entities_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n entities from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_total_n_chains_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n chains from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return len(set(get_chain_index_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_amino_acids_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n amino acids from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_amino_acids_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_nucleotides_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n nucleotides from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_nucleotides_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_ions_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n ions from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_ions_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_waters_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n waters from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_waters_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_lipids_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n lipids from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_lipids_from_component(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_saccharides_from_component(item, indices='all', skip_digestion=False):
    """
    Getting total n saccharides from component in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_saccharides_from_component(item, indices=indices, skip_digestion=True)))


# --- From chain ---

@arg_digest(form=form)
def get_total_n_atoms_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n atoms from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_atoms_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_groups_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n groups from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_groups_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_components_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n components from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_components_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_molecules_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n molecules from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_molecules_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_entities_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n entities from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_entities_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_chains_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n chains from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_total_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n amino acids from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_amino_acids_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_nucleotides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n nucleotides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_nucleotides_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_ions_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n ions from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_ions_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_waters_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n waters from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_waters_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_lipids_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n lipids from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_lipids_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_saccharides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n saccharides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_saccharides_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_polysaccharides_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n polysaccharides from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_polysaccharides_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_dnas_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n dnas from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_dnas_from_chain(item, indices=indices, skip_digestion=True)))

@arg_digest(form=form)
def get_total_n_rnas_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting total n rnas from chain in form mdtraj.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return int(sum(get_n_rnas_from_chain(item, indices=indices, skip_digestion=True)))


# List of functions to be imported

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]

