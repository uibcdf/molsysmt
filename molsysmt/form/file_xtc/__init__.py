form_name = "file:xtc"
form_type = "file"
form_info = ["", ""]

piped_topological_attribute = None
piped_structural_attribute = "mdtraj.XTCTrajectoryFile"
piped_any_attribute = None

# Form metadata and export initialization retain their established import order.
# isort: off
from .is_form import is_form  # noqa: E402

from .attributes import attributes  # noqa: E402
from .has_attribute import has_attribute  # noqa: E402

from .extract import extract  # noqa: E402
from .copy import copy  # noqa: E402
from .add import add  # noqa: E402
from .merge import merge  # noqa: E402
from .append_structures import append_structures  # noqa: E402
from .get_topological_attributes import *  # noqa: E402, F403
from .get_structural_attributes import *  # noqa: E402, F403
from .set import *  # noqa: E402, F403
from .iterators import StructuresIterator  # noqa: E402
# isort: on


_convert_to = {
    "file:xtc": "to_file_xtc",
    "mdtraj.Trajectory": "to_mdtraj_Trajectory",
    "mdtraj.XTCTrajectoryFile": "to_mdtraj_XTCTrajectoryFile",
    "molsysmt.Structures": "to_molsysmt_Structures",
    "file:h5msm": "to_file_h5msm",
}
_heavy_support = {
    "coordinates": True,
    "box": True,
}
bonds_are_explicit = False
bonds_can_be_computed = False
