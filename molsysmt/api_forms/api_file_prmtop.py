from molsysmt._private.exceptions import *

from molsysmt.form.file_prmtop.is_file_prmtop import is_file_prmtop as is_form
from molsysmt.form.file_prmtop.extract import extract
from molsysmt.form.file_prmtop.add import add
from molsysmt.form.file_prmtop.merge import merge
from molsysmt.form.file_prmtop.append_structures import append_structures
from molsysmt.form.file_prmtop.concatenate_structures import concatenate_structures
from molsysmt.form.file_prmtop.get import *
from molsysmt.form.file_prmtop.set import *

form_name='file:prmtop'
form_type='file'
form_info = ["AMBER parameter/topology file format","https://ambermd.org/FileFormats.php#topology"]

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

    'component_index' : True,
    'component_id' : False,
    'component_name' : False,
    'component_type' : False,

    'molecule_index' : True,
    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_index' : True,
    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_index' : False,
    'entity_id' : False,
    'entity_name' : False,
    'entity_type' : False,

    'coordinates' : False,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield_parameters' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.file_prmtop import to_file_pdb as file_prmtop_to_file_pdb
    from molsysmt.basic import get

    coordinates = get(molecular_system, target='atom', indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item = file_prmtop_to_file_pdb(item, atom_indices=atom_indices, coordinates=coordinates, output_filename=output_filename, check=False)

    return tmp_item

def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_mdtraj_Topology as file_prmtop_to_mdtraj_Topology

    tmp_item = file_prmtop_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_molsysmt_MolSys as file_prmtop_to_molsysmt_MolSys
    from molsysmt.basic import get

    coordinates = get(molecular_system, target='atom', indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item  = file_prmtop_to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_molsysmt_Topology as file_prmtop_to_molsysmt_Topology

    tmp_item  = file_prmtop_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_nglview_NGLWidget as file_prmtop_to_nglview_NGLWidget
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item  = file_prmtop_to_nglview_NGLWidget(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

def to_openmm_AmberPrmtopFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_openmm_AmberPrmtopFile as file_prmtop_to_openmm_AmberPrmtopFile

    tmp_item  = file_prmtop_to_nglview_NGLWidget(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_openmm_Topology as file_prmtop_to_openmm_Topology

    tmp_item  = file_prmtop_to_openmm_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_prmtop import to_openmm_Modeller as file_prmtop_to_openmm_Modeller
    from molsysmt.basic import get

    coordinates = get(molecular_system, atom_indices=atom_indices, structure_indices=structure_indices, coordinates=True, check=False)
    tmp_item = file_prmtop_to_openmm_Modeller(item, atom_indices=atom_indices, coordinates=coordinates, check=False)

    return tmp_item

