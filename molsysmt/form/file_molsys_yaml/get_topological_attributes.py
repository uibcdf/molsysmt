from functools import wraps

from molsysmt._private.arg_digestion import arg_digest

form = "file:molsys_yaml"


def _to_molsys(item):
    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    return to_molsysmt_MolSys(item, skip_digestion=True)


def _build_wrapper(name, target):
    @arg_digest(form=form)
    @wraps(target)
    def wrapper(item, *args, skip_digestion=False, **kwargs):
        molsys = _to_molsys(item)
        return target(molsys, *args, skip_digestion=True, **kwargs)

    wrapper.__name__ = name
    return wrapper


from molsysmt.form.molsysmt_MolSys import get_topological_attributes as _target_module

for _name, _target in vars(_target_module).items():
    if callable(_target) and _name.startswith("get_"):
        globals()[_name] = _build_wrapper(_name, _target)


__all__ = [name for name, obj in globals().items() if callable(obj) and name.startswith("get_")]
