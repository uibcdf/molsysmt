from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotWithThisFormError
from depdigest import dep_digest
import types

form = 'file:pir'

# aa1 → aa3 mapping (canonical 20 + ambiguous codes)
_aa1_to_aa3 = {
    'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
    'E': 'GLU', 'Q': 'GLN', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
    'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
    'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
    'O': 'PYL', 'U': 'SEC', 'B': 'ASX', 'Z': 'GLX', 'X': 'XAA', 'J': 'XLE',
}


def _parse_pir(item):
    from Bio import SeqIO
    return list(SeqIO.parse(item, 'pir'))


# --- System-level scalars ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_n_chains_from_system(item, skip_digestion=False):
    records = _parse_pir(item)
    return len(records)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_entities_from_system(item, skip_digestion=False):
    records = _parse_pir(item)
    return len(records)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_groups_from_system(item, skip_digestion=False):
    records = _parse_pir(item)
    return sum(len(r.seq) for r in records)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_amino_acids_from_system(item, skip_digestion=False):
    records = _parse_pir(item)
    return sum(len(r.seq) for r in records)


# --- Chain-level ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_chain_id_from_chain(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    ids = [r.id for r in records]
    if indices == 'all':
        return ids
    return [ids[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_chain_name_from_chain(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    names = [r.name for r in records]
    if indices == 'all':
        return names
    return [names[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_chain_type_from_chain(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    n = len(records)
    types_ = ['protein'] * n
    if indices == 'all':
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_groups_from_chain(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    lengths = [len(r.seq) for r in records]
    if indices == 'all':
        return lengths
    return [lengths[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_amino_acids_from_chain(item, indices='all', skip_digestion=False):
    return get_n_groups_from_chain(item, indices=indices, skip_digestion=True)


# --- Entity-level (one entity per sequence in PIR) ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_entity_id_from_entity(item, indices='all', skip_digestion=False):
    return get_chain_id_from_chain(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
@dep_digest('Bio')
def get_entity_name_from_entity(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    names = [r.description for r in records]
    if indices == 'all':
        return names
    return [names[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_entity_type_from_entity(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    n = len(records)
    types_ = ['protein'] * n
    if indices == 'all':
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_groups_from_entity(item, indices='all', skip_digestion=False):
    return get_n_groups_from_chain(item, indices=indices, skip_digestion=True)


@arg_digest(form=form)
@dep_digest('Bio')
def get_n_amino_acids_from_entity(item, indices='all', skip_digestion=False):
    return get_n_groups_from_chain(item, indices=indices, skip_digestion=True)


# --- Group-level ---

@arg_digest(form=form)
@dep_digest('Bio')
def get_group_name_from_group(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
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
    records = _parse_pir(item)
    total = sum(len(r.seq) for r in records)
    types_ = ['amino acid'] * total
    if indices == 'all':
        return types_
    return [types_[i] for i in indices]


@arg_digest(form=form)
@dep_digest('Bio')
def get_group_index_from_group(item, indices='all', skip_digestion=False):
    records = _parse_pir(item)
    total = sum(len(r.seq) for r in records)
    all_indices = list(range(total))
    if indices == 'all':
        return all_indices
    return [all_indices[i] for i in indices]


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
