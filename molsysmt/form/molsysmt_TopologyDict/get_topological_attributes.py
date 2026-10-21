import inspect
import types

from molsysmt._private.argdigest import arg_digest
from molsysmt.form._dict_atom_queries import (
    query_docstring as _query_docstring,
)
from molsysmt.form._dict_atom_queries import (
    read as _read_stored_atoms,
)
from molsysmt.form._dict_atom_queries import (
    supports as _supports_stored_atoms,
)

form = "molsysmt.TopologyDict"


def _make_wrapper(name, target):
    signature = inspect.signature(target)
    parameters = [str(parameter) for parameter in signature.parameters.values()]
    parameter_list = ", ".join(parameters)

    call_arguments = []
    for parameter in signature.parameters.values():
        if parameter.name == "item":
            call_arguments.append("tmp_item")
        elif parameter.name == "skip_digestion":
            call_arguments.append("skip_digestion=True")
        elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            call_arguments.append("*" + parameter.name)
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            call_arguments.append("**" + parameter.name)
        else:
            call_arguments.append(f"{parameter.name}={parameter.name}")
    call_arguments = ", ".join(call_arguments)

    attribute, element = name[4:].rsplit("_from_", 1)
    direct_arguments = "indices=indices, " if "indices" in signature.parameters else ""

    namespace = {
        "__name__": __name__,
        "arg_digest": arg_digest,
        "target": target,
        "form": form,
        "_read_stored_atoms": _read_stored_atoms,
    }
    # The generated wrapper receives this converter through locals().
    from .to_molsysmt_Topology import to_molsysmt_Topology  # noqa: F401

    namespace.update(locals())
    source = f"@arg_digest(form=form)\ndef {name}({parameter_list}):\n    stored = _read_stored_atoms(item, {attribute!r}, {element!r}, {direct_arguments}nested=False)\n    if stored is not NotImplemented:\n        return stored\n    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)\n    return target({call_arguments})\n"
    exec(source, namespace)
    wrapper = namespace[name]
    wrapper.__doc__ = (
        _query_docstring(attribute, element, form)
        if _supports_stored_atoms(attribute, element)
        else f"Delegating {name} through the native target form."
    )
    return wrapper


import molsysmt.form.molsysmt_Topology.get_topological_attributes as _target_module  # noqa: E402
from molsysmt.form.molsysmt_Topology.get_topological_attributes import *  # noqa: E402, F401, F403
from molsysmt.form.molsysmt_Topology.get_topological_attributes import (  # noqa: E402
    __all__ as _target_all,
)

for _name in _target_all:
    globals()[_name] = _make_wrapper(_name, getattr(_target_module, _name))

__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
