# Configuration file for MolSysMT

from .logging_setup import setup_logging
from molsysmt._private.argdigest import arg_digest

# Set this variable true while testing
_testing = False

# Set this variable true while debugging
_debugging = False

# Default attribute values

default_attribute = {
    "box": None,
    "structure_id": None,
    "box": None,
    "coordinates": None,
    "time": None,
    "forcefield": "AMBER14",
    "implicit_solvent": None,
    "water_model": "TIP3P",
    "non_bonded_method": "no cutoff",
    "constraints": "hbonds",
    "dispersion_correction": False,
    "switch_distance": None,
    "ewald_error_tolerance": 0.0005,
    "integrator": "Langevin",
    "temperature": "0.0 kelvin",
    "friction": "1.0/picoseconds",
    "platform": "CPU",
    "time_step": "1.0 femtoseconds",
}

# Default viewer
default_viewer = "MolSysViewer"


# Selection sortcuts
selection_shortcuts = {
    "MolSysMT": {
        "backbone": '(molecule_type==["protein", "peptide"] and atom_name==["CA", "N", "C", "O"])',
        "heavy atoms not solvent": '(atom_name!=["H"]) and (molecule_type!=["water", "ion"])',
        "heavy atoms": '(atom_name!=["H"])',
        "not solvent": '(molecule_type==["water", "ion"])',
        "solvent": '(molecule_type==["water", "ion"])',
        "hydrogens": '(atom_type=="H")',
        "hydrogen": '(atom_type=="H")',
    }
}

# Sphinx

# Is sphinx working?
# from os import environ
# _sphinx_is_working = ('SPHINXWORKING' in environ)
# del(environ)
#
## NGLview
# _view_from_htmlfiles=False
# if _sphinx_is_working:
#    _view_from_htmlfiles=True

# Optimization
large_list_length = 10000

# Visibility
show_all_capabilities = True

# Some third-party parsers write progress or format notes straight to the C stdout,
# with no verbosity switch of their own. MDTraj's DCD reader prints two lines per
# open, which floods any loop over trajectories. Set this to False to let that
# output through, for instance while diagnosing a malformed file.
silence_backend_stdout = True

# Heavy trajectory processing
import os as _os

max_ram_usage = int(
    0.5 * _os.sysconf("SC_PAGE_SIZE") * _os.sysconf("SC_PHYS_PAGES")
)  # 50% of total RAM in bytes
heavy_mode = "auto"  # 'auto' | 'force' | 'off'
chunk_size = 100  # default number of frames per chunk
emit_heavy_telemetry = True
memory_pressure_threshold = 0.80  # warn when RSS exceeds this fraction of max_ram_usage
chunk_memory_fraction = (
    0.10  # maximum safe fraction of max_ram_usage allocated to a single chunk
)
del _os

# Topology
min_length_protein = 50

# Reserved GPU compatibility controls. MolSysMT 1.0 has no supported GPU
# backend; explicit requests fall back to the Rust CPU kernels.
gpu_mode = "auto"  # 'auto' | True | False
use_gpu = "auto"  # kept for backward compatibility; alias for gpu_mode
gpu_threshold = (
    3_000_000  # payload (n_structures * n_atoms * 3) above which 'auto' uses GPU
)
gpu_backend = None
precision = "double"  # 'double' (float64) | 'single' (float32)
cell_list = "auto"  # 'auto' | True | False

# Native CPU parallelization policy
parallel_mode = "auto"  # 'auto' | True | False
num_threads = -1  # -1 (all processors available to the process) | positive integer
parallel_threshold = 500_000
min_payload_per_thread = 250_000

from contextvars import ContextVar as _ContextVar

_parallel_override = _ContextVar(
    "molsysmt_parallel_override",
    default=(None, None),
)


@arg_digest()
def set_parallelization(parallel="auto", num_threads=-1):
    """
    Configuring native CPU parallelization for the current session.

    Parameters
    ----------
    parallel : bool or str, default 'auto'
        Whether native kernels run in parallel. ``'auto'`` selects a pool size
        from the workload and configured resource limit.
    num_threads : int
        Maximum number of Rayon worker threads. Use ``-1`` for all processors
        available to the current process.

    Returns
    -------
    dict
        Session policy with ``parallel`` and ``num_threads`` entries.

    Notes
    -----
    Per-function ``parallel`` and ``num_threads`` arguments override this
    policy only for that call. MolSysMT caches Rayon pools by size, so changing
    the session policy does not rebuild kernels or mutate an irreversible
    process-global pool.

    .. versionadded:: 1.0.0
    """
    globals()["parallel_mode"] = parallel
    globals()["num_threads"] = num_threads
    return {"parallel": parallel, "num_threads": num_threads}


@arg_digest()
def set_num_threads(num_threads):
    """
    Configuring the native CPU thread limit for the current session.

    Parameters
    ----------
    num_threads : int
        Maximum number of Rayon worker threads. Use ``-1`` for all processors
        available to the current process.

    Returns
    -------
    int
        Configured session value.

    .. versionadded:: 1.0.0
    """
    globals()["num_threads"] = num_threads
    return num_threads


def get_num_threads():
    """
    Getting the native CPU thread limit for the current session.

    Returns
    -------
    int
        Configured value. ``-1`` means all processors available to the process.

    .. versionadded:: 1.0.0
    """
    return num_threads


def _get_effective_num_threads(payload_size):
    """Resolve the active session and per-call policy to a Rayon pool size."""
    from math import ceil
    import molsysmt._rust as _rust

    call_parallel, call_num_threads = _parallel_override.get()
    mode = parallel_mode if call_parallel is None else call_parallel
    requested = num_threads if call_num_threads is None else call_num_threads

    if mode is None:
        mode = "auto"
    if isinstance(mode, str):
        mode = mode.lower()
    if mode not in {"auto", True, False}:
        raise ValueError("parallel must be True, False, or 'auto'")

    if requested == -1:
        limit = _rust.get_available_num_threads()
    elif isinstance(requested, int) and requested > 0:
        limit = requested
    else:
        raise ValueError("num_threads must be -1 or a positive integer")

    if mode is False or limit == 1:
        return 1
    if mode is True:
        return limit

    if payload_size < parallel_threshold:
        return 1
    workload_threads = max(2, ceil(payload_size / min_payload_per_thread))
    return min(limit, workload_threads)


def _resolve_num_threads(*payloads):
    """Return the effective pool size for array-like kernel payloads."""
    payload_size = max(
        (getattr(payload, "size", 0) for payload in payloads if payload is not None),
        default=0,
    )
    return _get_effective_num_threads(payload_size)


class configure_context:
    """Context manager to temporarily override global configurations in a thread-safe manner."""

    def __init__(self, **kwargs):
        self.new_values = dict(kwargs)
        self.old_values = {}

    def __enter__(self):
        import sys

        module = sys.modules[__name__]

        # Symmetrically synchronize gpu_mode and use_gpu aliases if one is specified
        if "gpu_mode" in self.new_values and "use_gpu" not in self.new_values:
            self.new_values["use_gpu"] = self.new_values["gpu_mode"]
        elif "use_gpu" in self.new_values and "gpu_mode" not in self.new_values:
            self.new_values["gpu_mode"] = self.new_values["use_gpu"]

        for k, v in self.new_values.items():
            if hasattr(module, k):
                self.old_values[k] = getattr(module, k)
            setattr(module, k, v)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import sys

        module = sys.modules[__name__]
        for k, v in self.old_values.items():
            setattr(module, k, v)


def context(**kwargs):
    """Return a configure_context to temporarily modify configuration attributes."""
    return configure_context(**kwargs)


def with_configure_overrides(func):
    """Apply reversible per-call configuration overrides."""
    from functools import wraps
    from inspect import signature

    function_signature = signature(func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        arguments = function_signature.bind_partial(*args, **kwargs).arguments
        parallel = arguments.get("parallel", None)
        call_num_threads = arguments.get("num_threads", None)
        use_gpu_val = arguments.get("use_gpu", None)
        gpu_mode_val = arguments.get("gpu_mode", None)
        gpu_backend_val = arguments.get("gpu_backend", None)
        precision_val = arguments.get("precision", None)
        cell_list_val = arguments.get("cell_list", None)

        ctx_kwargs = {}
        if use_gpu_val is not None:
            ctx_kwargs["gpu_mode"] = use_gpu_val
            ctx_kwargs["use_gpu"] = use_gpu_val
        if gpu_mode_val is not None:
            ctx_kwargs["gpu_mode"] = gpu_mode_val
            ctx_kwargs["use_gpu"] = gpu_mode_val
        if gpu_backend_val is not None:
            ctx_kwargs["gpu_backend"] = gpu_backend_val
        if precision_val is not None:
            ctx_kwargs["precision"] = precision_val
        if cell_list_val is not None:
            ctx_kwargs["cell_list"] = cell_list_val
        if parallel is False and call_num_threads not in {None, 1}:
            from molsysmt._private.smonitor import ArgumentConflictError

            raise ArgumentConflictError(
                arg1="parallel",
                arg2="num_threads",
                reason="parallel=False is only compatible with num_threads=None or 1.",
                caller=func.__module__ + "." + func.__name__,
            )

        inherited_parallel, inherited_num_threads = _parallel_override.get()
        active_parallel = (
            inherited_parallel if parallel is None else parallel
        )
        active_num_threads = (
            inherited_num_threads if call_num_threads is None else call_num_threads
        )
        token = _parallel_override.set((active_parallel, active_num_threads))
        try:
            with context(**ctx_kwargs):
                return func(*args, **kwargs)
        finally:
            _parallel_override.reset(token)

    return wrapper
