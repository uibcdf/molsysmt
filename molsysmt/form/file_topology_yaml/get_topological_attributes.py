from molsysmt._private.argdigest import arg_digest
import inspect
import types

form = 'file:topology_yaml'


def _make_wrapper(name, target):
    signature = inspect.signature(target)
    parameters = [str(parameter) for parameter in signature.parameters.values()]
    parameter_list = ', '.join(parameters)

    call_arguments = []
    for parameter in signature.parameters.values():
        if parameter.name == 'item':
            call_arguments.append('tmp_item')
        elif parameter.name == 'skip_digestion':
            call_arguments.append('skip_digestion=True')
        elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            call_arguments.append('*' + parameter.name)
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            call_arguments.append('**' + parameter.name)
        else:
            call_arguments.append(f"{parameter.name}={parameter.name}")
    call_arguments = ', '.join(call_arguments)

    namespace = {
        '__name__': __name__, 'arg_digest': arg_digest, 'target': target, 'form': form
    }
    from .to_molsysmt_Topology import to_molsysmt_Topology
    namespace.update(locals())
    source = f"@arg_digest(form=form)\ndef {name}({parameter_list}):\n    tmp_item = to_molsysmt_Topology(item, skip_digestion=True)\n    return target({call_arguments})\n"
    exec(source, namespace)
    wrapper = namespace[name]
    wrapper.__doc__ = f'Delegating {name} through the native target form.'
    return wrapper


from molsysmt.form.molsysmt_Topology.get_topological_attributes import *  # noqa: F401,F403
from molsysmt.form.molsysmt_Topology.get_topological_attributes import __all__ as _target_all
import molsysmt.form.molsysmt_Topology.get_topological_attributes as _target_module

for _name in _target_all:
    globals()[_name] = _make_wrapper(_name, getattr(_target_module, _name))

__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
