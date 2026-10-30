"""Delegate declared form queries through an explicit bounded native reader."""

import inspect

from molsysmt._private.argdigest import arg_digest


def make_native_getter(name, target, form, read_source):
    """Preserve a known getter signature and validate once at the source boundary."""
    parameters = inspect.signature(target).parameters
    declaration = ", ".join(str(value) for value in parameters.values())
    arguments = ", ".join(
        "read_source(item)"
        if key == "item"
        else "skip_digestion=True"
        if key == "skip_digestion"
        else f"{key}={key}"
        for key in parameters
    )
    namespace = {
        "__name__": "molsysmt.form."
        + form.replace(".", "_", 1).replace(":", "_")
        + ".get_topological_attributes",
        "arg_digest": arg_digest,
        "target": target,
        "form": form,
        "read_source": read_source,
    }
    exec(
        f"@arg_digest(form=form)\ndef {name}({declaration}):\n"
        f"    return target({arguments})\n",
        namespace,
    )
    result = namespace[name]
    result.__doc__ = target.__doc__.replace("molsysmt.MolSys", form)
    return result
