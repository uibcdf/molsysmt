from molsysmt.form.pdbfixer_PDBFixer.is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer as is_form
from molsysmt.form.pdbfixer_PDBFixer.extract import extract
from molsysmt.form.pdbfixer_PDBFixer.add import add
from molsysmt.form.pdbfixer_PDBFixer.append_structures import append_structures
from molsysmt.form.pdbfixer_PDBFixer.get import *
from molsysmt.form.pdbfixer_PDBFixer.set import *
from molsysmt.form.pdbfixer_PDBFixer.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name = 'pdbfixer.PDBFixer'
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


def to_string_aminoacids3(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_string_aminoacids3 as pdbfixer_PDBFixer_to_string_aminoacids3

    return pdbfixer_PDBFixer_to_string_aminoacids3(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_string_aminoacids1(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_string_aminoacids1 as pdbfixer_PDBFixer_to_string_aminoacids1

    return pdbfixer_PDBFixer_to_string_aminoacids1(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_biopython_Seq(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_biopython_Seq as pdbfixer_PDBFixer_to_biopython_Seq

    return pdbfixer_PDBFixer_to_biopython_Seq(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_biopython_SeqRecord(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_biopython_Seq as pdbfixer_PDBFixer_to_biopython_Seq

    return pdbfixer_PDBFixer_to_biopython_SeqRecord(item, atom_indices=atom_indices,
                                                    structure_indices=structure_indices, digest=False)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_mdtraj_Topology as pdbfixer_PDBFixer_to_mdtraj_Topology

    return pdbfixer_PDBFixer_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_mdtraj_Trajectory as pdbfixer_PDBFixer_to_mdtraj_Trajectory

    return pdbfixer_PDBFixer_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_openmm_Modeller as pdbfixer_PDBFixer_to_openmm_Modeller

    return pdbfixer_PDBFixer_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_openmm_Topology as pdbfixer_PDBFixer_to_openmm_Topology

    return pdbfixer_PDBFixer_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_molsysmt_Topology as pdbfixer_PDBFixer_to_molsysmt_Topology

    return pdbfixer_PDBFixer_to_molsysmt_Topology(item, atom_indices=atom_indices, digest=False)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_molsysmt_MolSys as pdbfixer_PDBFixer_to_molsysmt_MolSys

    return pdbfixer_PDBFixer_to_molsysmt_MolSys(item, atom_indices=atom_indices, digest=False)


def to_parmed_Structure(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_parmed_Structure as pdbfixer_PDBFixer_to_parmed_Structure

    return pdbfixer_PDBFixer_to_parmed_Structure(item, atom_indices=atom_indices, digest=False)


def to_file_pdb(item, molecular_system=None, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.pdbfixer_PDBFixer import to_file_pdb as pdbfixer_PDBFixer_to_file_pdb

    return pdbfixer_PDBFixer_to_file_pdb(item, atom_indices=atom_indices, digest=False)


def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', structure_indices='all'):
    from molsysmt.form.pdbfixer_PDBFixer import to_nglview_NGLWidget as pdbfixer_PDBFixer_to_nglview_NGLWidget

    return pdbfixer_PDBFixer_to_nglview_NGLWidget(item, atom_indices=atom_indices, digest=False)
