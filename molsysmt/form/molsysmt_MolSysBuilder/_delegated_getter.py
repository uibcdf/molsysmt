import inspect

from molsysmt._private.argdigest import arg_digest


def make_delegated_getter(name, target, component):
    """Creating a form getter that delegates to a stored native component."""

    signature = inspect.signature(target)
    parameters = ", ".join(
        str(parameter) for parameter in signature.parameters.values()
    )

    call_arguments = []
    for parameter in signature.parameters.values():
        if parameter.name == "item":
            call_arguments.append("component_item")
        elif parameter.name == "skip_digestion":
            call_arguments.append("skip_digestion=True")
        elif parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
            call_arguments.append(parameter.name)
        elif parameter.kind == inspect.Parameter.VAR_POSITIONAL:
            call_arguments.append(f"*{parameter.name}")
        elif parameter.kind == inspect.Parameter.VAR_KEYWORD:
            call_arguments.append(f"**{parameter.name}")
        else:
            call_arguments.append(f"{parameter.name}={parameter.name}")

    namespace = {
        "__name__": __name__,
        "arg_digest": arg_digest,
        "component": component,
        "form": "molsysmt.MolSysBuilder",
        "target": target,
    }
    source = (
        f"@arg_digest(form=form)\n"
        f"def {name}({parameters}):\n"
        f"    component_item = getattr(item, component)\n"
        f"    return target({', '.join(call_arguments)})\n"
    )
    exec(source, namespace)
    wrapper = namespace[name]
    wrapper.__doc__ = (
        f"Delegating ``{name}`` directly to the builder's native "
        f"``{component}`` component."
    )
    return wrapper
