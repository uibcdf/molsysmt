import functools
import inspect

from molsysmt._private.digestion import digest
from molsysmt.form.molsysmt_MolSys import get_topological_attributes as _molsys_get

form = 'molsysviewer.MolSysView'


def _wrap_getter(func):
    signature = inspect.signature(func)
    has_skip = 'skip_digestion' in signature.parameters

    @digest(form=form)
    @functools.wraps(func)
    def wrapper(item, *args, **kwargs):
        from .to_molsysmt_MolSys import to_molsysmt_MolSys

        tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
        if tmp_item is None:
            return None
        if has_skip:
            kwargs['skip_digestion'] = True
        return func(tmp_item, *args, **kwargs)

    wrapper.__signature__ = signature
    return wrapper


for _name, _func in _molsys_get.__dict__.items():
    if _name.startswith('get_') and '_from_' in _name and callable(_func):
        globals()[_name] = _wrap_getter(_func)

del(_name, _func)
