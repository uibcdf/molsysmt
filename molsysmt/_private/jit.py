from functools import lru_cache, wraps
import numba as nb

_COMPILED_FACTORIES = []
_NUMBA_WARNING_EMITTED = False
_WRAPPER_COMPILED = {}
_COMPILING = set()


def _emit_numba_jit_warning(kernel_name, module_name):
    global _NUMBA_WARNING_EMITTED
    if _NUMBA_WARNING_EMITTED:
        return
    _NUMBA_WARNING_EMITTED = True

    from smonitor.integrations import emit_from_catalog
    from molsysmt._private.smonitor import CATALOG, META, PACKAGE_ROOT

    emit_from_catalog(
        CATALOG["warnings"]["NumbaJitWarning"],
        package_root=PACKAGE_ROOT,
        meta=META,
        extra={"kernel": kernel_name, "module": module_name},
    )


def lazy_njit(signature, cache=True, **kwargs):
    """Returning a lazily-compiled Numba function with a fixed signature."""

    def decorator(func):
        @lru_cache(maxsize=1)
        def _compiled():
            if wrapper in _COMPILING:
                return nb.njit(signature, cache=cache, **kwargs)(func)

            _COMPILING.add(wrapper)
            try:
                # Ensure dependencies are compiled and bound to their dispatchers.
                for name in func.__code__.co_names:
                    if name not in func.__globals__:
                        continue
                    value = func.__globals__[name]
                    if callable(value) and value in _WRAPPER_COMPILED and value is not wrapper:
                        func.__globals__[name] = _WRAPPER_COMPILED[value]()

                _emit_numba_jit_warning(func.__name__, func.__module__)
                return nb.njit(signature, cache=cache, **kwargs)(func)
            finally:
                _COMPILING.discard(wrapper)

        @wraps(func)
        def wrapper(*args, **kwds):
            return _compiled()(*args, **kwds)

        _WRAPPER_COMPILED[wrapper] = _compiled
        _COMPILED_FACTORIES.append(_compiled)

        return wrapper

    return decorator


def compile_registered():
    """Compiling all registered Numba kernels once."""
    compiled = 0
    for factory in _COMPILED_FACTORIES:
        factory()
        compiled += 1
    return compiled
