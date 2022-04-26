from molsysmt._private.exceptions import *

from molsysmt.form.file_gro.is_file_gro import is_file_gro as is_form
from molsysmt.form.file_gro.extract import extract
from molsysmt.form.file_gro.add import add
from molsysmt.form.file_gro.append_structures import append_structures
from molsysmt.form.file_gro.get import *
from molsysmt.form.file_gro.set import *

form_name='file:gro'
form_type='file'
form_info=["Gromacs gro file format","http://manual.gromacs.org/documentation/2018/user-guide/file-formats.html#gro"]

form_attributes = {

    'atom_index' : True,
    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_index' : True,
    'bond_id' : True,
    'bond_name' : True,
    'bond_type' : True,
    'bond_order' : True,

    'group_index' : True,
    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_index' : False,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : False,
    'molecule_id' : False,
    'molecule_name' : False,
    'molecule_type' : False,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : True,
    'velocities' : True,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield_parameters' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_molsysmt_MolSys as file_gro_to_molsysmt_MolSys

    tmp_item = file_gro_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                          structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_molsysmt_Topology as file_gro_to_molsysmt_Topology

    tmp_item = file_gro_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_molsysmt_Structures as file_gro_to_molsysmt_Structures

    tmp_item = file_gro_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                               structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_openmm_Topology as file_gro_to_openmm_Topology

    tmp_item = file_gro_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_openmm_Modeller as file_gro_to_openmm_Modeller

    tmp_item = file_gro_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_openmm_GromacsGroFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_openmm_GromacsGroFile as file_gro_to_openmm_GromacsGroFile

    tmp_item = file_gro_to_openmm_GromacsGroFile(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_gro import to_nglview_NGLWidget as file_gro_to_nglview_NGLWidget

    tmp_item = file_gro_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

