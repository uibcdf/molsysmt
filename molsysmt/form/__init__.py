import os
from depdigest import LazyRegistry

# Initialize the generic LazyRegistry from depdigest
# It will automatically find molsysmt._depdigest and handle filtering
current_dir = os.path.dirname(os.path.abspath(__file__))

_dict_modules = LazyRegistry(
    package_prefix='molsysmt.form',
    directory=current_dir,
    attr_name='form_name'
)

def __getattr__(name):
    if name == '_dict_forms_lowercase':
        return {ii.lower(): ii for ii in _dict_modules.keys()}
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

from .get_attributes import get_attributes
from .has_attribute import has_attribute
from .is_item import is_item
from .is_file import is_file
from .is_string import is_string

RESOURCE_FORMS = {
    'mdtraj.HDF5TrajectoryFile',
    'mdtraj.XTCTrajectoryFile',
    'mdtraj.DCDTrajectoryFile',
    'molsysmt.H5MSMFileHandler',
    'molsysmt.GROFileHandler',
    'molsysmt.PDBFileHandler',
}

def close(item):
    """Explicitly close a resource form if it is registered in RESOURCE_FORMS."""
    from molsysmt.basic import get_form
    try:
        form = get_form(item)
        if form in RESOURCE_FORMS:
            item.close()
    except Exception:
        pass

piped_topological_attribute = None
piped_structural_attribute = None
piped_any_attribute = None
bonds_are_explicit = False
bonds_can_be_computed = False
