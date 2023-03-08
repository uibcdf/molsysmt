form_name = 'file:inpcrd'
form_type = 'file'
form_info = ["AMBER ASCII restart/inpcrd file format",
             "https://ambermd.org/FileFormats.php#trajectory"]

from .is_form import is_form

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_openmm_AmberInpcrdFile import to_openmm_AmberInpcrdFile, _to_openmm_AmberInpcrdFile
from .to_mdtraj_AmberRestartFile import to_mdtraj_AmberRestartFile, _to_mdtraj_AmberRestartFile
from .to_molsysmt_Structures import to_molsysmt_Structures, _to_molsysmt_Structures

_convert_to={
        'openmm.AmberInpcrdFile': _to_openmm_AmberInpcrdFile,
        'mdtraj.AmberRestartFile': _to_mdtraj_AmberRestartFile,
        'molsysmt.Structures': _to_molsysmt_Structures,
        }

