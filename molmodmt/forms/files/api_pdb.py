from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'pdb': form_name,
    'PDB': form_name
    }

def to_molmodmt_MolMod(item, topology=None, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_molmod import from_pdb as _from_pdb
    return _from_pdb(item, topology=topology, atom_indices=atom_indices, frame_indices=frame_indices)

def to_molmodmt_Topology(item, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_topology import from_pdb as _from_pdb
    return _from_pdb(item, atom_indices=atom_indices)

def to_molmodmt_Trajectory(item, topology=None, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_trajectory import from_pdb as _from_pdb
    return _from_pdb(item, atom_indices=atom_indices, frame_indices=frame_indices)

def to_parmed_Structure(item, atom_indices=None, frame_indices=None):

    from parmed import load_file as parmed_file_loader
    from molmodmt.forms.classes.api_parmed_Structure import extract_subsystem as extract_parmed
    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_Universe(item, atom_indices=None, frame_indices=None):

    from MDAnalysis import Universe as mdanalysis_Universe
    from molmodmt.forms.classes.api_mdtraj_Universe import extract_subsystem as extract_universe
    tmp_item = mdanalysis_Universe(item)
    tmp_item = extract_universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices=None, frame_indices=None):

    from mdtraj import load_topology as mdtraj_load_topology
    from molmodmt.forms.classes.api_mdtraj_Topology import extract_subsystem as extract_mdtraj_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_item = extract_mdtraj_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices=None, frame_indices=None):

    from mdtraj import load_pdb as mdtraj_pdb_loader
    from molmodmt.forms.classes.api_mdtraj_Trajectory import extract_subsystem as extract_mdtraj_trajectory
    tmp_item = mdtraj_pdb_loader(item)
    tmp_item = extract_mdtraj_trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_PDBTrajectoryFile(item, atom_indices=None, frame_indices=None):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    return PDBTrajectoryFile(item)

def to_mol2(item, output_file_path=None, atom_indices=None, frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molmodmt.forms.classes.api_parmed_Structure import extract_subsystem as extract_parmed
    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item.save(output_file_path)

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app.pdbfile import PDBFile
    from molmodmt.forms.classes.api_openmm_Topology import extract_subsystem as extract_openmm_topology
    tmp_item = PDBFile(item).getTopology()
    tmp_item = extract_openmm_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Modeller(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app.pdbfile import PDBFile
    from simtk.openmm.app.modeller import Modeller
    from molmodmt.forms.classes.api_openmm_Modeller import extract_subsystem as extract_modeller
    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    tmp_item = extract_modeller(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_PDBFile(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app.pdbfile import PDBFile
    from molmodmt.forms.classes.api_openmm_PDBFile import extract_subsystem as extract_pdbfile
    tmp_item = PDBFile(item)
    tmp_item = extract_pdbfile(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices=None, frame_indices=None):

    from pdbfixer.pdbfixer import PDBFixer
    from molmodmt.forms.classes.api_openmm_PDBFixer import extract_subsystem as extract_pdbfixer
    tmp_item = PDBFixer(tmp_item)
    tmp_item = extract_pdbfixer(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_nglview(item, atom_indices=None, frame_indices=None):

    from nglview import show_file as _nglview_show_file
    from os import remove
    tmp_file = extract_subsystem(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _nglview_show_file(tmp_file)
    remove(tmp_file)
    return tmp_item

def to_yank_Topography(item, atom_indices=None, frame_indices=None):

    from molsysmt.forms.classes.api_openmm_Topology import to_yank_Topography as openmm_to_yank_Topography
    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = openmm_to_yank_Topography(tmp_item)
    return tmp_item

def select_with_MDTraj(item, selection):

    from mdtraj import load_topology as _dtraj_load_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_sel = tmp_item.select(selection)
    del(tmp_item)
    return tmp_sel

def duplicate(item):

    from shutil import copy
    from molmodmt.utils.pdb import tmp_pdb_filename
    tmp_file = tmp_pdb_filename()
    copy(item,tmp_file)
    return tmp_file

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    if (atom_indices is None) and (frame_indices is None):
        return item
    else:
        from molmodmt.utils.pdb import tmp_pdb_filename
        from molmodmt.forms.classes.api_pdbfixer_PDBFixer import to_pdb as pdbfixer_PDBFixer_to_pdb
        tmp_item = to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_file = tmp_pdb_filename()
        pdbfixer_PDBFixer_to_pdb(tmp_item, output_file_path=tmp_file)
        return tmp_file

###### Get

# System

#def get_frames_from_system (item, indices=None, frame_indices=None):
#
#    from molmodmt import get
#    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
#    xyz, time, step, box = get(tmp_item, target='system',
#            frame_indices=frame_indices, frames=True)
#    tmp_item.close()
#    del(tmp_item, get)
#    return xyz, time, step, box

def get_n_frames_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    from mdtraj.formats.pdb import PDBTrajectoryFile
    tmp_item = PDBTrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices=None, frame_indices=None):

    from molmodmt import get
    from mdtraj.formats.pdb import PDBTrajectoryFile
    tmp_item = PDBTrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

def get_form_from_system(item, indices=None, frame_indices=None):

    from molmodmt import get_form
    return get_form(item)

