# Configuration file for MolSysMT

from contextvars import ContextVar as _ContextVar
from threading import RLock as _RLock
from types import ModuleType as _ModuleType

# Preserve configuration setup before argument digestion.
# isort: off
from .logging_setup import setup_logging
from ._memory import total_physical_memory_bytes as _total_physical_memory_bytes
from molsysmt._private.argdigest import arg_digest
# isort: on

# Set this variable true while testing
_testing = False

# Set this variable true while debugging
_debugging = False

# Default attribute values

default_attribute = {
    "box": None,
    "structure_id": None,
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
max_ram_usage = _total_physical_memory_bytes() // 2  # 50% of total RAM in bytes
heavy_mode = "auto"  # 'auto' | 'force' | 'off'
chunk_size = 100  # default number of frames per chunk
emit_heavy_telemetry = True
memory_pressure_threshold = 0.80  # warn when RSS exceeds this fraction of max_ram_usage
chunk_memory_fraction = (
    0.10  # maximum safe fraction of max_ram_usage allocated to a single chunk
)
del _total_physical_memory_bytes

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

_parallel_override = _ContextVar(
    "molsysmt_parallel_override",
    default=(None, None),
)
_configuration_lock = _RLock()


def _configuration_names():
    """Enumerate configurable public data without exposing implementation objects."""
    return tuple(
        name
        for name, value in globals().items()
        if not name.startswith("_")
        and not callable(value)
        and not isinstance(value, _ModuleType)
    )


def _normalize_context_overrides(values):
    """Validate the complete name/alias declaration before publishing any value."""
    from molsysmt._private.argdigest.argument.use_gpu import digest_use_gpu
    from molsysmt._private.smonitor import ArgumentConflictError, ArgumentError

    result = dict(values)
    names = _configuration_names()
    for name in result:
        if name not in names:
            raise ArgumentError(
                name,
                caller="molsysmt.configure.context",
                message="Only existing public configuration data can be overridden.",
            )
    for name in ("gpu_mode", "use_gpu"):
        if name in result:
            result[name] = digest_use_gpu(
                result[name], caller="molsysmt.configure.context"
            )
    if "gpu_mode" in result and "use_gpu" in result:
        if result["gpu_mode"] != result["use_gpu"]:
            raise ArgumentConflictError(
                arg1="gpu_mode",
                arg2="use_gpu",
                reason="The two compatibility aliases must declare the same policy.",
                caller="molsysmt.configure.context",
            )
    elif "gpu_mode" in result:
        result["use_gpu"] = result["gpu_mode"]
    elif "use_gpu" in result:
        result["gpu_mode"] = result["use_gpu"]
    return result


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
    with _configuration_lock:
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
    with _configuration_lock:
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
    """Overriding process-global data with serialized, reversible context writers.

    Use :func:`context` for the configuration contract. Contexts may nest and
    the same object may be reused. This synchronous context is not task-local
    and must not span awaits in overlapping asynchronous tasks.
    """

    # Axis 1 validates names; this configuration boundary deliberately preserves
    # operation-owned values. This spelling also supports the declared 0.14 floor.
    @arg_digest(digestion_source=None, strictness="ignore")
    def __init__(self, *, skip_digestion=False, **kwargs):
        if type(skip_digestion) is not bool:
            from molsysmt._private.smonitor import ArgumentError

            raise ArgumentError("skip_digestion", value=skip_digestion)
        self.new_values = _normalize_context_overrides(kwargs)
        self._snapshots = []

    def __enter__(self):
        _configuration_lock.acquire()
        try:
            values = _normalize_context_overrides(self.new_values)
            self._snapshots.append({name: globals()[name] for name in values})
            globals().update(values)
        except BaseException:
            _configuration_lock.release()
            raise
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            globals().update(self._snapshots.pop())
        finally:
            _configuration_lock.release()
        return False


@arg_digest(digestion_source=None, strictness="ignore")
def context(*, skip_digestion=False, **kwargs):
    """Overriding process-global configuration for one synchronous block.

    Parameters
    ----------
    skip_digestion : bool, default=False
        Whether to skip argument digestion for an already validated call.
    **kwargs : dict
        Existing public configuration data to replace temporarily. Unknown,
        private, callable and module names are rejected before any write.
        ``gpu_mode`` and ``use_gpu`` are synchronized compatibility aliases;
        contradictory values are rejected. Other values retain the contracts
        of the operations that consume those settings.

    Returns
    -------
    configure_context
        Reusable synchronous context restoring the previous values on exit,
        including exceptional exits.

    Raises
    ------
    UnknownArgumentError
        If a normal public call names data outside the configuration domain.
    ArgumentError
        If a configuration name or GPU compatibility policy is invalid.
    ArgumentConflictError
        If both GPU aliases specify different policies.

    Notes
    -----
    Writers are serialized for their full lifetime by a reentrant process
    lock. Nesting is supported. Concurrent code outside a context can observe
    temporary values; direct module assignments do not take the lock. Session
    setter functions participate in writer serialization. This is
    not thread/task-local isolation. Do not hold the context across an await
    in overlapping asynchronous tasks. Explicit CPU per-call controls remain
    context-local and calls without global overrides do not acquire this lock.
    Key and alias integrity checks still apply to trusted delegation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> previous = msm.configure.chunk_size
    >>> with msm.configure.context(chunk_size=2):
    ...     assert msm.configure.chunk_size == 2
    >>> msm.configure.chunk_size == previous
    True

    .. versionadded:: 1.0.0
    """
    if type(skip_digestion) is not bool:
        from molsysmt._private.smonitor import ArgumentError

        raise ArgumentError("skip_digestion", value=skip_digestion)
    values = _normalize_context_overrides(kwargs)
    return configure_context(skip_digestion=True, **values)


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
            ctx_kwargs["use_gpu"] = use_gpu_val
        if gpu_mode_val is not None:
            ctx_kwargs["gpu_mode"] = gpu_mode_val
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
        active_parallel = inherited_parallel if parallel is None else parallel
        active_num_threads = (
            inherited_num_threads if call_num_threads is None else call_num_threads
        )
        token = _parallel_override.set((active_parallel, active_num_threads))
        try:
            if not ctx_kwargs:
                return func(*args, **kwargs)
            with context(**ctx_kwargs):
                return func(*args, **kwargs)
        finally:
            _parallel_override.reset(token)

    return wrapper
