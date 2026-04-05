from molsysmt._private.arg_digestion import arg_digest
import types

form = 'molsysmt.PDBFileHandler'


def _get_first_model_records(item):
    models = item.entry.coordinate.model
    if models is None or len(models) == 0:
        return []
    return [record for record in models[0].record if record.recordName in ['ATOM', 'HETATOM']]


def _get_group_rows(records):
    group_rows = []
    previous_key = None
    current_chain_segment = -1
    previous_chain_id = None

    for record in records:
        if record.chainId != previous_chain_id:
            current_chain_segment += 1
            previous_chain_id = record.chainId

        key = (current_chain_segment, record.chainId, str(record.resSeq), record.iCode, record.resName)
        if key != previous_key:
            group_rows.append((str(record.resSeq), record.resName, record.chainId))
            previous_key = key

    return group_rows


@arg_digest(form=form)
def get_n_atoms_from_system(item, skip_digestion=False):
    return len(_get_first_model_records(item))


@arg_digest(form=form)
def get_n_groups_from_system(item, skip_digestion=False):
    return len(_get_group_rows(_get_first_model_records(item)))


@arg_digest(form=form)
def get_atom_id_from_atom(item, indices='all', skip_digestion=False):
    atom_ids = [str(record.serial) for record in _get_first_model_records(item)]
    if indices == 'all':
        return atom_ids
    return [atom_ids[ii] for ii in indices]


@arg_digest(form=form)
def get_atom_name_from_atom(item, indices='all', skip_digestion=False):
    atom_names = [record.name for record in _get_first_model_records(item)]
    if indices == 'all':
        return atom_names
    return [atom_names[ii] for ii in indices]


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):
    group_names = [row[1] for row in _get_group_rows(_get_first_model_records(item))]
    if indices == 'all':
        return group_names
    return [group_names[ii] for ii in indices]


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
