import os

from depdigest import DeclaredRegistry

from . import catalogue

# Adapter inspection is separate from guarded optional-engine execution.
current_dir = os.path.dirname(os.path.abspath(__file__))

_dict_modules = DeclaredRegistry(
    package_prefix="molsysmt.form",
    directory=current_dir,
    declarations={name: catalogue.plugin_of(name) for name in catalogue.form_names()},
    attr_name="form_name",
    load_policy="adapter",
)


def __getattr__(name):
    if name == "_dict_forms_lowercase":
        return {ii.lower(): ii for ii in _dict_modules.keys()}
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# The registry is initialized before these public helpers are imported.
# isort: off
from .get_attributes import get_attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402
from .is_item import is_item  # noqa: E402
from .is_file import is_file  # noqa: E402
from .load_converter import load_converter  # noqa: E402
from .is_string import is_string  # noqa: E402
from .read_pdbqt_poses import read_pdbqt_poses  # noqa: E402
from .compose_atom_maps import compose_atom_maps  # noqa: E402
from .project_atom_names import project_atom_names  # noqa: E402
# isort: on

RESOURCE_FORMS = {
    "mdtraj.HDF5TrajectoryFile",
    "mdtraj.XTCTrajectoryFile",
    "mdtraj.DCDTrajectoryFile",
    "molsysmt.H5MSMFileHandler",
    "molsysmt.GROFileHandler",
    "molsysmt.PDBFileHandler",
}


def close(item):
    """
    Explicitly closing a resource form object or file handler.

    Parameters
    ----------
    item : object
        Item in any resource form (e.g. file handler or stream).

    Returns
    -------
    None
        Modifies item by closing its handle.

    .. versionadded:: 1.0.0
    """
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
