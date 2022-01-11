from molsysmt._private_tools.exceptions import *

form_name='molsysmt.MolSys'
form_type='class'
form_info=["",""]
form_components = {
    'elements' : True, # atoms, groups, chains, entities, etc.
    'bonds' : True, # bonds
    'coordinates' : True, # coordinates, steps, time
    'velocities' : False, # velocities
    'box' : True, # box or unit cell
    'ff_parameters' : False, # interatomic interaction parameters or force field
    'mm_parameters' : False, # molecular mechanics parameters to work with the interatomic interactions
    'thermo_state' : False, # thermodinamic state or parameters of the ensemble: T and P.
    'simulation' : False # Other simulation parameters to simulate the behaviour such as integrator, damping, etc.
}

def to_molsysmt_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Topology as molsysmt_MolSys_to_molsysmt_Topology

    tmp_item = molsysmt_MolSys_to_molsysmt_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_molsysmt_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_molsysmt_Trajectory as molsysmt_MolSys_to_molsysmt_Trajectory

    tmp_item = molsysmt_MolSys_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_XYZ(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_XYZ as molsysmt_MolSys_to_XYZ

    tmp_item = molsysmt_MolSys_to_XYZ(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_aminoacids3(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids3 as molsysmt_MolSys_to_string_aminoacids3

    tmp_item = molsysmt_MolSys_to_string_aminoacids3(item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_aminoacids1(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_string_aminoacids1 as molsysmt_MolSys_to_string_aminoacids1

    tmp_item = molsysmt_MolSys_to_string_aminoacids1(item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_biopython_Seq(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_biopython_Seq as molsysmt_MolSys_to_biopython_Seq

    tmp_item = molsysmt_MolSys_to_biopython_Seq(item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_biopython_SeqRecord(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_biopython_SeqRecord as molsysmt_MolSys_to_biopython_SeqRecord

    tmp_item = molsysmt_MolSys_to_biopython_SeqRecord(item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdtraj_Trajectory(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_mdtraj_Trajectory as molsysmt_MolSys_to_mdtraj_Trajectory

    tmp_item = molsysmt_MolSys_to_mdtraj_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_mdtraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_mdtraj_Topology as molsysmt_MolSys_to_mdtraj_Topology

    tmp_item = molsysmt_MolSys_to_mdtraj_Topology(item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Topology as molsysmt_MolSys_to_openmm_Topology

    tmp_item = molsysmt_MolSys_to_openmm_Topology(item, atom_indices=atom_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Modeller(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Modeller as molsysmt_MolSys_to_openmm_Modeller

    tmp_item = molsysmt_MolSys_to_openmm_Modeller(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                                                                   atom_indices=atom_indices,
                                                                   frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_System(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_openmm_System as molsysmt_MolSys_to_openmm_System

    tmp_item = molsysmt_MolSys_to_openmm_System(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                                                                   atom_indices=atom_indices,
                                                                   frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Context(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Context as molsysmt_MolSys_to_openmm_Context

    tmp_item = molsysmt_MolSys_to_openmm_Context(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                                                                   atom_indices=atom_indices,
                                                                   frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_openmm_Simulation(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.tools.molsysmt_MolSys import to_openmm_Simulation as molsysmt_MolSys_to_openmm_Simulation

    tmp_item = molsysmt_MolSys_to_openmm_Simulation(item, atom_indices=atom_indices, frame_indices=frame_indices)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                                                                   atom_indices=atom_indices,
                                                                   frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_file_pdb(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.tools.molsysmt_MolSys import to_file_pdb as molsysmt_MolSys_to_file_pdb

    tmp_item = molsysmt_MolSys_to_file_pdb(item, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                                                                   atom_indices=atom_indices,
                                                                   frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_file_msmpk(item, molecular_system=None, atom_indices='all', frame_indices='all', output_filename=None):

    from molsysmt.tools.molsysmt_MolSys import to_file_msmpk as molsysmt_MolSys_to_file_msmpk

    tmp_item = molsysmt_MolSys_to_file_msmpk(item, atom_indices=atom_indices, frame_indices=frame_indices, output_filename=output_filename)

    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item,
                                                                   atom_indices=atom_indices,
                                                                   frame_indices=frame_indices)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_string_pdb_text(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import to_string_pdb_text as molsysmt_MolSys_to_string_pdb_text

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_string_pdb_text(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_pdbfixer_PDBFixer(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import to_pdbfixer_PDBFixer as molsysmt_MolSys_to_pdbfixer_PDBFixer

    tmp_item, tmp_molecular_system = molsysmt_MolSys_to_pdbfixer_PDBFixer(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

def to_pytraj_Topology(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_molsysmt_Topology import to_pytraj_Topology as molsysmt_Topology_to_pytraj_Topology

    tmp_item, tmp_molecular_system = to_molsysmt_Topology(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = molsysmt_Topology_to_pytraj_Topology(tmp_item, molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

def to_rdkit_Mol(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys import to_rdkit_Mol as molsysmt_MolSys_to_rdkit_Mol

    is_a_ligand = msm.is_composed_of(item, molecular_system=molecular_system, selection=atom_indices, small_molecule=1)

    if is_a_ligand:

        tmp_item, tmp_molecular_system = molsysmt_MolSys_to_rdkit_Mol(item, molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)

    else:

        raise SystemError("The system needs to be composed of a single small molecule")

    return tmp_item, tmp_molecular_system

def to_nglview_NGLWidget(item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from nglview import show_molsysmt

    tmp_item = show_molsysmt(item, selection=atom_indices, frame_indices=frame_indices)
    if molecular_system is not None:
        tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
    else:
        tmp_molecular_system = None

    return tmp_item, tmp_molecular_system

def to_molsysmt_MolSys(item, molecular_system=None, atom_indices='all', frame_indices='all', copy_if_all=True):

    tmp_molecular_system = None

    if (atom_indices is 'all') and (frame_indices is 'all'):
        if copy_if_all:
            tmp_item = extract(item)
            if molecular_system is not None:
                tmp_molecular_system = molecular_system.combine_with_items(tmp_item)
        else:
            tmp_item = item
            if molecular_system is not None:
                tmp_molecular_system = molecular_system
    else:
        tmp_item = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
        if molecular_system is not None:
            tmp_molecular_system = molecular_system.combine_with_items(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)

    return tmp_item, tmp_molecular_system

from molsysmt.tools.molsysmt_MolSys import extract

def add(to_item, item):

    to_item.add(item)
    pass

def merge(item_1, item_2):

    tmp_item = extract(item_1)
    tmp_item.add(item_2)

    return tmp_item

def append_frames(item, step=None, time=None, coordinates=None, box=None):

    item.trajectory.append_frames(step=step, time=time, coordinates=coordinates, box=box)
    pass

def concatenate_frames(item, step=None, time=None, coordinates=None, box=None):

    tmp_item = extract(item)
    tmp_item.append_frames(step=step, time=time, coordinates=coordinates, box=box)

    return tmp_item

###### Get

from molsysmt.tools.molsysmt_MolSys.get import *

###### Set

from molsysmt.tools.molsysmt_MolSys.set import *

