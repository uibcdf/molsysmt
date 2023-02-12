from molsysmt.form.file_psf.is_file_psf import is_file_psf as is_form
from molsysmt.form.file_psf.extract import extract
from molsysmt.form.file_psf.add import add
from molsysmt.form.file_psf.append_structures import append_structures
from molsysmt.form.file_psf.get import *
from molsysmt.form.file_psf.set import *
from molsysmt.form.file_psf.iterators import StructuresIterator, TopologyIterator
from .form_attributes import form_attributes

form_name='file:psf'
form_type = 'file'
form_info = ["CHARMM Protein Structure File (PSF).","https://www.ks.uiuc.edu/Training/Tutorials/namd/namd-tutorial-unix-html/node23.html"]

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
form_attributes['coordinates'] = False
form_attributes['velocities'] = False
form_attributes['box'] = False
form_attributes['time'] = False
form_attributes['structure_id'] = False
form_attributes['forcefield_parameters'] = False
form_attributes['temperature'] = False

def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_molsysmt_MolSys as file_psf_to_molsysmt_MolSys
    from molsysmt import convert



    molsysmt_structures = convert(molecular_system, selection=atom_indices, structure_indices=structure_indices,
            to_form='molsysmt.Structures')

    coordinates = molsysmt_structures.coordinates
    time = molsysmt_structures.time
    box = molsysmt_structures.box
    structure_id = molsysmt_structures.structure_id

    tmp_item = file_psf_to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates,
            time=time, box=box, structure_id=structure_id)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_molsysmt_Topology as file_psf_to_molsysmt_Topology

    tmp_item = file_psf_to_molsysmt_Topology(item, atom_indices=atom_indices)

    return tmp_item

def to_openmm_CharmmPsfFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_openmm_CharmmPsfFile as file_psf_to_openmm_CharmmPsfFile

    tmp_item = file_psf_to_openmm_CharmmPsfFile(item, atom_indices=atom_indices)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_openmm_Topology as file_psf_to_openmm_Topology

    tmp_item = file_psf_to_openmm_Topology(item, atom_indices=atom_indices)

    return tmp_item


