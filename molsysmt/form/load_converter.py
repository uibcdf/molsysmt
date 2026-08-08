# This method must not be digested
def load_converter(module, converter):
    """Resolve a converter that a form declares lazily, by submodule name.

    A form's `_convert_to` maps a target form to either the converter itself or, for the
    ones that would drag a third-party library in at import time, the *name* of the
    submodule holding it. This resolves the second case and leaves the first alone, so
    callers do not each need to know the difference.

    Parameters
    ----------
    module : module
        The form module declaring the conversion.
    converter : callable or str
        The value read from `_convert_to`.

    Returns
    -------
    callable
        The converter.

    Notes
    -----
    Importing `<form>.to_x` makes the *submodule* an attribute of the form package,
    shadowing the function of the same name. Around 1400 call sites do
    `from molsysmt.form.<form> import to_x` expecting the function, so this rebinds the
    attribute after loading. Without that, whether the name means the function or the
    module depends on whether some earlier conversion happened to import it -- which is
    the kind of bug that appears far from its cause.
    """

    if not isinstance(converter, str):
        return converter

    from importlib import import_module

    submodule = import_module(f'{module.__name__}.{converter}')
    function = getattr(submodule, converter)
    setattr(module, converter, function)

    return function
