from molsysmt.form.string_pdb_id.is_string_pdb_id import is_string_pdb_id as is_form
from molsysmt.form.string_pdb_id.extract import extract
from molsysmt.form.string_pdb_id.add import add
from molsysmt.form.string_pdb_id.append_structures import append_structures
from molsysmt.form.string_pdb_id.get import *
from molsysmt.form.string_pdb_id.set import *
from .form_attributes import form_attributes

form_name = 'string:pdb_id'
form_type = 'string'
form_info = ["", ""]

form_attributes = form_attributes()
form_attributes['atom_index'] = True
form_attributes['atom_id'] = True
form_attributes['atom_name'] = True
form_attributes['atom_type'] = True
form_attributes['group_index'] = True
form_attributes['group_id'] = True
form_attributes['group_name'] = True
form_attributes['group_type'] = True
form_attributes['molecule_index'] = True
form_attributes['molecule_id'] = True
form_attributes['molecule_name'] = True
form_attributes['molecule_type'] = True
form_attributes['chain_index'] = True
form_attributes['chain_id'] = True
form_attributes['chain_name'] = True
form_attributes['chain_type'] = True
form_attributes['entity_index'] = True
form_attributes['entity_id'] = True
form_attributes['entity_name'] = True
form_attributes['entity_type'] = True
form_attributes['coordinates'] = True
form_attributes['box'] = True
form_attributes['bioassemblies'] = True
form_attributes['occupancy'] = True
form_attributes['alternate_location'] = True
form_attributes['b_factor'] = True
form_attributes['formal_charge'] = True
form_attributes['partial_charge'] = True


def to_file_pdb(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.string_pdb_id import to_file_pdb as string_pdb_id_to_file_pdb

    return string_pdb_id_to_file_pdb(item, atom_indices=atom_indices,
                                     structure_indices=structure_indices,
                                     output_filename=output_filename)


def to_file_mmtf(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.string_pdb_id import to_file_mmtf as string_pdb_id_to_file_mmtf

    return string_pdb_id_to_file_mmtf(item, atom_indices=atom_indices,
                                      structure_indices=structure_indices,
                                      output_filename=output_filename)


def to_file_msmpk(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from molsysmt.form.string_pdb_id import to_file_msmpk as string_pdb_id_to_file_msmpk

    return string_pdb_id_to_file_msmpk(item, atom_indices=atom_indices,
                                       structure_indices=structure_indices,
                                       output_filename=output_filename)


def to_file_fasta(item, molecular_system, atom_indices='all', structure_indices='all', output_filename=None):
    from sabueso.tools.string_pdb_id import to_file_fasta as string_pdb_id_to_file_fasta
    from sabueso.tools.file_fasta import extract as extract_file_fasta
    from sabueso.basic import get
    import numpy as np

    tmp_item = string_pdb_id_to_file_fasta(item)
    group_indices = get(molecular_system, element='atom', indices=atom_indices, group_index=True)
    group_indices = np.unique(group_indices)
    return extract_file_fasta(tmp_item, group_indices=group_indices, output_filename=output_filename, copy_if_all=False)


def to_mmtf_MMTFDecoder(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_mmtf_MMTFDecoder as string_pdb_id_to_mmtf_MMTFDecoder

    return string_pdb_id_to_mmtf_MMTFDecoder(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all',
        bioassembly_name=None):
    from molsysmt.form.string_pdb_id import to_molsysmt_MolSys as string_pdb_id_to_molsysmt_MolSys

    return string_pdb_id_to_molsysmt_MolSys(item, atom_indices=atom_indices,
            structure_indices=structure_indices, bioassembly_name=bioassembly_name)


def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_molsysmt_Topology as string_pdb_id_to_molsysmt_Topology

    return string_pdb_id_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_molsysmt_Structures(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_molsysmt_Structures as string_pdb_id_to_molsysmt_Structures

    return string_pdb_id_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_mdtraj_Trajectory as string_pdb_id_to_mdtraj_Trajectory

    return string_pdb_id_to_mdtraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdtraj_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_mdtraj_Topology as string_pdb_id_to_mdtraj_Topology

    return string_pdb_id_to_mdtraj_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_parmed_Structure(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_parmed_Structure as string_pdb_id_to_parmed_Structure

    return string_pdb_id_to_parmed_Structure(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_pdbfixer_PDBFixer(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_pdbfixer_PDBFixer as string_pdb_id_to_pdbfixer_PDBFixer

    return string_pdb_id_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Modeller(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_openmm_Modeller as string_pdb_id_to_openmm_Modeller

    return string_pdb_id_to_openmm_Modeller(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_openmm_Topology as string_pdb_id_to_openmm_Topology

    return string_pdb_id_to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_openmm_PDBFile(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_openmm_PDBFile as string_pdb_id_to_openmm_PDBFile

    return string_pdb_id_to_openmm_PDBFile(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_mdanalysis_Universe(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_mdanalysis_Universe as string_pdb_id_to_mdanalysis_Universe

    return string_pdb_id_to_mdanalysis_Universe(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_pytraj_Trajectory(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_pytraj_Trajectory as string_pdb_id_to_pytraj_Trajectory

    return string_pdb_id_to_pytraj_Trajectory(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_string_pdb_text(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_string_pdb_text as string_pdb_id_to_string_pdb_text

    return string_pdb_id_to_string_pdb_text(item, atom_indices=atom_indices, structure_indices=structure_indices)


def to_nglview_NGLWidget(item, molecular_system, atom_indices='all', structure_indices='all'):
    from molsysmt.form.string_pdb_id import to_nglview_NGLWidget as string_pdb_id_to_nglview_NGLWidget

    return string_pdb_id_to_nglview_NGLWidget(item, atom_indices=atom_indices, structure_indices=structure_indices)
