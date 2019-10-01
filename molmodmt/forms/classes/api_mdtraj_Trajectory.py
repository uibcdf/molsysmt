from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name,
    'mdtraj.Trajectory':form_name
    }

def to_aminoacids3_seq(item, atom_indices=None, frame_indices=None):

    return ''.join([ r.name for r in item.topology.residues ])

def to_aminoacids1_seq(item, atom_indices=None, frame_indices=None):

    from molmodmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as _aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _aminoacids3_to_aminoacids1(tmp_item)
    del(_aminoacids3_to_aminoacids1)
    return tmp_item

def to_biopython_Seq(item, atom_indices=None, frame_indices=None):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_Seq as _aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_Seq(tmp_item)
    del(_aminoacids1_to_biopython_Seq)
    return tmp_item

def to_biopython_SeqRecord(item, atom_indices=None, frame_indices=None):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_SeqRecord as _aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_SeqRecord(tmp_item)
    del(_aminoacids1_to_biopython_SeqRecord)
    return tmp_item

def to_molmodmt_MolMod(item, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_molmod import from_mdtraj_Trajectory as _molmodmt_MolMod_from_mdtraj_Trajectory
    tmp_item = _molmodmt_MolMod_from_mdtraj_Trajectory(item, atom_indices=atom_indices)
    return tmp_item

def to_molmodmt_Trajectory(item, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_trajectory import from_mdtraj_Trajectory as _molmodmt_Trajectory_from_mdtraj_Trajectory
    tmp_item = _molmodmt_Trajectory_from_mdtraj_Trajectory(item, atom_indices=atom_indices)
    return tmp_item

def to_molmodmt_Topology(item, atom_indices=None, frame_indices=None):

    from molmodmt.native.io_topology import from_mdtraj_Topology as _molmodmt_Topology_from_mdtraj_Trajectory
    tmp_item = _molmodmt_Topology_from_mdtraj_Trajectory(item, atom_indices=atom_indices)
    return tmp_item

def to_molmodmt(item, atom_indices=None, frame_indices=None):

    return to_molmodmt_MolMod(item, atom_indices=atom_indices)

def to_mdtraj_Topology(item, atom_indices=None, frame_indices=None):

    return item.topology

def to_openmm_Topology(item, atom_indices=None, frame_indices=None):

    from .api_mdtraj_Topology import to_openmm_Topology as _mdtraj_Topology_to_openmm_Topology

    tmp_form = to_mdtraj_Topology(item)
    tmp_form = _mdtraj_Topology_to_openmm_Topology(tmp_form)
    del(_mdtraj_Topology_to_openmm_Topology)
    return tmp_form

def to_openmm_Modeller(item, atom_indices=None, frame_indices=None):

    from simtk.openmm.app import Modeller as _Modeller
    from molmodmt import reformat as _reformat

    topology = to_openmm_Topology(item)
    positions = getting(item, coordinates=True)
    positions = _reformat(attribute='coordinates', value=positions, is_format='mdtraj.Trajectory',
                         to_format='openmm')
    tmp_item = _Modeller(topology, positions)
    return tmp_item

def to_yank_Topography(item, atom_indices=None, frame_indices=None):

    from .api_openmm_Topology import to_yank_Topography as _openmm_Topology_to_yank_Topography

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_yank_Topography(tmp_form)
    del(_openmm_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item, atom_indices=None, frame_indices=None):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_parmed_Structure(tmp_form)
    del(_openmm_Topology_to_parmed_Structure)
    return tmp_form

def to_mdtraj_Topology(item, atom_indices=None, frame_indices=None):

    return item.topology

def to_pdbfixer_PDBFixer(item, atom_indices=None, frame_indices=None):

    from molmodmt.forms.files.api_pdb import to_pdbfixer as _pdb_to_pdbfixer
    import tempfile as _tempfile
    from os import remove as _remove

    tmp_pdbfilename = _tempfile.NamedTemporaryFile(suffix=".pdb").name
    tmp_system = to_pdb(item,tmp_pdbfilename)
    tmp_item = _pdb_to_pdbfixer(tmp_pdbfilename)
    _remove(tmp_pdbfilename)
    del(_pdb_to_pdbfixer, tmp_pdbfilename, _tempfile, _remove)
    return tmp_item

def to_pdb(item, filename=None, atom_indices=None, frame_indices=None):

    from molmodmt import extract as _extract

    if selection is not None:
        tmp_item = _extract(item, selection=atom_indices, frame_indices=frame_indices)
    else:
        tmp_item = item

    if frame_indices is not None:
        return item.slice(frame_indices).save_pdb(filename)
    else:
        return item.save_pdb(filename)


def to_xtc(item, filename=None, atom_indices=None, frame_indices=None):

    return item.save_xtc(filename)

def to_nglview(item, atom_indices=None, frame_indices=None):

    from nglview import show_mdtraj as _show_mdtraj

    tmp_view = _show_mdtraj(item)
    tmp_view.clear()
    tmp_view.add_representation('licorice',selection=atom_indices)
    return tmp_view

def select_with_MDTraj(item, selection):

    return item.topology.select(selection)

def extract_subsystem(item, atom_indices=None, frame_indices=None):

    return item.atom_slice(atom_indices)

def merge_two_items(item1, item2):

    tmp_item = item1.stack(item2)
    return tmp_item


### Get

## atom

def get_masses_from_atom(item, indices=None, frame_indices=None):

    return [atom.element.mass for atom in tmp_item.topology.atoms]

## residue

## system

def get_n_atoms_from_system(item, indices=None, frame_indices=None):

    return item.n_atoms

def get_n_residues_from_system(item, indices=None, frame_indices=None):

    return item.n_residues

def get_n_molecules_from_system(item, indices=None, frame_indices=None):

    return len(get_molecules_from_system(item))

def get_n_frames_from_system(item, indices=None, frame_indices=None):

    return item.n_frames

def get_coordinates_from_system(item, indices=None, frame_indices=None):

    return item.xyz

def get_bonded_atoms_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_bonded_atoms_from_system as _get
    return _get(item, indices=indices, frame_indices=frame_indices)

def get_bonds_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_bonds_from_system as _get
    return _get(item, indices=indices, frame_indices=frame_indices)

def get_graph_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_graph_from_system as _get
    return _get(item, indices=indices, frame_indices=frame_indices)

def get_molecules_from_system(item, indices=None, frame_indices=None):

    from .api_mdtraj_Topology import get_molecules_from_system as _get
    return _get(item, indices=indices, frame_indices=frame_indices)

