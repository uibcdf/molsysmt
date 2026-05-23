import os
import inspect
from functools import lru_cache, wraps
import smonitor
from molsysmt._private.smonitor import PACKAGE_ROOT

# Configure repository-local JIT caching dynamically for development/QA environments
try:
    _profile = smonitor.get_manager().config.profile
except Exception:
    _profile = "user"

if _profile in ("dev", "qa", "debug", "agent"):
    if "NUMBA_CACHE_DIR" not in os.environ:
        # PACKAGE_ROOT is /path/to/repo/molsysmt
        # Repository root is PACKAGE_ROOT.parent
        repo_root = PACKAGE_ROOT.parent
        os.environ["NUMBA_CACHE_DIR"] = str(repo_root / ".numba_cache")

import numba as nb

_COMPILED_FACTORIES = []
_NUMBA_WARNING_EMITTED = False
_WRAPPER_COMPILED = {}
_COMPILING = set()


def _is_kernel_cached(func):
    """Detect if a function is likely cached in Numba's disk cache."""
    try:
        # Get the module file path
        source_file = inspect.getfile(func)
        module_dir = os.path.dirname(source_file)
        # Numba default cache is in __pycache__ next to the source
        cache_dir = os.path.join(module_dir, "__pycache__")
        if not os.path.exists(cache_dir):
            return False
        
        # Kernel cache files end with .nbc and .nbi
        # They usually contain the function name
        func_name = func.__name__
        for f in os.listdir(cache_dir):
            if func_name in f and (f.endswith(".nbc") or f.endswith(".nbi")):
                return True
    except Exception:
        pass
    return False


def _emit_numba_jit_warning(func):
    global _NUMBA_WARNING_EMITTED
    if _NUMBA_WARNING_EMITTED:
        return
    
    # Bypass smonitor warnings for pure mathematical core/lib kernels
    # to avoid loading telemetry/catalog infrastructure in high-performance mode.
    if func.__module__.startswith("molsysmt.lib") or func.__module__.startswith("molsysmt.core"):
        return

    # If the kernel is already cached on disk, don't annoy the user
    if _is_kernel_cached(func):
        return

    _NUMBA_WARNING_EMITTED = True

    from smonitor.integrations import context_extra, emit_from_catalog
    from molsysmt._private.smonitor import CATALOG, META, PACKAGE_ROOT

    emit_from_catalog(
        CATALOG["warnings"]["NumbaJitWarning"],
        package_root=PACKAGE_ROOT,
        meta=META,
        extra=context_extra(
            caller="molsysmt._private.jit._emit_numba_jit_warning",
            operation="jit_compile",
            extra={"kernel": func.__name__, "module": func.__module__, "cache_state": "cold"},
        ),
    )


def lazy_njit(signature, cache=True, **kwargs):
    """Returning a lazily-compiled Numba function with a fixed signature."""

    def decorator(func):
        @lru_cache(maxsize=1)
        def _compiled():
            # Check global parallel_mode configuration
            import molsysmt.configure as config
            compile_parallel = kwargs.get('parallel', False)
            if compile_parallel and config.parallel_mode is False:
                compile_parallel = False

            # Build compilation keyword arguments
            jit_kwargs = kwargs.copy()
            jit_kwargs['parallel'] = compile_parallel
            if 'fastmath' not in jit_kwargs:
                jit_kwargs['fastmath'] = True

            if wrapper in _COMPILING:
                compiled_dispatcher = nb.njit(signature, cache=cache, **jit_kwargs)(func)
                compiled_dispatcher._compiled_parallel = compile_parallel
                return compiled_dispatcher

            _COMPILING.add(wrapper)
            try:
                # Ensure dependencies are compiled and bound to their dispatchers.
                for name in func.__code__.co_names:
                    if name not in func.__globals__:
                        continue
                    value = func.__globals__[name]
                    if callable(value) and value in _WRAPPER_COMPILED and value is not wrapper:
                        func.__globals__[name] = _WRAPPER_COMPILED[value]()

                _emit_numba_jit_warning(func)
                compiled_dispatcher = nb.njit(signature, cache=cache, **jit_kwargs)(func)
                compiled_dispatcher._compiled_parallel = compile_parallel
                return compiled_dispatcher
            finally:
                _COMPILING.discard(wrapper)

        @wraps(func)
        def wrapper(*args, **kwds):
            compiled_dispatcher = _compiled()
            
            # Manage thread pool at runtime if compiled as a parallel JIT kernel
            if getattr(compiled_dispatcher, '_compiled_parallel', False):
                try:
                    import molsysmt.configure as config
                    import numpy as np
                    p_mode = config.parallel_mode
                    n_threads = config.num_threads

                    if p_mode is False:
                        nb.set_num_threads(1)
                    elif p_mode == 'auto':
                        # Determine payload size from largest numpy array argument
                        payload_size = 0
                        for arg in args:
                            if isinstance(arg, np.ndarray):
                                if arg.size > payload_size:
                                    payload_size = arg.size

                        if payload_size < config.parallel_threshold:
                            nb.set_num_threads(1)
                        else:
                            # Workload-based optimal scaling
                            optimal = max(1, payload_size // config.min_payload_per_thread)
                            
                            # Limit max threads
                            if n_threads == -1:
                                import multiprocessing
                                max_cores = multiprocessing.cpu_count()
                            else:
                                max_cores = n_threads
                            
                            final_threads = min(max_cores, optimal)
                            nb.set_num_threads(final_threads)
                    elif p_mode is True:
                        if n_threads == -1:
                            import multiprocessing
                            nb.set_num_threads(multiprocessing.cpu_count())
                        else:
                            nb.set_num_threads(n_threads)
                except Exception:
                    pass

            return compiled_dispatcher(*args, **kwds)

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
