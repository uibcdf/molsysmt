# Configuration file for MolSysMT

from .logging_setup import setup_logging

# Set this variable true while testing
_testing = False

# Set this variable true while debugging
_debugging = False

# Default attribute values

default_attribute = {

        'box':None,
        'structure_id':None,
        'box':None,
        'coordinates':None,
        'time':None,

        'forcefield':'AMBER14',
        'implicit_solvent':None,
        'water_model':'TIP3P',
        'non_bonded_method':'no cutoff',
        'constraints':'hbonds',
        'dispersion_correction':False,
        'switch_distance':None,
        'ewald_error_tolerance':0.0005,
        'integrator':'Langevin',
        'temperature':'0.0 kelvin',
        'friction':'1.0/picoseconds',
        'platform':'CUDA',
        'time_step':'1.0 femtoseconds',
        }

# Default viewer
default_viewer = 'MolSysViewer'


# Selection sortcuts
selection_shortcuts={
        'MolSysMT': {
            'backbone':'(molecule_type==["protein", "peptide"] and atom_name==["CA", "N", "C", "O"])',
            'heavy atoms not solvent':'(atom_name!=["H"]) and (molecule_type!=["water", "ion"])',
            'heavy atoms':'(atom_name!=["H"])',
            'not solvent':'(molecule_type==["water", "ion"])',
            'solvent':'(molecule_type==["water", "ion"])',
            'hydrogens':'(atom_type=="H")',
            'hydrogen':'(atom_type=="H")',
            }
        }

# Sphinx

# Is sphinx working?
#from os import environ
#_sphinx_is_working = ('SPHINXWORKING' in environ)
#del(environ)
#
## NGLview
#_view_from_htmlfiles=False
#if _sphinx_is_working:
#    _view_from_htmlfiles=True

# Optimization
large_list_length = 10000

# Visibility
show_all_capabilities = True

# Heavy trajectory processing
import os as _os
max_ram_usage = int(0.5 * _os.sysconf('SC_PAGE_SIZE') * _os.sysconf('SC_PHYS_PAGES'))  # 50% of total RAM in bytes
heavy_mode = 'auto'         # 'auto' | 'force' | 'off'
chunk_size = 100            # default number of frames per chunk
emit_heavy_telemetry = True
memory_pressure_threshold = 0.80  # warn when RSS exceeds this fraction of max_ram_usage
chunk_memory_fraction = 0.10      # maximum safe fraction of max_ram_usage allocated to a single chunk
del _os

# Topology
min_length_protein = 50

# GPU acceleration
gpu_mode = 'auto'          # 'auto' | True | False
use_gpu = 'auto'           # kept for backward compatibility; alias for gpu_mode
gpu_threshold = 3_000_000  # payload (n_structures * n_atoms * 3) above which 'auto' uses GPU
gpu_backend = 'cuda'       # 'cuda' (Numba CUDA) | 'taichi' (Experimental Taichi Lang)
precision = 'double'       # 'double' (float64) | 'single' (float32)
cell_list = 'auto'         # 'auto' | True | False

# Dynamic Parallel JIT & Thread Controls
parallel_mode = 'auto'         # 'auto' | True | False
num_threads = -1               # -1 (all available cores) | positive integer
parallel_threshold = 500_000   # payload size threshold (n_structures * n_atoms * 3)
min_payload_per_thread = 250_000 # workload-based optimal scale per thread

# Compute kernel backend (Rust migration coexistence; see
# devguide/pending_proposals/rust_numba_coexistence_and_cut_plan.md).
#   'numba' : the JIT kernels (default; unchanged behaviour, no Rust wheel needed)
#   'rust'  : the Rust kernels (requires the optional 'msm_rust_kernels' wheel)
#   'auto'  : Rust when the wheel is importable, else Numba
# Numba remains the default until Rust wheels are proven across platforms; the flip to
# 'auto'/'rust' is the dogfooding step, not this landing.
kernel = 'numba'               # 'numba' | 'rust' | 'auto'

class configure_context:
    """Context manager to temporarily override global configurations in a thread-safe manner."""
    def __init__(self, **kwargs):
        self.new_values = dict(kwargs)
        self.old_values = {}

    def __enter__(self):
        import sys
        module = sys.modules[__name__]

        # Symmetrically synchronize gpu_mode and use_gpu aliases if one is specified
        if 'gpu_mode' in self.new_values and 'use_gpu' not in self.new_values:
            self.new_values['use_gpu'] = self.new_values['gpu_mode']
        elif 'use_gpu' in self.new_values and 'gpu_mode' not in self.new_values:
            self.new_values['gpu_mode'] = self.new_values['use_gpu']

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
    """Decorator to automatically apply parallel, num_threads, gpu_mode, gpu_backend, precision, and cell_list local overrides thread-safely."""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        parallel = kwargs.get('parallel', None)
        num_threads = kwargs.get('num_threads', None)
        use_gpu_val = kwargs.get('use_gpu', None)
        gpu_mode_val = kwargs.get('gpu_mode', None)
        gpu_backend_val = kwargs.get('gpu_backend', None)
        precision_val = kwargs.get('precision', None)
        cell_list_val = kwargs.get('cell_list', None)
        kernel_val = kwargs.get('kernel', None)

        ctx_kwargs = {}
        if parallel is not None:
            ctx_kwargs['parallel_mode'] = parallel
        if num_threads is not None:
            ctx_kwargs['num_threads'] = num_threads
        if use_gpu_val is not None:
            ctx_kwargs['gpu_mode'] = use_gpu_val
            ctx_kwargs['use_gpu'] = use_gpu_val
        if gpu_mode_val is not None:
            ctx_kwargs['gpu_mode'] = gpu_mode_val
            ctx_kwargs['use_gpu'] = gpu_mode_val
        if gpu_backend_val is not None:
            ctx_kwargs['gpu_backend'] = gpu_backend_val
        if precision_val is not None:
            ctx_kwargs['precision'] = precision_val
        if cell_list_val is not None:
            ctx_kwargs['cell_list'] = cell_list_val
        if kernel_val is not None:
            ctx_kwargs['kernel'] = kernel_val

        with context(**ctx_kwargs):
            return func(*args, **kwargs)
    return wrapper



