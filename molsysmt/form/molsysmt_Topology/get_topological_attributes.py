import types
from collections import defaultdict

import numpy as np
import pandas as pd

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.native._chain_groups import (
    uses_declared_hierarchy as _uses_declared_hierarchy,
)
from molsysmt.native._group_hierarchy import project as _project_hierarchy
from molsysmt.native._topology_infer import (
    molecule_indices_from_atoms as _molecule_indices_from_atoms,
)

form = "molsysmt.Topology"

_PUBLIC_TO_NATIVE_ATOM_STATE = {
    "formal_charge": "formal_charge",
    "atom_is_aromatic": "is_aromatic",
    "n_unpaired_electrons": "n_unpaired_electrons",
    "n_implicit_hydrogens": "n_implicit_hydrogens",
    "n_explicit_hydrogens": "n_explicit_hydrogens",
    "allows_implicit_hydrogens": "allows_implicit_hydrogens",
    "atom_stereochemistry": "stereochemistry",
}


def _get_hierarchy_from_atom(item, level, attribute, indices):
    """Map nullable parent indices without assigning missing atoms to a group."""
    if level == "group" and item.n_groups == 0:
        return None
    if level in {"molecule", "entity"}:
        from molsysmt.native._topology_infer import molecule_indices_from_atoms

        parents = pd.Series(molecule_indices_from_atoms(item)).replace(-1, pd.NA)
    elif level == "chain":
        parents = item.atoms["chain_index"]
    else:
        parents = item.atoms["group_index"]
    if not is_all(indices):
        parents = parents.iloc[indices]
    if level == "entity":
        parents = parents.map(item.molecules["entity_index"])
    if attribute != "index":
        table = getattr(
            item,
            {
                "group": "groups",
                "molecule": "molecules",
                "entity": "entities",
                "chain": "chains",
            }[level],
        )
        parents = parents.map(table[level + "_" + attribute])
    return [
        None if pd.isna(value) else int(value) if attribute == "index" else value
        for value in parents
    ]


def _count_hierarchy_from_atom(item, level, indices):
    """Count declared selected memberships without counting missing parents."""
    if level == "chain":
        values = item.atoms["chain_index"].iloc[indices]
        return int(values.nunique(dropna=True))
    values = _get_hierarchy_from_atom(item, level, "index", indices)
    return len({value for value in (values or []) if value is not None})


def _count_typed_hierarchy_from_atom(item, level, kind, indices):
    """Count distinct declared parents of one type in the selected inventory."""
    table = item.groups if level == "group" else item.molecules
    values = table[level + "_type"].to_numpy()
    if not is_all(indices):
        mapped = _get_hierarchy_from_atom(item, level, "index", indices)
        parents = np.asarray(
            sorted({value for value in (mapped or []) if value is not None}), dtype=int
        )
        values = values[parents]
    return int(np.count_nonzero(values == kind))


#######################################################################
#                 To be customized for each form                      #
#######################################################################

# From atom


@arg_digest(form=form)
def get_atom_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom index from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = list(range(item.atoms.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom id from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_id_from_atom = item.atoms["atom_id"].to_numpy()

    if indices == "all":
        output = atom_id_from_atom.tolist()
    else:
        output = atom_id_from_atom[indices].tolist()

    del atom_id_from_atom

    return output


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom name from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_name_from_atom = item.atoms["atom_name"].to_numpy()

    if indices == "all":
        output = atom_name_from_atom.tolist()
    else:
        output = atom_name_from_atom[indices].tolist()

    del atom_name_from_atom

    return output


@arg_digest(form=form)
def get_atom_type_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting atom type from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    atom_type_from_atom = item.atoms["atom_type"].to_numpy()

    if indices == "all":
        output = atom_type_from_atom.tolist()
    else:
        output = atom_type_from_atom[indices].tolist()

    del atom_type_from_atom

    return output


@arg_digest(form=form)
def get_isotope_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting isotope from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    values = item.atoms["isotope"]
    values = values if is_all(indices) else values.iloc[indices]
    return values.to_list()


@arg_digest(form=form)
def get_group_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting group index from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()

    if indices == "all":
        output = group_index_from_atom.tolist()
    else:
        output = group_index_from_atom[indices].tolist()

    del group_index_from_atom

    return output


@arg_digest(form=form)
def get_group_id_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting group id from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list or None
        The group IDs mapped to selected atoms. Missing
        parent membership yields None per atom; no groups yields None.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "group", "id", indices)


@arg_digest(form=form)
def get_group_name_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting group name from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list or None
        The group names mapped to selected atoms. Missing
        parent membership yields None per atom; no groups yields None.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "group", "name", indices)


@arg_digest(form=form)
def get_group_type_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting group type from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list or None
        The group types mapped to selected atoms. Missing
        parent membership yields None per atom; no groups yields None.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "group", "type", indices)


@arg_digest(form=form)
def get_molecule_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "molecule", "index", indices)


@arg_digest(form=form)
def get_molecule_id_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting molecule id from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "molecule", "id", indices)


@arg_digest(form=form)
def get_molecule_name_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting molecule name from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "molecule", "name", indices)


@arg_digest(form=form)
def get_molecule_type_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting molecule type from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "molecule", "type", indices)


@arg_digest(form=form)
def get_entity_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting entity index from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "entity", "index", indices)


@arg_digest(form=form)
def get_entity_id_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting entity id from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "entity", "id", indices)


@arg_digest(form=form)
def get_entity_name_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting entity name from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "entity", "name", indices)


@arg_digest(form=form)
def get_entity_type_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting entity type from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "entity", "type", indices)


@arg_digest(form=form)
def get_chain_index_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting chain index from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list
        Atom-aligned chain positions as integers, with ``None`` for missing membership.


    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.atoms["chain_index"].to_numpy(
        dtype=object, na_value=None
    )

    if indices == "all":
        output = chain_index_from_atom.tolist()
    else:
        output = chain_index_from_atom[indices].tolist()

    del chain_index_from_atom

    return output


@arg_digest(form=form)
def get_chain_id_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting chain id from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "chain", "id", indices)


@arg_digest(form=form)
def get_chain_name_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting chain name from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "chain", "name", indices)


@arg_digest(form=form)
def get_chain_type_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting chain type from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return _get_hierarchy_from_atom(item, "chain", "type", indices)


@arg_digest(form=form)
def get_n_atoms_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = item.atoms.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n atoms from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_groups_from_atom(item, indices="all", skip_digestion=False):
    """Counting groups represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships represented by selected atoms.
        With all atoms, returns the complete declared group inventory size.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_groups_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        return len(item.groups)
    return _count_hierarchy_from_atom(item, "group", indices)


@arg_digest(form=form)
def get_total_n_groups_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n groups from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_molecules_from_atom(item, indices="all", skip_digestion=False):
    """Counting molecules represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared molecule memberships represented by selected atoms.
        With all atoms, returns the complete declared molecule inventory size.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_molecules_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        return len(item.molecules)
    return _count_hierarchy_from_atom(item, "molecule", indices)


@arg_digest(form=form)
def get_total_n_molecules_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n molecules from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_entities_from_atom(item, indices="all", skip_digestion=False):
    """Counting entities represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared entity memberships represented by selected atoms.
        With all atoms, returns the complete declared entity inventory size.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_entities_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        return len(item.entities)
    return _count_hierarchy_from_atom(item, "entity", indices)


@arg_digest(form=form)
def get_total_n_entities_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n entities from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_chains_from_atom(item, indices="all", skip_digestion=False):
    """Counting chains represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared chain memberships represented by selected atoms.
        With all atoms, returns the complete declared chain inventory size.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_chains_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    if is_all(indices):
        return len(item.chains)
    return _count_hierarchy_from_atom(item, "chain", indices)


@arg_digest(form=form)
def get_total_n_chains_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n chains from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_amino_acids_from_atom(item, indices="all", skip_digestion=False):
    """Counting amino acids represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing amino acids type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_amino_acids_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "amino acid", indices)


@arg_digest(form=form)
def get_total_n_amino_acids_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n amino acids from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_nucleotides_from_atom(item, indices="all", skip_digestion=False):
    """Counting nucleotides represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing nucleotides type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_nucleotides_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "nucleotide", indices)


@arg_digest(form=form)
def get_total_n_nucleotides_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n nucleotides from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_ions_from_atom(item, indices="all", skip_digestion=False):
    """Counting ions represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing ions type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_ions_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "ion", indices)


@arg_digest(form=form)
def get_total_n_ions_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n ions from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_waters_from_atom(item, indices="all", skip_digestion=False):
    """Counting waters represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing waters type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_waters_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "water", indices)


@arg_digest(form=form)
def get_total_n_waters_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n waters from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_small_molecules_from_atom(item, indices="all", skip_digestion=False):
    """Counting small molecules represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing small molecules type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_small_molecules_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "small molecule", indices)


@arg_digest(form=form)
def get_total_n_small_molecules_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n small molecules from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_lipids_from_atom(item, indices="all", skip_digestion=False):
    """Counting lipids represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing lipids type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_lipids_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "lipid", indices)


@arg_digest(form=form)
def get_total_n_lipids_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n lipids from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_saccharides_from_atom(item, indices="all", skip_digestion=False):
    """Counting saccharides represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared group memberships having the existing saccharides type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_saccharides_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "group", "saccharide", indices)


@arg_digest(form=form)
def get_total_n_saccharides_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n saccharides from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_peptides_from_atom(item, indices="all", skip_digestion=False):
    """Counting peptides represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared molecule memberships having the existing peptides type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_peptides_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "molecule", "peptide", indices)


@arg_digest(form=form)
def get_total_n_peptides_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n peptides from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_proteins_from_atom(item, indices="all", skip_digestion=False):
    """Counting proteins represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared molecule memberships having the existing proteins type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_proteins_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "molecule", "protein", indices)


@arg_digest(form=form)
def get_total_n_proteins_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n proteins from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_dnas_from_atom(item, indices="all", skip_digestion=False):
    """Counting dnas represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared molecule memberships having the existing dnas type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_dnas_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "molecule", "dna", indices)


@arg_digest(form=form)
def get_total_n_dnas_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n dnas from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_rnas_from_atom(item, indices="all", skip_digestion=False):
    """Counting rnas represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared molecule memberships having the existing rnas type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_rnas_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "molecule", "rna", indices)


@arg_digest(form=form)
def get_total_n_rnas_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n rnas from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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


@arg_digest(form=form)
def get_n_polysaccharides_from_atom(item, indices="all", skip_digestion=False):
    """Counting polysaccharides represented by selected atoms.

    Parameters
    ----------
    item : molecular system
        Native Topology supplying the atom inventory and declared parent links.
    indices : str or list of int, default='all'
        Source atom indices to inspect. Repetitions do not duplicate a parent
        count; an empty list represents no memberships. 'all' uses the full
        declared inventory.
    skip_digestion : bool, default=False
        Whether to skip digestion of already validated arguments.

    Returns
    -------
    int
        Distinct declared molecule memberships having the existing polysaccharides type.
        With all atoms, counts matching rows in the complete declared table.
        Missing parent links contribute zero and are never used as array indices.

    Notes
    -----
    Counts use explicit hierarchy and existing type assignments. They do not
    infer missing groups, molecules or chemical classifications.

    Examples
    --------
    >>> from molsysmt.native import Topology
    >>> get_n_polysaccharides_from_atom(Topology(n_atoms=2), indices=[1])
    0

    .. versionadded:: 1.0.0
    """
    return _count_typed_hierarchy_from_atom(item, "molecule", "polysaccharide", indices)


@arg_digest(form=form)
def get_total_n_polysaccharides_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting total n polysaccharides from atom in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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


# From group


@arg_digest(form=form)
def get_atom_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting atom index from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()

    if is_all(indices):
        indices = range(item.n_groups)
    aux_dict = {ii: [] for ii in indices}
    for atom_index, parent_index in enumerate(group_index_from_atom):
        if pd.notna(parent_index) and parent_index in aux_dict:
            aux_dict[parent_index].append(atom_index)
    output = [aux_dict[ii] for ii in indices]

    del group_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_group(item, indices="all", skip_digestion=False):
    """
    Getting atom id from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    atom_id_from_atom = item.atoms["atom_id"].to_numpy()

    if indices == "all":
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
def get_atom_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting atom name from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    atom_name_from_atom = item.atoms["atom_name"].to_numpy()

    if indices == "all":
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
def get_atom_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting atom type from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    atom_type_from_atom = item.atoms["atom_type"].to_numpy()

    if indices == "all":
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
def get_group_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group index from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "group_index", indices)

    if indices == "all":
        output = list(range(item.groups.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_group_id_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group id from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "group_id", indices)

    group_id_from_group = item.groups["group_id"].to_numpy()

    if indices == "all":
        output = group_id_from_group.tolist()
    else:
        output = group_id_from_group[indices].tolist()

    del group_id_from_group

    return output


@arg_digest(form=form)
def get_group_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group name from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "group_name", indices)

    group_name_from_group = item.groups["group_name"].to_numpy()

    if indices == "all":
        output = group_name_from_group.tolist()
    else:
        output = group_name_from_group[indices].tolist()

    del group_name_from_group

    return output


@arg_digest(form=form)
def get_group_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group type from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "group_type", indices)

    group_type_from_group = item.groups["group_type"].to_numpy()

    if indices == "all":
        output = group_type_from_group.tolist()
    else:
        output = group_type_from_group[indices].tolist()

    del group_type_from_group

    return output


@arg_digest(form=form)
def get_molecule_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "molecule_index", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group.tolist()
    else:
        output = molecule_index_from_group[indices].tolist()

    del molecule_index_from_group

    return output


@arg_digest(form=form)
def get_molecule_id_from_group(item, indices="all", skip_digestion=False):
    """
    Getting molecule id from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "molecule_id", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_id_from_molecule = item.molecules["molecule_id"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_id_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting molecule name from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "molecule_name", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_name_from_molecule = item.molecules["molecule_name"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_name_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting molecule type from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "molecule_type", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_type_from_molecule = item.molecules["molecule_type"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = molecule_type_from_molecule[output].tolist()

    del molecule_index_from_group, molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting entity index from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "entity_index", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_group(item, indices="all", skip_digestion=False):
    """
    Getting entity id from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "entity_id", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_id_from_entity = item.entities["entity_id"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_id_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting entity name from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "entity_name", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_name_from_entity = item.entities["entity_name"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_name_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting entity type from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "entity_type", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_type_from_entity = item.entities["entity_type"].to_numpy()

    if indices == "all":
        output = molecule_index_from_group
    else:
        output = molecule_index_from_group[indices]

    output = entity_index_from_molecule[output]
    output = entity_type_from_entity[output].tolist()

    del molecule_index_from_group, entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_chain_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting chain index from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list
        Per-group chain positions as integers or ``None`` when unknown. A group
        spanning several chains returns its list of memberships, preserving ambiguity.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "chain_index", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    chain_index_from_atom = item.atoms["chain_index"].to_numpy(
        dtype=object, na_value=None
    )

    if indices == "all":
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

    output = [next(iter(ii)) if len(ii) == 1 else list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_chain_id_from_group(item, indices="all", skip_digestion=False):
    """
    Getting chain id from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "chain_id", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_id_from_chain = item.chains["chain_id"].to_numpy()

    if indices == "all":
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

    output = [
        chain_id_from_chain[next(iter(ii))]
        if len(ii) == 1
        else chain_id_from_chain[list(ii)].tolist()
        for ii in output
    ]

    del group_index_from_atom, chain_index_from_atom, chain_id_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting chain name from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "chain_name", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_name_from_chain = item.chains["chain_name"].to_numpy()

    if indices == "all":
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

    output = [
        chain_name_from_chain[next(iter(ii))]
        if len(ii) == 1
        else chain_name_from_chain[list(ii)].tolist()
        for ii in output
    ]

    del group_index_from_atom, chain_index_from_atom, chain_name_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_chain_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting chain type from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "chain_type", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_type_from_chain = item.chains["chain_type"].to_numpy()

    if indices == "all":
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

    output = [
        chain_type_from_chain[next(iter(ii))]
        if len(ii) == 1
        else chain_type_from_chain[list(ii)].tolist()
        for ii in output
    ]

    del group_index_from_atom, chain_index_from_atom, chain_type_from_chain, aux_dict

    return output


@arg_digest(form=form)
def get_n_atoms_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_atoms", indices)

    output = get_atom_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n atoms from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_atoms_from_group(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n groups from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_groups", indices)

    if indices == "all":
        output = item.groups.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_groups_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n groups from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_molecules_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n molecules from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_molecules", indices)

    if indices == "all":
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = get_molecule_index_from_group(
            item, indices=indices, skip_digestion=True
        )
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n molecules from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_entities_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n entities from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_entities", indices)

    if indices == "all":
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_group(item, indices=indices, skip_digestion=True)
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n entities from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_chains_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n chains from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_chains", indices)

    output = get_chain_index_from_group(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n chains from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_amino_acids_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n amino acids from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_amino_acids", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("amino acid")

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n amino acids from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_nucleotides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n nucleotides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_nucleotides", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("nucleotide")

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n nucleotides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_ions_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n ions from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_ions", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("ion")

    return output


@arg_digest(form=form)
def get_total_n_ions_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n ions from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_waters_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n waters from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_waters", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("water")

    return output


@arg_digest(form=form)
def get_total_n_waters_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n waters from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_small_molecules_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n small molecules from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_small_molecules", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("small molecule")

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n small molecules from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_lipids_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n lipids from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_lipids", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("lipid")

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n lipids from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_saccharides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n saccharides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_saccharides", indices)

    group_types = get_group_type_from_group(item, indices=indices, skip_digestion=True)

    output = group_types.count("saccharide")

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n saccharides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_peptides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n peptides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_peptides", indices)

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
def get_total_n_peptides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n peptides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_proteins_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n proteins from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_proteins", indices)

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
def get_total_n_proteins_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n proteins from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_dnas_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n dnas from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_dnas", indices)

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
def get_total_n_dnas_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n dnas from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_rnas_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n rnas from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_rnas", indices)

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
def get_total_n_rnas_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n rnas from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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


@arg_digest(form=form)
def get_n_polysaccharides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting n polysaccharides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "group", "n_polysaccharides", indices)

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
def get_total_n_polysaccharides_from_group(item, indices="all", skip_digestion=False):
    """
    Getting total n polysaccharides from group in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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


# From molecule


@arg_digest(form=form)
def get_atom_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting atom index from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)

    if is_all(indices):
        indices = range(item.n_molecules)
    aux_dict = {ii: [] for ii in indices}
    for atom_index, parent_index in enumerate(molecule_index_from_atom):
        if pd.notna(parent_index) and parent_index in aux_dict:
            aux_dict[parent_index].append(atom_index)
    output = [aux_dict[ii] for ii in indices]

    del (
        group_index_from_atom,
        molecule_index_from_group,
        molecule_index_from_atom,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_atom_id_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting atom id from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    atom_id_from_atom = item.atoms["atom_id"].to_numpy()

    if indices == "all":
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
def get_atom_name_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting atom name from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    atom_name_from_atom = item.atoms["atom_name"].to_numpy()

    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_name_from_atom[atom_index])

        output = list(aux_dict.values())

    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_name_from_atom[atom_index])

        output = [aux_dict.get(m, []) for m in indices]

    del (
        group_index_from_atom,
        molecule_index_from_atom,
        molecule_index_from_group,
        atom_name_from_atom,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_atom_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting atom type from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    atom_type_from_atom = item.atoms["atom_type"].to_numpy()

    if indices == "all":
        aux_dict = defaultdict(list)
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            aux_dict[molecule_index].append(atom_type_from_atom[atom_index])

        output = list(aux_dict.values())

    else:
        aux_dict = {ii: [] for ii in indices}
        for atom_index, molecule_index in enumerate(molecule_index_from_atom):
            if molecule_index in aux_dict:
                aux_dict[molecule_index].append(atom_type_from_atom[atom_index])

        output = [aux_dict.get(m, []) for m in indices]

    del (
        group_index_from_atom,
        molecule_index_from_atom,
        molecule_index_from_group,
        atom_type_from_atom,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_group_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting group index from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "group_index", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()

    if indices == "all":
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
def get_group_id_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting group id from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "group_id", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    group_id_from_group = item.groups["group_id"].to_numpy()

    if indices == "all":
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
def get_group_name_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting group name from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "group_name", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    group_name_from_group = item.groups["group_name"].to_numpy()

    if indices == "all":
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
def get_group_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting group type from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "group_type", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    group_type_from_group = item.groups["group_type"].to_numpy()

    if indices == "all":
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
def get_molecule_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "molecule_index", indices)

    if indices == "all":
        output = list(range(item.molecules.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_molecule_id_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule id from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "molecule_id", indices)

    molecule_id_from_molecule = item.molecules["molecule_id"].to_numpy()

    if indices == "all":
        output = molecule_id_from_molecule.tolist()
    else:
        output = molecule_id_from_molecule[indices].tolist()

    del molecule_id_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_name_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule name from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "molecule_name", indices)

    molecule_name_from_molecule = item.molecules["molecule_name"].to_numpy()

    if indices == "all":
        output = molecule_name_from_molecule.tolist()
    else:
        output = molecule_name_from_molecule[indices].tolist()

    del molecule_name_from_molecule

    return output


@arg_digest(form=form)
def get_molecule_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting molecule type from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "molecule_type", indices)

    molecule_type_from_molecule = item.molecules["molecule_type"].to_numpy()

    if indices == "all":
        output = molecule_type_from_molecule.tolist()
    else:
        output = molecule_type_from_molecule[indices].tolist()

    del molecule_type_from_molecule

    return output


@arg_digest(form=form)
def get_entity_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting entity index from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "entity_index", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()

    if indices == "all":
        output = entity_index_from_molecule.tolist()
    else:
        output = entity_index_from_molecule[indices].tolist()

    del entity_index_from_molecule

    return output


@arg_digest(form=form)
def get_entity_id_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting entity id from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "entity_id", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_id_from_entity = item.entities["entity_id"].to_numpy()

    if indices == "all":
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_id_from_entity[output].tolist()

    del entity_index_from_molecule, entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting entity name from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "entity_name", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_name_from_entity = item.entities["entity_name"].to_numpy()

    if indices == "all":
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_name_from_entity[output].tolist()

    del entity_index_from_molecule, entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting entity type from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "entity_type", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_type_from_entity = item.entities["entity_type"].to_numpy()

    if indices == "all":
        output = entity_index_from_molecule
    else:
        output = entity_index_from_molecule[indices]

    output = entity_type_from_entity[output].tolist()

    del entity_index_from_molecule, entity_type_from_entity

    return output


@arg_digest(form=form)
def get_chain_index_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting chain index from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "chain_index", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()

    if indices == "all":
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

    del group_index_from_atom, molecule_index_from_atom, chain_index_from_atom, aux_dict

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii)) for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_id_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting chain id from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "chain_id", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_id_from_chain = item.chains["chain_id"].to_numpy()

    if indices == "all":
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

    del (
        group_index_from_atom,
        molecule_index_from_atom,
        chain_index_from_atom,
        chain_id_from_chain,
        aux_dict,
    )

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii)) for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_name_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting chain name from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "chain_name", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_name_from_chain = item.chains["chain_name"].to_numpy()

    if indices == "all":
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

    del (
        group_index_from_atom,
        molecule_index_from_atom,
        chain_index_from_atom,
        chain_name_from_chain,
        aux_dict,
    )

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii)) for ii in output
    ]

    return output


@arg_digest(form=form)
def get_chain_type_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting chain type from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "chain_type", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_type_from_chain = item.chains["chain_type"].to_numpy()

    if indices == "all":
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

    del (
        group_index_from_atom,
        molecule_index_from_atom,
        chain_index_from_atom,
        chain_type_from_chain,
        aux_dict,
    )

    output = [
        (lambda u: u[0] if u.size == 1 else u.tolist())(np.unique(ii)) for ii in output
    ]

    return output


@arg_digest(form=form)
def get_n_atoms_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_atoms", indices)

    output = get_atom_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n atoms from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n groups from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_groups", indices)

    output = get_group_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n groups from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_groups_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_molecules_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n molecules from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_molecules", indices)

    if indices == "all":
        output = get_n_molecules_from_system(item, skip_digestion=True)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n molecules from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_entities_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n entities from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_entities", indices)

    if indices == "all":
        output = get_n_entities_from_system(item, skip_digestion=True)
    else:
        output = get_entity_index_from_molecule(
            item, indices=indices, skip_digestion=True
        )
        output = np.unique(output).size

    return output


@arg_digest(form=form)
def get_total_n_entities_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n entities from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_chains_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n chains from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_chains", indices)

    output = get_chain_index_from_molecule(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n chains from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_amino_acids_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n amino acids from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_amino_acids", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("amino acid") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n amino acids from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_amino_acids_from_molecule(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n nucleotides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_nucleotides", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("nucleotide") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n nucleotides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_nucleotides_from_molecule(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n ions from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_ions", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("ion") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n ions from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_ions_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n waters from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_waters", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("water") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n waters from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_waters_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n small molecules from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_small_molecules", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("small molecule") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_molecule(
    item, indices="all", skip_digestion=False
):
    """
    Getting total n small molecules from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_small_molecules_from_molecule(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n lipids from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_lipids", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("lipid") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n lipids from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_lipids_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n saccharides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_saccharides", indices)

    group_types = get_group_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("saccharide") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n saccharides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_saccharides_from_molecule(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n peptides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_peptides", indices)

    molecule_types = get_molecule_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = molecule_types.count("peptide")

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n peptides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_proteins_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n proteins from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_proteins", indices)

    molecule_types = get_molecule_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = molecule_types.count("protein")

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n proteins from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_polysaccharides_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n polysaccharides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_polysaccharides", indices)

    molecule_types = get_molecule_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = molecule_types.count("polysaccharide")

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_molecule(
    item, indices="all", skip_digestion=False
):
    """
    Getting total n polysaccharides from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    output = get_n_polysaccharides_from_molecule(
        item, indices=indices, skip_digestion=True
    )

    return output


@arg_digest(form=form)
def get_n_dnas_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n dnas from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_dnas", indices)

    molecule_types = get_molecule_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = molecule_types.count("dna")

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n dnas from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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
def get_n_rnas_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting n rnas from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "molecule", "n_rnas", indices)

    molecule_types = get_molecule_type_from_molecule(
        item, indices=indices, skip_digestion=True
    )
    output = molecule_types.count("rna")

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_molecule(item, indices="all", skip_digestion=False):
    """
    Getting total n rnas from molecule in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
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


# From entity


@arg_digest(form=form)
def get_atom_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting atom index from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    entity_index_from_atom = _get_hierarchy_from_atom(item, "entity", "index", "all")

    if is_all(indices):
        indices = range(item.n_entities)
    aux_dict = {ii: [] for ii in indices}
    for atom_index, parent_index in enumerate(entity_index_from_atom):
        if pd.notna(parent_index) and parent_index in aux_dict:
            aux_dict[parent_index].append(atom_index)
    output = [aux_dict[ii] for ii in indices]

    del entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting atom id from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_id_from_atom = item.atoms["atom_id"].to_numpy()

    if indices == "all":
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
def get_atom_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting atom name from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_name_from_atom = item.atoms["atom_name"].to_numpy()

    if indices == "all":
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
def get_atom_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting atom type from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    atom_type_from_atom = item.atoms["atom_type"].to_numpy()

    if indices == "all":
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
def get_group_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting group index from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "group_index", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_index_from_group = entity_index_from_molecule[molecule_index_from_group]

    if indices == "all":
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

    del (
        molecule_index_from_group,
        entity_index_from_molecule,
        entity_index_from_group,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_group_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting group id from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "group_id", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_index_from_group = entity_index_from_molecule[molecule_index_from_group]
    group_id_from_group = item.groups["group_id"].to_numpy()

    if indices == "all":
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

    del (
        molecule_index_from_group,
        entity_index_from_molecule,
        entity_index_from_group,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_group_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting group name from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "group_name", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_index_from_group = entity_index_from_molecule[molecule_index_from_group]
    group_name_from_group = item.groups["group_name"].to_numpy()

    if indices == "all":
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

    del (
        molecule_index_from_group,
        entity_index_from_molecule,
        entity_index_from_group,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_group_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting group type from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "group_type", indices)

    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    entity_index_from_group = entity_index_from_molecule[molecule_index_from_group]
    group_type_from_group = item.groups["group_type"].to_numpy()

    if indices == "all":
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

    del (
        molecule_index_from_group,
        entity_index_from_molecule,
        entity_index_from_group,
        aux_dict,
    )

    return output


@arg_digest(form=form)
def get_molecule_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "molecule_index", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()

    if indices == "all":
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
def get_molecule_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting molecule id from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "molecule_id", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_id_from_molecule = item.molecules["molecule_id"].to_numpy()

    if indices == "all":
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
def get_molecule_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting molecule name from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "molecule_name", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_name_from_molecule = item.molecules["molecule_name"].to_numpy()

    if indices == "all":
        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_name_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:
        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(
                    molecule_name_from_molecule[molecule_index]
                )

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting molecule type from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "molecule_type", indices)

    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_type_from_molecule = item.molecules["molecule_type"].to_numpy()

    if indices == "all":
        aux_dict = defaultdict(list)
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            aux_dict[entity_index].append(molecule_type_from_molecule[molecule_index])

        output = list(aux_dict.values())

    else:
        aux_dict = {ii: [] for ii in indices}
        for molecule_index, entity_index in enumerate(entity_index_from_molecule):
            if entity_index in aux_dict:
                aux_dict[entity_index].append(
                    molecule_type_from_molecule[molecule_index]
                )

        output = [aux_dict[m] for m in indices]

    del entity_index_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity index from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "entity_index", indices)

    if indices == "all":
        output = list(range(item.entities.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_entity_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity id from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "entity_id", indices)

    entity_id_from_entity = item.entities["entity_id"].to_numpy()

    if indices == "all":
        output = entity_id_from_entity.tolist()
    else:
        output = entity_id_from_entity[indices].tolist()

    del entity_id_from_entity

    return output


@arg_digest(form=form)
def get_entity_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity name from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "entity_name", indices)

    entity_name_from_entity = item.entities["entity_name"].to_numpy()

    if indices == "all":
        output = entity_name_from_entity.tolist()
    else:
        output = entity_name_from_entity[indices].tolist()

    del entity_name_from_entity

    return output


@arg_digest(form=form)
def get_entity_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity type from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "entity_type", indices)

    entity_type_from_entity = item.entities["entity_type"].to_numpy()

    if indices == "all":
        output = entity_type_from_entity.tolist()
    else:
        output = entity_type_from_entity[indices].tolist()

    del entity_type_from_entity

    return output


@arg_digest(form=form)
def get_chain_index_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting chain index from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "chain_index", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()

    if indices == "all":
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
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        chain_index_from_atom,
        aux_dict,
    )

    output = [list(np.unique(ii)) for ii in output]

    return output


@arg_digest(form=form)
def get_chain_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting chain id from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "chain_id", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_id_from_chain = item.chains["chain_id"].to_numpy()

    if indices == "all":
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
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        chain_index_from_atom,
        aux_dict,
    )
    del chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting chain name from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "chain_name", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_name_from_chain = item.chains["chain_name"].to_numpy()

    if indices == "all":
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
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        chain_index_from_atom,
        aux_dict,
    )
    del chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting chain type from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "chain_type", indices)

    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    chain_type_from_chain = item.chains["chain_type"].to_numpy()

    if indices == "all":
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
    del (
        molecule_index_from_atom,
        entity_index_from_atom,
        chain_index_from_atom,
        aux_dict,
    )
    del chain_type_from_chain

    return output


@arg_digest(form=form)
def get_n_atoms_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_atoms", indices)

    output = get_atom_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n atoms from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_atoms_from_molecule(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n groups from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_groups", indices)

    output = get_group_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n groups from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_groups_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_molecules_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n molecules from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_molecules", indices)

    output = get_molecule_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n molecules from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_molecules_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_entities_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n entities from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_entities", indices)

    if indices == "all":
        output = get_n_entities_from_system(item)
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_entities_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n entities from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_chains_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n chains from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_chains", indices)

    output = get_chain_index_from_entity(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_chains_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n chains from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_amino_acids_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n amino acids from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_amino_acids", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("amino acid") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n amino acids from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_amino_acids_from_entity(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n nucleotides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_nucleotides", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("nucleotide") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n nucleotides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_nucleotides_from_entity(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n ions from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_ions", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("ion") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n ions from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_ions_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n waters from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_waters", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("water") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n waters from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_waters_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n small molecules from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_small_molecules", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("small molecule") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n small molecules from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_small_molecules_from_entity(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n lipids from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_lipids", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("lipid") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n lipids from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_lipids_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n saccharides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_saccharides", indices)

    group_types = get_group_type_from_entity(item, indices=indices, skip_digestion=True)
    output = [ii.count("saccharide") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n saccharides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_saccharides_from_entity(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n peptides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_peptides", indices)

    molecule_types = get_molecule_type_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("peptide") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n peptides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_peptides_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_proteins_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n proteins from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_proteins", indices)

    molecule_types = get_molecule_type_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("protein") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n proteins from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_proteins_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n polysaccharides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_polysaccharides", indices)

    molecule_types = get_molecule_type_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("polysaccharide") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n polysaccharides from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_polysaccharides_from_entity(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_dnas_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n dnas from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_dnas", indices)

    molecule_types = get_molecule_type_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("dna") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n dnas from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_dnas_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_rnas_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n rnas from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "entity", "n_rnas", indices)

    molecule_types = get_molecule_type_from_entity(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("rna") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting total n rnas from entity in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_rnas_from_entity(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


# From component


# From chain


@arg_digest(form=form)
def get_atom_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting atom index from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()

    if is_all(indices):
        indices = range(item.n_chains)
    aux_dict = {ii: [] for ii in indices}
    for atom_index, parent_index in enumerate(chain_index_from_atom):
        if pd.notna(parent_index) and parent_index in aux_dict:
            aux_dict[parent_index].append(atom_index)
    output = [aux_dict[ii] for ii in indices]

    del chain_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_atom_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting atom id from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    atom_id_from_atom = item.atoms["atom_id"].to_numpy()

    if indices == "all":
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
def get_atom_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting atom name from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    atom_name_from_atom = item.atoms["atom_name"].to_numpy()

    if indices == "all":
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
def get_atom_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting atom type from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    atom_type_from_atom = item.atoms["atom_type"].to_numpy()

    if indices == "all":
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
def get_group_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting group index from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "group_index", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()

    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(group_index_from_atom[atom_index].tolist())

        output = list(aux_dict.values())

    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(group_index_from_atom[atom_index].tolist())

        output = [aux_dict[m] for m in indices]

    del group_index_from_atom, chain_index_from_atom, aux_dict

    output = [list(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_group_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting group id from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "group_id", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    group_id_from_group = item.groups["group_id"].to_numpy()

    if indices == "all":
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
def get_group_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting group name from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "group_name", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    group_name_from_group = item.groups["group_name"].to_numpy()

    if indices == "all":
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
def get_group_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting group type from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "group_type", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    group_type_from_group = item.groups["group_type"].to_numpy()

    if indices == "all":
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
def get_molecule_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting molecule index from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "molecule_index", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)

    if indices == "all":
        from molsysmt.form.molsysmt_Topology.get_topological_attributes import (
            get_n_chains_from_system,
        )

        n_chains = get_n_chains_from_system(item)
        indices = range(n_chains)

    aux_dict = {ii: set() for ii in indices}
    for atom_index, chain_index in enumerate(chain_index_from_atom):
        if chain_index in aux_dict:
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

    output = [aux_dict[m] for m in indices]

    aux_list = output
    output = []
    for ii in aux_list:
        clean_ii = [int(jj) for jj in ii if jj is not None and not pd.isna(jj)]
        output.append(sorted(clean_ii))

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting molecule id from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "molecule_id", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    molecule_id_from_molecule = item.molecules["molecule_id"].to_numpy()

    if indices == "all":
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

    output = [molecule_id_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_id_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting molecule name from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "molecule_name", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    molecule_name_from_molecule = item.molecules["molecule_name"].to_numpy()

    if indices == "all":
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

    output = [molecule_name_from_molecule[sorted(ii)].tolist() for ii in output]

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_name_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_molecule_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting molecule type from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "molecule_type", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    molecule_index_from_atom = molecule_index_from_group[
        group_index_from_atom.astype(int)
    ]
    molecule_type_from_molecule = item.molecules["molecule_type"].to_numpy()

    if indices == "all":
        from molsysmt.form.molsysmt_Topology.get_topological_attributes import (
            get_n_chains_from_system,
        )

        n_chains = get_n_chains_from_system(item)
        indices = range(n_chains)

    aux_dict = {ii: set() for ii in indices}
    for atom_index, chain_index in enumerate(chain_index_from_atom):
        if chain_index in aux_dict:
            aux_dict[chain_index].add(molecule_index_from_atom[atom_index])

    output = [aux_dict[m] for m in indices]

    aux_list = output
    output = []
    for ii in aux_list:
        clean_ii = [int(jj) for jj in ii if jj is not None and not pd.isna(jj)]
        if clean_ii:
            output.append(molecule_type_from_molecule[sorted(clean_ii)].tolist())
        else:
            output.append([])

    del chain_index_from_atom, group_index_from_atom, molecule_index_from_group
    del molecule_index_from_atom, molecule_type_from_molecule, aux_dict

    return output


@arg_digest(form=form)
def get_entity_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting entity index from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "entity_index", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices == "all":
        aux_dict = defaultdict(set)
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            aux_dict[chain_index].add(entity_index_from_atom[atom_index].tolist())

        output = list(aux_dict.values())

    else:
        aux_dict = {ii: set() for ii in indices}
        for atom_index, chain_index in enumerate(chain_index_from_atom):
            if chain_index in aux_dict:
                aux_dict[chain_index].add(entity_index_from_atom[atom_index].tolist())

        output = [aux_dict[m] for m in indices]

    output = [sorted(ii) for ii in output]

    del chain_index_from_atom, entity_index_from_atom, aux_dict

    return output


@arg_digest(form=form)
def get_entity_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting entity id from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "entity_id", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_id_from_entity = item.entities["entity_id"].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices == "all":
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
def get_entity_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting entity name from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "entity_name", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_name_from_entity = item.entities["entity_name"].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices == "all":
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
def get_entity_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting entity type from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "entity_type", indices)

    chain_index_from_atom = item.atoms["chain_index"].to_numpy()
    group_index_from_atom = item.atoms["group_index"].to_numpy()
    molecule_index_from_group = item.groups["molecule_index"].to_numpy()
    entity_index_from_molecule = item.molecules["entity_index"].to_numpy()
    molecule_index_from_atom = _molecule_indices_from_atoms(item)
    entity_index_from_atom = entity_index_from_molecule[molecule_index_from_atom]
    entity_type_from_entity = item.entities["entity_type"].to_numpy()

    del group_index_from_atom, molecule_index_from_group, entity_index_from_molecule

    if indices == "all":
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
def get_chain_index_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain index from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "chain_index", indices)

    if indices == "all":
        output = list(range(item.chains.shape[0]))
    else:
        output = indices

    return output


@arg_digest(form=form)
def get_chain_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain id from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "chain_id", indices)

    chain_id_from_chain = item.chains["chain_id"].to_numpy()

    if indices == "all":
        output = chain_id_from_chain.tolist()
    else:
        output = chain_id_from_chain[indices].tolist()

    del chain_id_from_chain

    return output


@arg_digest(form=form)
def get_chain_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain name from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "chain_name", indices)

    chain_name_from_chain = item.chains["chain_name"].to_numpy()

    if indices == "all":
        output = chain_name_from_chain.tolist()
    else:
        output = chain_name_from_chain[indices].tolist()

    del chain_name_from_chain

    return output


@arg_digest(form=form)
def get_chain_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain type from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "chain_type", indices)

    chain_type_from_chain = item.chains["chain_type"].to_numpy()

    if indices == "all":
        output = chain_type_from_chain.tolist()
    else:
        output = chain_type_from_chain[indices].tolist()

    del chain_type_from_chain

    return output


@arg_digest(form=form)
def get_n_atoms_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n atoms from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_atoms", indices)

    output = get_atom_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_atoms_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n atoms from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        aux = get_n_atoms_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(aux)
        del aux

    return output


@arg_digest(form=form)
def get_n_groups_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n groups from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_groups", indices)

    output = get_group_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_groups_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n groups from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_molecules_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n molecules from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_molecules", indices)

    output = get_molecule_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_molecules_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n molecules from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_entities_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n entities from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_entities", indices)

    output = get_entity_index_from_chain(item, indices, skip_digestion=True)
    output = [len(ii) if isinstance(ii, list) else 1 for ii in output]

    return output


@arg_digest(form=form)
def get_total_n_entities_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n entities from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_chains_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n chains from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_chains", indices)

    if indices == "all":
        output = item.chains.shape[0]
    else:
        output = len(indices)

    return output


@arg_digest(form=form)
def get_total_n_chains_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n chains from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
def get_n_amino_acids_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n amino acids from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_amino_acids", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("amino acid") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_amino_acids_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n amino acids from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_amino_acids_from_chain(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n nucleotides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_nucleotides", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("nucleotide") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_nucleotides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n nucleotides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_nucleotides_from_chain(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_ions_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n ions from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_ions", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("ion") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_ions_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n ions from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_ions_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_waters_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n waters from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_waters", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("water") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_waters_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n waters from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_waters_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n small molecules from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_small_molecules", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("small molecule") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_small_molecules_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n small molecules from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_small_molecules_from_chain(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_lipids_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n lipids from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_lipids", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("lipid") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_lipids_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n lipids from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_lipids_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_saccharides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n saccharides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_saccharides", indices)

    group_types = get_group_type_from_chain(item, indices=indices, skip_digestion=True)
    output = [ii.count("saccharide") for ii in group_types]

    return output


@arg_digest(form=form)
def get_total_n_saccharides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n saccharides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_saccharides_from_chain(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n polysaccharides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_polysaccharides", indices)

    molecule_types = get_molecule_type_from_chain(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("polysaccharide") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_polysaccharides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n polysaccharides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_polysaccharides_from_chain(
            item, indices=indices, skip_digestion=True
        )
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_peptides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n peptides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_peptides", indices)

    molecule_types = get_molecule_type_from_chain(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("peptide") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_peptides_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n peptides from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_peptides_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_proteins_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n proteins from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_proteins", indices)

    molecule_types = get_molecule_type_from_chain(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("protein") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_proteins_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n proteins from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_proteins_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_dnas_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n dnas from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_dnas", indices)

    molecule_types = get_molecule_type_from_chain(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("dna") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_dnas_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n dnas from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_dnas_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


@arg_digest(form=form)
def get_n_rnas_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n rnas from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "chain", "n_rnas", indices)

    molecule_types = get_molecule_type_from_chain(
        item, indices=indices, skip_digestion=True
    )
    output = [ii.count("rna") for ii in molecule_types]

    return output


@arg_digest(form=form)
def get_total_n_rnas_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting total n rnas from chain in form molsysmt.Topology.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
        output = get_n_rnas_from_chain(item, indices=indices, skip_digestion=True)
        output = sum(output)

    return output


# From bond


# From system


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    """
    Getting n atoms from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_atoms")

    return item.atoms.shape[0]


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_groups")

    return item.groups.shape[0]


@arg_digest(form=form)
def get_n_molecules_from_system(item, skip_digestion=False):
    """
    Getting n molecules from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_molecules")

    if item._molecules_dirty or item.groups["molecule_index"].isnull().any():
        item.rebuild_molecules(force=True)

    return item.molecules.shape[0]


@arg_digest(form=form)
def get_n_entities_from_system(item, skip_digestion=False):
    """
    Getting n entities from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_entities")

    if item._entities_dirty or item.molecules["entity_index"].isnull().any():
        item.rebuild_entities(force=True)

    return item.entities.shape[0]


@arg_digest(form=form)
def get_n_chains_from_system(item, skip_digestion=False):
    """
    Getting n chains from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_chains")

    return item.chains.shape[0]


@arg_digest(form=form)
def get_n_amino_acids_from_system(item, skip_digestion=False):
    """
    Getting n amino acids from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_amino_acids")

    output = int(item.groups["group_type"].eq("amino acid").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_nucleotides_from_system(item, skip_digestion=False):
    """
    Getting n nucleotides from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_nucleotides")

    output = int(item.groups["group_type"].eq("nucleotide").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_ions_from_system(item, skip_digestion=False):
    """
    Getting n ions from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_ions")

    output = int(item.groups["group_type"].eq("ion").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_waters_from_system(item, skip_digestion=False):
    """
    Getting n waters from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_waters")

    output = int(item.groups["group_type"].eq("water").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_small_molecules_from_system(item, skip_digestion=False):
    """
    Getting n small molecules from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_small_molecules")

    output = int(item.groups["group_type"].eq("small molecule").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_lipids_from_system(item, skip_digestion=False):
    """
    Getting n lipids from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_lipids")

    output = int(item.groups["group_type"].eq("lipid").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_saccharides_from_system(item, skip_digestion=False):
    """
    Getting n saccharides from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_saccharides")

    output = int(item.groups["group_type"].eq("saccharide").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_peptides_from_system(item, skip_digestion=False):
    """
    Getting n peptides from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_peptides")

    output = int(item.molecules["molecule_type"].eq("peptide").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_proteins_from_system(item, skip_digestion=False):
    """
    Getting n proteins from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_proteins")

    output = int(item.molecules["molecule_type"].eq("protein").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_polysaccharides_from_system(item, skip_digestion=False):
    """
    Getting n polysaccharides from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_polysaccharides")

    output = int(
        item.molecules["molecule_type"].eq("polysaccharide").fillna(False).sum()
    )

    return output


@arg_digest(form=form)
def get_n_dnas_from_system(item, skip_digestion=False):
    """
    Getting n dnas from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_dnas")

    output = int(item.molecules["molecule_type"].eq("dna").fillna(False).sum())

    return output


@arg_digest(form=form)
def get_n_rnas_from_system(item, skip_digestion=False):
    """
    Getting n rnas from system in form molsysmt.Topology.


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
    if _uses_declared_hierarchy(item):
        return _project_hierarchy(item, "system", "n_rnas")

    output = int(item.molecules["molecule_type"].eq("rna").fillna(False).sum())

    return output


# List of functions to be imported

__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
