import types

from depdigest import dep_digest

from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.element.group.amino_acid.codes import aa1_to_aa3 as _aa1_to_aa3

form = "file:pir"


def _parse_pir(item):
    from Bio import SeqIO

    return list(SeqIO.parse(item, "pir"))


# --- System-level scalars ---


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_chains_from_system(item, skip_digestion=False):
    """
    Getting n chains from system in form file:pir.


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
    records = _parse_pir(item)
    return len(records)


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_entities_from_system(item, skip_digestion=False):
    """
    Getting n entities from system in form file:pir.


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
    records = _parse_pir(item)
    return len(records)


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_groups_from_system(item, skip_digestion=False):
    """
    Getting n groups from system in form file:pir.


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
    records = _parse_pir(item)
    return sum(len(r.seq) for r in records)


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_amino_acids_from_system(item, skip_digestion=False):
    """
    Getting n amino acids from system in form file:pir.


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
    records = _parse_pir(item)
    return sum(len(r.seq) for r in records)


# --- Chain-level ---


@arg_digest(form=form)
@dep_digest("Bio")
def get_chain_index_from_chain(item, indices="all", skip_digestion=False):
    """Getting source chain-position indices from a PIR sequence file.

    Parameters
    ----------
    item : file:pir
        Input sequence file, with one chain per sequence record.
    indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Source positions to return, retaining their order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or none
        Zero-based source record positions. Empty files return an empty list;
        indices=None returns None. Record IDs are separate string labels.

    Notes
    -----
    The existing record-count getter supplies the unrestricted positional axis.
    No atom topology or coordinates are constructed.

    Examples
    --------
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     molsys = Path(directory) / 'chains.pir'
    ...     _ = molsys.write_text('>P1;alpha\\nfirst chain\\nACD*\\n>P1;beta\\nsecond chain\\nGK*\\n')
    ...     positions = get_chain_index_from_chain(str(molsys), indices=[1, 0, 1])
    >>> positions
    [1, 0, 1]

    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        count = get_n_chains_from_system(item, skip_digestion=True)
        return list(range(count))
    return list(indices)


@arg_digest(form=form)
@dep_digest("Bio")
def get_chain_id_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain id from chain in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    ids = [r.id for r in records]
    if indices == "all":
        return ids
    return [ids[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_chain_name_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain name from chain in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    names = [r.name for r in records]
    if indices == "all":
        return names
    return [names[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_chain_type_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting chain type from chain in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    n = len(records)
    types_ = ["protein"] * n
    if indices == "all":
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_groups_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n groups from chain in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    lengths = [len(r.seq) for r in records]
    if indices == "all":
        return lengths
    return [lengths[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_amino_acids_from_chain(item, indices="all", skip_digestion=False):
    """
    Getting n amino acids from chain in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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


# --- Entity-level (one entity per sequence in PIR) ---


@arg_digest(form=form)
@dep_digest("Bio")
def get_entity_index_from_entity(item, indices="all", skip_digestion=False):
    """Getting source entity-position indices from a PIR sequence file.

    Parameters
    ----------
    item : file:pir
        Input sequence file, with one entity per sequence record.
    indices : str, int, list, tuple, or numpy.ndarray, default='all'
        Source positions to return, retaining their order and repetitions.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    list of int or none
        Zero-based source record positions. Empty files return an empty list;
        indices=None returns None. Record IDs are separate string labels.

    Notes
    -----
    The existing record-count getter supplies the unrestricted positional axis.
    No atom topology or coordinates are constructed.

    Examples
    --------
    >>> from pathlib import Path
    >>> from tempfile import TemporaryDirectory
    >>> with TemporaryDirectory() as directory:
    ...     molsys = Path(directory) / 'chains.pir'
    ...     _ = molsys.write_text('>P1;alpha\\nfirst chain\\nACD*\\n>P1;beta\\nsecond chain\\nGK*\\n')
    ...     positions = get_entity_index_from_entity(str(molsys), indices=[1, 0, 1])
    >>> positions
    [1, 0, 1]

    .. versionadded:: 1.0.0
    """
    if indices is None:
        return None
    if is_all(indices):
        count = get_n_entities_from_system(item, skip_digestion=True)
        return list(range(count))
    return list(indices)


@arg_digest(form=form)
@dep_digest("Bio")
def get_entity_id_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity id from entity in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
@dep_digest("Bio")
def get_entity_name_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity name from entity in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    names = [r.description for r in records]
    if indices == "all":
        return names
    return [names[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_entity_type_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting entity type from entity in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    n = len(records)
    types_ = ["protein"] * n
    if indices == "all":
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_n_groups_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n groups from entity in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
@dep_digest("Bio")
def get_n_amino_acids_from_entity(item, indices="all", skip_digestion=False):
    """
    Getting n amino acids from entity in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
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
@dep_digest("Bio")
def get_group_name_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group name from group in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    all_names = []
    for r in records:
        for aa1 in str(r.seq):
            all_names.append(_aa1_to_aa3.get(aa1.upper(), "XAA"))
    if indices == "all":
        return all_names
    return [all_names[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_group_type_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group type from group in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    total = sum(len(r.seq) for r in records)
    types_ = ["amino acid"] * total
    if indices == "all":
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest("Bio")
def get_group_index_from_group(item, indices="all", skip_digestion=False):
    """
    Getting group index from group in form file:pir.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    records = _parse_pir(item)
    total = sum(len(r.seq) for r in records)
    all_indices = list(range(total))
    if indices == "all":
        return all_indices
    return [all_indices[i] for i in indices]


__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
