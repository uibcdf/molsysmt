form_name = 'file:inpcrd'
form_type = 'file'
form_info = ["AMBER ASCII restart/inpcrd file format",
             "https://ambermd.org/FileFormats.php#trajectory"]

from .is_file_inpcrd import is_file_inpcrd

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_AmberInpcrdFile import to_openmm_AmberInpcrdFile
from .to_mdtraj_AmberRestartFile import to_mdtraj_AmberRestartFile
from .to_molsysmt_Structures import to_molsysmt_Structures

_dict_convert={
        'openmm.AmberInpcrdFile': to_openmm_AmberInpcrdFile,
        'openmm.AmberRestartFile': to_openmm_AmberRestartFile,
        'molsysmt.Structures': to_molsysmt_Structures,
        }

