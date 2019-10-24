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
    from molmodmt import extract as _extract
    from parmed import load_file as _parmed_file_loader
    tmp_item = _parmed_file_loader(item)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    del(_parmed_file_loader)
    return tmp_item

def to_mdanalysis_Universe(item, atom_indices=None, frame_indices=None):
    from MDAnalysis import Universe as _mdanalysis_Universe
    return _mdanalysis_Universe(item)

def to_mdtraj_Topology(item, atom_indices=None, frame_indices=None):

    from mdtraj import load_topology as _mdtraj_load_topology
    from molmodmt import extract as _extract

    tmp_item = _mdtraj_load_topology(item)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_Trajectory(item, atom_indices=None, frame_indices=None):

    from mdtraj import load_pdb as _mdtraj_pdb_loader
    from molmodmt import extract as _extract
    tmp_item = _mdtraj_pdb_loader(item)
    tmp_item = _extract(tmp_item, selection=atom_indices, frame_indices=frame_indices)
    return tmp_item

def to_mdtraj_PDBTrajectoryFile(item, atom_indices=None, frame_indices=None):

    from mdtraj.formats.pdb import PDBTrajectoryFile

    return PDBTrajectoryFile(item)

def to_mol2(item, filename=None, atom_indices=None, frame_indices='all'):

    from parmed import load_file as _parmed_file_loader
    tmp_parmed_form = _parmed_file_loader(item)
    tmp_parmed_form.save(filename)
    pass

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):
    from simtk.openmm.app.pdbfile import PDBFile
    tmp_item = PDBFile(item).getTopology()
    return tmp_item

#def to_openmm_Positions(item, selection="all", syntaxis="mdtraj"):
#    from simtk.openmm.app.pdbfile import PDBFile as _openmm_pdb_loader
#    tmp_form = _openmm_pdb_loader(item).getPositions()
#    del(_openmm_pdb_loader)
#    return tmp_form

def to_openmm_Modeller(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app.pdbfile import PDBFile
    from simtk.openmm.app.modeller import Modeller
    tmp_item = PDBFile(item)
    tmp_item = Modeller(tmp_item.topology, tmp_item.positions)
    return tmp_item

def to_openmm_PDBFile(item, atom_indices=None, frame_indices=None):
    from simtk.openmm.app.pdbfile import PDBFile
    tmp_item = PDBFile(item)
    return tmp_item

def to_pdbfixer_PDBFixer(item, atom_indices=None, frame_indices=None):

    from molmodmt import extract
    from pdbfixer.pdbfixer import PDBFixer
    tmp_item = extract(item, selection=atom_indices)
    tmp_item = PDBFixer(tmp_item)
    return tmp_item

def to_nglview(item, atom_indices=None, frame_indices=None):
    from nglview import show_file as _nglview_show_file
    return _nglview_show_file(item)

def to_yank_Topography(item, atom_indices=None, frame_indices=None):

    from molsysmt.forms.classes.api_openmm_Topology import to_yank_Topography as _openmm_to_yank_Topography
    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_to_yank_Topography(tmp_form)
    del(_openmm_to_yank_Topography)
    return tmp_form

def select_with_MDTraj(item, selection):

    from mdtraj import load_topology as _mdtraj_load_topology

    tmp_item = _mdtraj_load_topology(item)
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

    from molmodmt.utils.pdb import tmp_pdb_filename
    from molmodmt.forms.classes.api_pdbfixer_PDBFixer import to_pdb as pdbfixer_PDBFixer_to_pdb
    tmp_item = to_pdbfixer_PDBFixer(item, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_file = tmp_pdb_filename()
    pdbfixer_PDBFixer_to_pdb(tmp_item, output_file_path=tmp_file)
    return tmp_file

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

