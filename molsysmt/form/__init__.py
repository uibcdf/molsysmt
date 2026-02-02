import os
from importlib import import_module
from molsysmt.config import show_all_capabilities
from molsysmt.dependencies import is_installed
from molsysmt.config.dependencies import form_dir_to_library, dependencies as _dependencies_config

class _FormsDictionary(dict):
    """
    Dynamic dictionary for form modules.
    It populates itself lazily and filters based on current configuration.
    """
    _initialized = False

    def _ensure_initialized(self):
        if not self._initialized:
            self._initialize_forms()
            self._initialized = True

    def _initialize_forms(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        for f in os.scandir(current_dir):
            if f.is_dir() and f.name not in ['__pycache__']:
                
                # Check if this form directory has a known dependency
                lib_key = form_dir_to_library.get(f.name)
                
                if lib_key:
                    # If the library is soft and missing, and the user wants to filter...
                    if not show_all_capabilities:
                        dep_info = _dependencies_config.get(lib_key)
                        if dep_info and dep_info.type == 'soft':
                            if not is_installed(dep_info.pypi):
                                continue # Skip registration

                try:
                    mod = import_module('molsysmt.form.'+f.name)
                    self[mod.form_name] = mod
                except Exception:
                    # Robustness: skip forms that fail to import for any reason
                    pass

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

# Note: _dict_forms_lowercase will also need to be lazy if we want full consistency,
# but since it's mostly used internally after _dict_modules is accessed, we can 
# handle it or make it a property.

@property
def _dict_forms_lowercase():
    _dict_modules._ensure_initialized()
    return {ii.lower(): ii for ii in _dict_modules.keys()}

# For backward compatibility with the rest of the code that expects these functions
from .get_attributes import get_attributes
from .has_attribute import has_attribute
from .is_item import is_item
from .is_file import is_file
from .is_string import is_string