from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from depdigest import dep_digest
import types

form = 'file:fasta'

# aa1 → aa3 mapping (canonical 20 + ambiguous codes)
_aa1_to_aa3 = {
    'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
    'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
    'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
    'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
    'O': 'PYL', 'U': 'SEC', 'B': 'ASX', 'Z': 'GLX', 'X': 'XAA', 'J': 'XLE',
}


def _parse_fasta(item):
    from Bio import SeqIO
    return list(SeqIO.parse(item, 'fasta'))


# --- System-level scalars ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_n_chains_from_system(item, skip_digestion=False):
    """
    Getting n chains from system in form file:fasta.


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
    records = _parse_fasta(item)
    return len(records)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_entities_from_system(item, skip_digestion=False):
    """
    Getting n entities from system in form file:fasta.


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
    records = _parse_fasta(item)
    return len(records)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form file:fasta.


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
    records = _parse_fasta(item)
    return sum(len(r.seq) for r in records)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_amino_acids_from_system(item, skip_digestion=False):
    """
    Getting n amino acids from system in form file:fasta.


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
    records = _parse_fasta(item)
    return sum(len(r.seq) for r in records)


# --- Chain-level ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting chain id from chain in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    ids = [r.id for r in records]
    if indices == 'all':
        return ids
    return [ids[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting chain name from chain in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    names = [r.name for r in records]
    if indices == 'all':
        return names
    return [names[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting chain type from chain in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    n = len(records)
    types_ = ['protein'] * n
    if indices == 'all':
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n groups from chain in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    lengths = [len(r.seq) for r in records]
    if indices == 'all':
        return lengths
    return [lengths[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):
    """
    Getting n amino acids from chain in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_groups_from_chain(item, indices=indices, skip_digestion=True)


# --- Entity-level (one entity per sequence in FASTA) ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting entity id from entity in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_chain_id_from_chain(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
@dep_digest('Bio')
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting entity name from entity in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    names = [r.description for r in records]
    if indices == 'all':
        return names
    return [names[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting entity type from entity in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    n = len(records)
    types_ = ['protein'] * n
    if indices == 'all':
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n groups from entity in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_groups_from_chain(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):
    """
    Getting n amino acids from entity in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return get_n_groups_from_chain(item, indices=indices, skip_digestion=True)


# --- Group-level ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_group_name_from_group(item, indices='all', skip_digestion=False):
    """
    Getting group name from group in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    all_names = []
    for r in records:
        for aa1 in str(r.seq):
            all_names.append(_aa1_to_aa3.get(aa1.upper(), 'XAA'))
    if indices == 'all':
        return all_names
    return [all_names[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_group_type_from_group(item, indices='all', skip_digestion=False):
    """
    Getting group type from group in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    total = sum(len(r.seq) for r in records)
    types_ = ['amino acid'] * total
    if indices == 'all':
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_group_index_from_group(item, indices='all', skip_digestion=False):
    """
    Getting group index from group in form file:fasta.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_fasta(item)
    total = sum(len(r.seq) for r in records)
    all_indices = list(range(total))
    if indices == 'all':
        return all_indices
    return [all_indices[i] for i in indices]


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
