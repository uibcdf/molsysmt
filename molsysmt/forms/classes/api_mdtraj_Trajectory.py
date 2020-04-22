from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name,
    'mdtraj.Trajectory':form_name
    }

info=["",""]

def to_aminoacids3_seq(item, atom_indices='all', frame_indices='all'):

    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)

    return ''.join([ r.name for r in tmp_item.groups ])

def to_aminoacids1_seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids3_to_aminoacids1(tmp_item)
    return tmp_item

def to_biopython_Seq(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1 import to_biopython_Seq as aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_Seq(tmp_item)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.seqs.api_aminoacids1 import to_biopython_SeqRecord as aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = aminoacids1_to_biopython_SeqRecord(tmp_item)
    return tmp_item

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmt_MolSys
    tmp_item = mdtraj_Trajectory_to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmtDataFrame
    tmp_item = mdtraj_Trajectory_to_molsysmt_DataFrame(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmt_Composition
    tmp_item = mdtraj_Trajectory_to_molsysmt_Composition(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.composition.classes import from_mdtraj_Trajectory as mdtraj_Trajectory_to_molsysmt_Composition
    tmp_item = mdtraj_Trajectory_to_molsysmt_Composition(item, atom_indices=atom_indices)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import extract_subsystem as extract_mdtraj_Topology
    tmp_item=item.topology
    tmp_item=extract_mdtraj_Topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import to_openmm_Topology as mdtraj_Topology_to_openmm_Topology
    tmp_item = to_mdtraj_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = mdtraj_Topology_to_openmm_Topology(tmp_item)
    return tmp_item

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app import Modeller
    from simtk.unit import nanometers
    topology = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    positions = get_coordinates_from_atom(item, indices=atom_indices, frame_indices=frame_indices)
    positions = positions*nanometers
    tmp_item = Modeller(topology, positions)
    del(topology, positions)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_yank_Topography as openmm_Topology_to_yank_Topography

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_yank_Topography(tmp_item)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from .api_openmm_Topology import to_parmed_Structure as openmm_Topology_to_parmed_Structure

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_Topology_to_parmed_Structure(tmp_item)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.files.api_pdb import to_pdbfixer_PDBFixer as pdb_to_pdbfixer_PDBFixer
    from molsysmt.utils.pdb import tmp_pdb_filename
    from os import remove as remove

    tmp_file = tmp_pdb_filename()
    to_pdb(item, output_file_path=tmp_file, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = pdb_to_pdbfixer_PDBFixer(tmp_item)
    remove(tmp_file)
    return tmp_item

def to_pdb(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item.save_pdb(output_file_path)

def to_xtc(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return item.save_xtc(output_file_path)

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from nglview import show_mdtraj as show_mdtraj
    from molsysmt.utils.nglview import standardize_view
    tmp_item = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_view = show_mdtraj(tmp_item)
    tmp_view = standardize_view(tmp_view)
    return tmp_view

def select_with_MDTraj(item, selection):

    return item.topology.select(selection)

def select_with_MolSysMT(item, selection):

    from .api_mdtraj_Topology import select_with_Pandas as topology_select_with_Pandas

    return topology_select_with_Pandas(item.topology, selection)

def extract_subsystem(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        tmp_item = item.atom_slice(atom_indices)
        tmp_item = tmp_item.slice(frame_indices)
        return tmp_item

def duplicate(item):

    from copy import deepcopy

    return deepcopy(item)

def merge_two_items(item1, item2):

    tmp_item = item1.stack(item2)
    return tmp_item


### Get

## atom

def get_masses_from_atom(item, indices='all', frame_indices='all'):

    return [atom.element.mass for atom in tmp_item.topology.atoms]

def get_coordinates_from_atom(item, indices='all', frame_indices='all'):

    tmp_item=item.xyz
    if frame_indices is not 'all':
        tmp_item=item_item[frame_indices,:,:]
    if indices is not 'all':
        tmp_item=tmp_item[:,indices,:]
    return tmp_item

## group

## system

def get_n_atoms_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_n_atoms_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_groups_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_n_groups_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_chains_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_n_chains_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_molecules_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_n_molecules_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_waters_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_n_waters_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_ions_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_n_ions_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_n_frames_from_system(item, indices='all', frame_indices='all'):

    return item.n_frames

def get_coordinates_from_system(item, indices='all', frame_indices='all'):

    return item.xyz

def get_bonded_atoms_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_bonded_atoms_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_bonds_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_bonds_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_graph_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_graph_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_molecules_from_system(item, indices='all', frame_indices='all'):

    from .api_mdtraj_Topology import get_molecules_from_system as get
    return get(item.topology, indices=indices, frame_indices=frame_indices)

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

