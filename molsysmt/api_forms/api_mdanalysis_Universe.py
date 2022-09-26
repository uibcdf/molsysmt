import numpy as np
from molsysmt.form.mdanalysis_Universe.is_mdanalysis_Universe import is_mdanalysis_Universe as is_form
from molsysmt.form.mdanalysis_Universe.extract import extract
from molsysmt.form.mdanalysis_Universe.add import add
from molsysmt.form.mdanalysis_Universe.append_structures import append_structures
from molsysmt.form.mdanalysis_Universe.get import *
from molsysmt.form.mdanalysis_Universe.set import *
from .form_attributes import form_attributes

form_name = 'mdanalysis.Universe'
form_type = 'class'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['bond_index'] = True
form_attributes['bond_id'] = True
form_attributes['bond_name'] = True
form_attributes['bond_type'] = True
form_attributes['bond_order'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['component_index'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdanalysis_Universe import to_nglview_NGLWidget as mdanalysis_Universe_to_nglview_NGLWidget

    return mdanalysis_Universe_to_nglview_NGLWidget(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.mdanalysis_Universe import to_file_pdb as mdanalysis_Universe_to_file_pdb

    return mdanalysis_Universe_to_file_pdb(item, atom_indices=atom_indices,
                                           structure_indices=structure_indices, output_filename=output_filename)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdanalysis_Universe import to_mdtraj_Trajectory as mdanalysis_Universe_to_mdtraj_Trajectory

    return mdanalysis_Universe_to_mdtraj_Trajectory(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdanalysis_Universe import to_molsysmt_MolSys as mdanalysis_Universe_to_molsysmt_MolSys

    return mdanalysis_Universe_to_molsysmt_MolSys(item, atom_indices=atom_indices,
                                                  structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdanalysis_Universe import to_molsysmt_MolSys as mdanalysis_Universe_to_molsysmt_Structures

    return mdanalysis_Universe_to_molsysmt_Structures(item, atom_indices=atom_indices,
                                                      structure_indices=structure_indices)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.mdanalysis_Universe import to_molsysmt_Topology as mdanalysis_Universe_to_molsysmt_Topology

    return mdanalysis_Universe_to_molsysmt_Topology(item, atom_indices=atom_indices)
