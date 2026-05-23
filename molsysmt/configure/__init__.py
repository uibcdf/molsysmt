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
        'time_step':'2.0 femtoseconds',
        'platform':'CUDA',
        }

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
use_gpu = False          # True | False | 'auto'
gpu_threshold = 3_000_000  # payload (n_structures * n_atoms * 3) above which 'auto' uses GPU

# Dynamic Parallel JIT & Thread Controls
parallel_mode = 'auto'         # 'auto' | True | False
num_threads = -1               # -1 (all available cores) | positive integer
parallel_threshold = 500_000   # payload size threshold (n_structures * n_atoms * 3)
min_payload_per_thread = 250_000 # workload-based optimal scale per thread

class configure_context:
    """Context manager to temporarily override global configurations in a thread-safe manner."""
    def __init__(self, **kwargs):
        self.new_values = kwargs
        self.old_values = {}

    def __enter__(self):
        import sys
        module = sys.modules[__name__]
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
    """Decorator to automatically apply parallel and num_threads local overrides thread-safely."""
    from functools import wraps
    @wraps(func)
    def wrapper(*args, **kwargs):
        parallel = kwargs.get('parallel', None)
        num_threads = kwargs.get('num_threads', None)
        
        ctx_kwargs = {}
        if parallel is not None:
            ctx_kwargs['parallel_mode'] = parallel
        if num_threads is not None:
            ctx_kwargs['num_threads'] = num_threads
            
        with context(**ctx_kwargs):
            return func(*args, **kwargs)
    return wrapper


