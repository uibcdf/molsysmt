from importlib import import_module
from importlib.util import find_spec
from functools import wraps, lru_cache
import inspect
from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt.config.dependencies import dependencies as _dependencies_config

@lru_cache(maxsize=None)
def is_installed(module_name):
    """
    Checking if a module is installed (cached).

    This function checks if a module is installed without importing it.
    The result is cached for performance.

    Parameters
    ----------
    module_name : str
        Name of the module to check.

    Returns
    -------
    bool
        True if the module is installed, False otherwise.
    """
    return find_spec(module_name) is not None

def check_dependency(module_name, caller=None):
    """
    Checking if a module is installed.

    This function checks if a module is installed. If it is not, it raises a
    LibraryNotFoundError. It consults the central configuration to differentiate
    between hard and soft dependencies.

    Parameters
    ----------
    module_name : str
        Name of the module to check (must be a key in molsysmt.config.dependencies).
    caller : str, optional
        Name of the function that is checking the dependency.

    Raises
    ------
    LibraryNotFoundError
        If the module is a missing soft dependency.
    ValueError
        If the module_name is not registered in the configuration.
    """
    
    if module_name not in _dependencies_config:
        # Fallback for internal modules or unregistered deps
        # But ideally all external deps should be registered
        if not is_installed(module_name):
             raise LibraryNotFoundError(module_name, caller=caller)
        return

    config = _dependencies_config[module_name]

    if config.type == 'hard':
        # Hard dependencies are assumed to be present.
        # If they are missing, the package shouldn't have loaded.
        pass
    elif config.type == 'soft':
        if not is_installed(config.pypi): # Check the importable name
             raise LibraryNotFoundError(config.name, caller=caller)

def requires(library, when=None, action='error'):
    """
    Decorator to declare a dependency.

    This decorator serves two purposes:
    1. Runtime Validation: Checks if the dependency is installed before executing the function.
       Can be conditional based on arguments (e.g. engine='OpenMM').
    2. Metadata Registration: Tags the function with its requirements for introspection.

    Parameters
    ----------
    library : str
        Name of the library (key in molsysmt.config.dependencies).
    when : dict, optional
        Condition map {argument_name: value}. The dependency is checked ONLY 
        if the runtime argument matches this value.
    action : str, default 'error'
        'error': Raise LibraryNotFoundError if missing.
        'hide': (Reserved for future UI filtering).
    """
    def decorator(func):
        
        # 1. Metadata Registration
        if not hasattr(func, '_dependencies'):
            func._dependencies = []
        func._dependencies.append({'library': library, 'when': when, 'action': action})

        # Pre-compute signature for performance
        sig = inspect.signature(func)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            
            should_check = True
            
            # 2. Conditional Logic
            if when is not None:
                # Optimized binding: try to avoid full bind if possible
                # But for robustness with defaults, bind is safest.
                # Optimization can be added later if profiling shows overhead.
                bound = sig.bind(*args, **kwargs)
                bound.apply_defaults()
                arguments = bound.arguments
                
                for arg_name, required_value in when.items():
                    if arg_name not in arguments:
                        # Argument not present (and no default?), condition fails safely
                        should_check = False
                        break
                    
                    if arguments[arg_name] != required_value:
                        should_check = False
                        break
            
            if should_check:
                check_dependency(library, caller=func.__name__)
                
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

def info():
    """
    Display a summary of the dependency ecosystem.

    Returns
    -------
    pandas.io.formats.style.Styler
        A styled DataFrame showing the status of each library.
    """
    from pandas import DataFrame
    
    rows = []
    for key, dep in _dependencies_config.items():
        installed = is_installed(dep.pypi)
        rows.append({
            'Library': dep.name,
            'Status': 'Installed' if installed else 'Not Installed',
            'Type': dep.type.capitalize(),
            'Install (PyPI)': f"pip install {dep.pypi}",
            'Install (Conda)': f"conda install -c conda-forge {dep.conda}"
        })
        
    df = DataFrame(rows)
    df.sort_values(by=['Status', 'Type', 'Library'], ascending=[True, True, True], inplace=True)
    
    return df.style.hide(axis='index').set_properties(**{'text-align': 'left'})
