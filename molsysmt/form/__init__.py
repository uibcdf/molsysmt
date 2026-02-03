import os
import logging
from importlib import import_module
from molsysmt import config
from molsysmt.dependencies import is_installed
from molsysmt.config.dependencies import form_dir_to_library, dependencies as _dependencies_config
from molsysmt._private.exceptions import LibraryNotFoundError

logger = logging.getLogger(__name__)

class _FormsDictionary(dict):
    """
    Dynamic dictionary for form modules.
    It populates itself lazily and filters based on current configuration.
    """
    _initialized = False
    _initializing = False

    def _ensure_initialized(self):
        if self._initialized:
            return
        
        # Prevent recursive calls during initialization
        if self._initializing:
            return

        self._initializing = True
        try:
            self._initialize_forms()
            self._initialized = True
        finally:
            self._initializing = False

    def _initialize_forms(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for f in os.scandir(current_dir):
            if f.is_dir() and f.name not in ['__pycache__']:
                
                # Check if this form directory has a known dependency
                lib_key = form_dir_to_library.get(f.name)
                
                if lib_key:
                    # If the library is soft and missing, and the user wants to filter...
                    if not config.show_all_capabilities:
                        dep_info = _dependencies_config.get(lib_key)
                        if dep_info and dep_info.type == 'soft':
                            if not is_installed(dep_info.pypi):
                                continue # Skip registration

                try:
                    mod = import_module('molsysmt.form.'+f.name)
                    self[mod.form_name] = mod
                except (ImportError, LibraryNotFoundError) as e:
                    # Expected if a soft dependency is missing and not fully shielded
                    if show_all_capabilities:
                        logger.debug(f"Form module '{f.name}' skipped due to missing dependency: {e}")
                except Exception as e:
                    # Unexpected error in form implementation
                    logger.warning(f"Failed to load form module '{f.name}': {e}")

    def __getitem__(self, key):
        self._ensure_initialized()
        return super().__getitem__(key)

    def __contains__(self, key):
        self._ensure_initialized()
        return super().__contains__(key)

    def keys(self):
        self._ensure_initialized()
        return super().keys()

    def values(self):
        self._ensure_initialized()
        return super().values()

    def items(self):
        self._ensure_initialized()
        return super().items()

    def get(self, key, default=None):
        self._ensure_initialized()
        return super().get(key, default)

_dict_modules = _FormsDictionary()

def __getattr__(name):
    """
    Module-level getattr to handle dynamic attributes like _dict_forms_lowercase.
    """
    if name == '_dict_forms_lowercase':
        _dict_modules._ensure_initialized()
        return {ii.lower(): ii for ii in _dict_modules.keys()}
    
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# For backward compatibility with the rest of the code that expects these functions
from .get_attributes import get_attributes
from .has_attribute import has_attribute
from .is_item import is_item
from .is_file import is_file
from .is_string import is_string
