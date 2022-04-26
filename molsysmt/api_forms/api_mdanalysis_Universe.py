from molsysmt._private.exceptions import *
import numpy as np

from molsysmt.form.mdanalysis_Universe.is_mdanalysis_Universe import is_mdanalysis_Universe as is_form
from molsysmt.form.mdanalysis_Universe.extract import extract
from molsysmt.form.mdanalysis_Universe.add import add
from molsysmt.form.mdanalysis_Universe.append_structures import append_structures
from molsysmt.form.mdanalysis_Universe.get import *
from molsysmt.form.mdanalysis_Universe.set import *

form_name='mdanalysis.Universe'
form_type='class'
form_info=["",""]

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

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : False,
    'step' : False,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}

def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdanalysis_Universe import to_nglview_NGLWidget as mdanalysis_Universe_to_nglview_NGLWidget

    tmp_item = mdanalysis_Universe_to_nglview_NGLWidget(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):

    from molsysmt.form.mdanalysis_Universe import to_file_pdb as mdanalysis_Universe_to_file_pdb

    tmp_item = mdanalysis_Universe_to_file_pdb(item, atom_indices=atom_indices,
            structure_indices=structure_indices, output_filename=output_filename, check=False)

    return tmp_item

def to_mdtraj_Trajectory (item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdanalysis_Universe import to_mdtraj_Trajectory as mdanalysis_Universe_to_mdtraj_Trajectory

    tmp_item = mdanalysis_Universe_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_MolSys (item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdanalysis_Universe import to_molsysmt_MolSys as mdanalysis_Universe_to_molsysmt_MolSys

    tmp_item = mdanalysis_Universe_to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Structures (item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdanalysis_Universe import to_molsysmt_MolSys as mdanalysis_Universe_to_molsysmt_Structures

    tmp_item = mdanalysis_Universe_to_molsysmt_Structures(item, atom_indices=atom_indices,
            structure_indices=structure_indices, check=False)

    return tmp_item

def to_molsysmt_Topology (item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.mdanalysis_Universe import to_molsysmt_Topology as mdanalysis_Universe_to_molsysmt_Topology

    tmp_item = mdanalysis_Universe_to_molsysmt_Topology(item, atom_indices=atom_indices, check=False)

    return tmp_item

