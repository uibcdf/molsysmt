from molsysmt._private_tools.exceptions import *

from molsysmt.tools.molsysmt_MolSys.extract import extract
from molsysmt.tools.molsysmt_MolSys.add import add
from molsysmt.tools.molsysmt_MolSys.merge import merge
from molsysmt.tools.molsysmt_MolSys.append_frames import append_frames
from molsysmt.tools.molsysmt_MolSys.concatenate_frames import concatenate_frames
from molsysmt.tools.molsysmt_MolSys.get import *
from molsysmt.tools.molsysmt_MolSys.set import *

form_name='molsysmt.MolSys'
form_type='class'
form_info=["",""]

form_elements = {
    'atoms' : True,
    'bonds' : True,
    'groups' : True,
    'component' : True,
    'molecule' : True,
    'chain' : True,
    'entity' : True,
        }

form_attributes = {

    'atom_id' : True,
    'atom_name' : True,
    'atom_type' : True,

    'bond_id' : False,
    'bond_name' : False,
    'bond_type' : False,

    'group_id' : True,
    'group_name' : True,
    'group_type' : True,

    'component_id' : True,
    'component_name' : True,
    'component_type' : True,

    'molecule_id' : True,
    'molecule_name' : True,
    'molecule_type' : True,

    'chain_id' : True,
    'chain_name' : True,
    'chain_type' : True,

    'entity_id' : True,
    'entity_name' : True,
    'entity_type' : True,

    'coordinates' : True,
    'velocities' : False,
    'box' : True,
    'time' : True,
    'step' : True,

    'forcefield' : False,
    'temperature' : False,
    'pressure' : False,
    'integrator' : False,
    'damping' : False,
}



def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices)

    return tmp_item

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Trajectory as molsysmt_MolSys_to_molsysmt_Trajectory

    tmp_item = molsysmt_MolSys_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

def to_XYZ(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_XYZ as molsysmt_MolSys_to_XYZ

    tmp_item = molsysmt_MolSys_to_XYZ(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item

#def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids3 as molsysmt_MolSys_to_string_aminoacids3
#
#    tmp_item = molsysmt_MolSys_to_string_aminoacids3(item, atom_indices=atom_indices)
#
#    return tmp_item

#def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1
#
#    tmp_item = molsysmt_MolSys_to_string_aminoacids1(item, atom_indices=atom_indices)
#
#    return tmp_item

#def to_biopython_Seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_biopython_Seq as molsysmt_MolSys_to_biopython_Seq
#
#    tmp_item = molsysmt_MolSys_to_biopython_Seq(item, atom_indices=atom_indices)
#
#    return tmp_item

#def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_biopython_SeqRecord as molsysmt_MolSys_to_biopython_SeqRecord
#
#    tmp_item = molsysmt_MolSys_to_biopython_SeqRecord(item, atom_indices=atom_indices)
#
#    return tmp_item

#def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory
#
#    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

#def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology
#
#    tmp_item = molsysmt_MolSys_to_mdtraj_Topology(item, atom_indices=atom_indices)
#
#    return tmp_item

#def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology
#
#    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices)
#
#    return tmp_item

#def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller
#
#    tmp_item = molsysmt_MolSys_to_openmm_Modeller(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

#def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_openmm_System as molsysmt_MolSys_to_openmm_System
#
#    tmp_item = molsysmt_MolSys_to_openmm_System(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

#def to_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_openmm_Context as molsysmt_MolSys_to_openmm_Context
#
#    tmp_item = molsysmt_MolSys_to_openmm_Context(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

#def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_openmm_Simulation as molsysmt_MolSys_to_openmm_Simulation
#
#    tmp_item = molsysmt_MolSys_to_openmm_Simulation(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

#def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):
#
#    from molsysmt.tools.molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb
#
#    tmp_item = molsysmt_MolSys_to_file_pdb(item, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)
#
#    return tmp_item

#def to_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):
#
#    from molsysmt.tools.molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk
#
#    tmp_item = molsysmt_MolSys_to_file_msmpk(item, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)
#
#    return tmp_item

#def to_string_pdb_text(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.tools.molsysmt_MolSys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text
#
#    tmp_item = molsysmt_MolSys_to_string_pdb_text(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

#def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.native.io.molsys import to_pdbfixer_PDBFixer as molsysmt_MolSys_to_pdbfixer_PDBFixer
#
#    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item, tmp_molecular_system

#def to_pytraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.forms.api_molsysmt_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology
#
#    tmp_item = to_molsysmt_Topology(item, atom_indices=atom_indices)
#    tmp_item = molsysmt_Topology_to_pytraj_Topology(tmp_item)
#
#    return tmp_item, tmp_molecular_system

#def to_rdkit_Mol(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from molsysmt.native.io.molsys import to_rdkit_Mol as molsysmt_MolSys_to_rdkit_Mol
#
#    is_a_ligand = msm.is_composed_of(item, molecular_system=molecular_system, selection=atom_indices, small_molecule=1)
#
#    if is_a_ligand:
#
#        tmp_item, tmp_molecular_system = molsysmt_MolSys_to_rdkit_Mol(item, atom_indices=atom_indices, frame_indices=frame_indices)
#
#    else:
#
#        raise SystemError("The system needs to be composed of a single small molecule")
#
#    return tmp_item, tmp_molecular_system

#def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):
#
#    from nglview import show_molsysmt
#
#    tmp_item = show_molsysmt(item, selection=atom_indices, frame_indices=frame_indices)
#
#    return tmp_item

