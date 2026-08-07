from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
import types

form = 'string:amino_acids_1'


def _group_names(item):
    sequence = item.removeprefix('amino_acids_1:')
    return list(sequence.upper())


@arg_digest(form=form)
def get_group_index_from_group(item, indices='all', skip_digestion=False):
    output = list(range(len(_group_names(item))))
    if not is_all(indices):
        output = [output[ii] for ii in indices]
    return output


@arg_digest(form=form)
def get_group_name_from_group(item, indices='all', skip_digestion=False):
    output = _group_names(item)
    if not is_all(indices):
        output = [output[ii] for ii in indices]
    return output


__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
