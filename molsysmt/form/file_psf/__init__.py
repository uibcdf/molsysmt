form_name='file:psf'
form_type = 'file'
form_info = ["CHARMM Protein Structure File (PSF).","https://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node23.html"]

from .is_file_psf import is_file_psf

from .attributes import attributes

from .extract import extract
from .add import add
from .append_structures import append_structures
from .get import *
from .set import *
from .iterators import StructuresIterator, TopologyIterator

from .to_molsysmt_MolSys import to_molsysmt_MolSys, _to_molsysmt_MolSys
from .to_molsysmt_Topology import to_molsysmt_Topology, _to_molsysmt_Topology
from .to_openmm_CharmmPsfFile import to_openmm_CharmmPsfFile, _to_openmm_CharmmPsfFile
from .to_openmm_Topology import to_openmm_Topology, _to_openmm_Topology

_dict_convert={
        'molsysmt.MolSys': _to_molsysmt_MolSys,
        'molsysmt.Topology': _to_molsysmt_Topology,
        'openmm.CharmPsfFile': _to_openmm_CharmmPsfFile,
        'openmm.Topology': _to_openmm_Topology,
        }
