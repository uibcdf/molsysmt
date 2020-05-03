from os.path import basename as _basename

form_name=_basename(__file__).split('.')[0].split('_')[-1]

is_form = {
    'pdb': form_name,
    'PDB': form_name
    }

info=["",""]

info = ["Protein Data Bank file format","https://www.rcsb.org/pdb/static.do?p=file_formats/pdb/index.html"]

def to_molsysmt_MolSys(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.molsys.files import from_pdb as pdb_to_molsysmt_MolSys
    tmp_item = pdb_to_molsysmt_MolSys(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Composition(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.composition.files import from_pdb as pdb_to_molsysmt_Composition
    tmp_item = pdb_to_molsysmt_Composition(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_DataFrame(item, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.dataframe.files import from_pdb as pdb_to_molsysmt_DataFrame
    tmp_item = pdb_to_molsysmt_DataFrame(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_molsysmt_Trajectory(item, topology=None, atom_indices='all', frame_indices='all'):

    from molsysmt.native.io.trajectory.files import from_pdb as pdb_to_molsysmt_Trajectory
    tmp_item = pdb_to_molsysmt_Trajectory(item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_parmed_Structure(item, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed
    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdanalysis_Universe(item, atom_indices='all', frame_indices='all'):

    from MDAnalysis import Universe as mdanalysis_Universe
    from molsysmt.forms.classes.api_mdtraj_Universe import extract as extract_universe
    tmp_item = mdanalysis_Universe(item)
    tmp_item = extract_universe(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Topology(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_topology as mdtraj_load_topology
    from molsysmt.forms.classes.api_mdtraj_Topology import extract as extract_mdtraj_topology
    tmp_item = mdtraj_load_topology(item)
    tmp_item = extract_mdtraj_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices='all', frame_indices='all'):

    from mdtraj import load_pdb as mdtraj_pdb_loader
    from molsysmt.forms.classes.api_mdtraj_Trajectory import extract as extract_mdtraj_trajectory
    tmp_item = mdtraj_pdb_loader(item)
    tmp_item = extract_mdtraj_trajectory(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_PDBTrajectoryFile(item, atom_indices='all', frame_indices='all'):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    return PDBTrajectoryFile(item)

def to_mol2(item, output_file_path=None, atom_indices='all', frame_indices='all'):

    from parmed import load_file as parmed_file_loader
    from molsysmt.forms.classes.api_parmed_Structure import extract as extract_parmed
    tmp_item = parmed_file_loader(item)
    tmp_item = extract_parmed(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item.save(output_file_path)

def to_openmm_Topology(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_Topology import extract as extract_openmm_topology
    tmp_item = PDBFile(item).getTopology()
    tmp_item = extract_openmm_topology(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_Modeller(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from simtk.openmm.app.modeller import Modeller
    from molsysmt.forms.classes.api_openmm_Modeller import extract as extract_modeller
    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    tmp_item = extract_modeller(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_openmm_PDBFile(item, atom_indices='all', frame_indices='all'):

    from simtk.openmm.app.pdbfile import PDBFile
    from molsysmt.forms.classes.api_openmm_PDBFile import extract as extract_pdbfile
    tmp_item = PDBFile(item)
    tmp_item = extract_pdbfile(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices='all', frame_indices='all'):

    from pdbfixer.pdbfixer import PDBFixer
    from molsysmt.forms.classes.api_pdbfixer_PDBFixer import extract as extract_pdbfixer
    tmp_item = PDBFixer(item)
    tmp_item = extract_pdbfixer(tmp_item, atom_indices=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_nglview(item, atom_indices='all', frame_indices='all'):

    from nglview import show_file as _nglview_show_file
    from os import remove
    tmp_file = extract(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item = _nglview_show_file(tmp_file)
    remove(tmp_file)
    return tmp_item

def to_yank_Topography(item, atom_indices='all', frame_indices='all'):

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

def copy(item):

    from shutil import copy
    from molsysmt.utils.pdb import tmp_pdb_filename
    tmp_file = tmp_pdb_filename()
    copy(item,tmp_file)
    return tmp_file

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        from molsysmt.utils.pdb import tmp_pdb_filename
        from molsysmt.forms.classes.api_pdbfixer_PDBFixer import to_pdb as pdbfixer_PDBFixer_to_pdb
        tmp_item = to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, frame_indices=frame_indices)
        tmp_file = tmp_pdb_filename()
        pdbfixer_PDBFixer_to_pdb(tmp_item, output_file_path=tmp_file)
        return tmp_file

###### Get

# System

#def get_frames_from_system (item, indices='all', frame_indices='all'):
#
#    from molsysmt import get
#    tmp_item = to_mdtraj_XTCTrajectoryFile(item)
#    xyz, time, step, box = get(tmp_item, target='system',
#            frame_indices=frame_indices, frames=True)
#    tmp_item.close()
#    del(tmp_item, get)
#    return xyz, time, step, box

def get_n_frames_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    from mdtraj.formats.pdb import PDBTrajectoryFile
    tmp_item = PDBTrajectoryFile(item)
    n_frames = get(tmp_item, target='system',  n_frames=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_frames

def get_n_atoms_from_system (item, indices='all', frame_indices='all'):

    from molsysmt import get
    from mdtraj.formats.pdb import PDBTrajectoryFile
    tmp_item = PDBTrajectoryFile(item)
    n_atoms = get(tmp_item, target='system',  n_atoms=True)
    tmp_item.close()
    del(tmp_item, get)
    return n_atoms

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

