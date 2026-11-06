"""Shared lifetime binding for explicit element labels and data utilities."""

from ._basic import _native_documentation


def _call_explicit(owner, module, name, parameters):
    owner._view()
    import molsysmt

    namespace = molsysmt.element
    for part in module:
        namespace = getattr(namespace, part)
    return getattr(namespace, name)(**parameters)


def _utility_documentation(name, module="element", *, local_skip=False):
    def decorate(function):
        function = _native_documentation(name, module=module, bind_primary=False)(
            function
        )
        function.__doc__ += (
            "\n\nView integration\n----------------\n"
            "Works with an open empty view. Scientific inputs stay explicit; "
            "no primary molecular reader, synchronization, scene/history change "
            "or assignment is involved. Native validation, warnings, return "
            "types and result ownership are retained.\n"
        )
        if local_skip:
            function.__doc__ = function.__doc__.replace(
                "\nReturns\n-------",
                "\nskip_digestion : bool, default=False\n"
                "    Keyword-only addon validation control, not forwarded to "
                "the native utility.\n\nReturns\n-------",
                1,
            )
            function.__doc__ += (
                "skip_digestion is a keyword-only addon validation control. "
                "This native utility has no such parameter; it receives no "
                "skip flag and retains its own validation.\n"
            )
        if name == "is_composed_of":
            function.__doc__ += (
                "This is the native declared relation between two element-level "
                "names, not a query of the actual contents of view.molsys.\n"
            )
        return function

    return decorate


class _ElementUtilities:
    def __init__(self, owner):
        self._owner = owner

    def __dir__(self):
        return list(self._NAMES)

    def _call_explicit(self, module, name, parameters):
        return _call_explicit(self._owner, module, name, parameters)
