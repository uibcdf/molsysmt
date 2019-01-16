from os.path import basename as _basename
from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Trajectory:form_name
    }

def to_aminoacids3_seq(item):

    return ''.join([ r.name for r in item.topology.residues ])

def to_aminoacids1_seq(item):

    from molmodmt.formats.seqs.api_aminoacids3 import to_aminoacids1_seq as _aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _aminoacids3_to_aminoacids1(tmp_item)
    del(_aminoacids3_to_aminoacids1)
    return tmp_item

def to_biopython_Seq(item):

    from molmodmt.formats.seqs.api_aminoacids1 import to_biopython_Seq as _aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_Seq(tmp_item)
    del(_aminoacids1_to_biopython_Seq)
    return tmp_item

def to_biopython_SeqRecord(item):

    from molmodmt.formats.seqs.api_aminoacids1 import to_biopython_SeqRecord as _aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_SeqRecord(tmp_item)
    del(_aminoacids1_to_biopython_SeqRecord)
    return tmp_item

def to_native_Native(item):

    from molsysmt.native import Native as _Native
    tmp_form = _Native(item)
    del(_Native)
    return tmp_form

def to_mdtraj_Topology(item):

    return item.topology

def to_openmm_Topology(item):

    from .api_mdtraj_Topology import to_openmm_Topology as _mdtraj_Topology_to_openmm_Topology

    tmp_form = to_mdtraj_Topology(item)
    tmp_form = _mdtraj_Topology_to_openmm_Topology(tmp_form)
    del(_mdtraj_Topology_to_openmm_Topology)
    return tmp_form

def to_openmm_Positions(item):

    from simtk import unit as _units
    return item.xyz*_units.nanometers

def to_yank_Topography(item):

    from .api_openmm_Topology import to_yank_Topography as _openmm_Topology_to_yank_Topography

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_yank_Topography(tmp_form)
    del(_openmm_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure

    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_parmed_Structure(tmp_form)
    del(_openmm_Topology_to_parmed_Structure)
    return tmp_form

def to_mdtraj_Topology(item):

    return item.topology

def to_openmm_Topology(item):

    from .api_mdtraj_Topology import to_openmm_Topology as _mdtraj_to_openmm_Topology
    tmp_item = _mdtraj_to_openmm_Topology(to_mdtraj_Topology(item))
    del(_mdtraj_to_openmm_Topology)
    return tmp_item

def to_pdbfixer_PDBFixer(item):

    from molmodmt.formats.files.api_pdb import to_pdbfixer as _pdb_to_pdbfixer
    import tempfile as _tempfile
    from os import remove as _remove

    tmp_pdbfilename = _tempfile.NamedTemporaryFile(suffix=".pdb").name
    to_pdb(item,tmp_pdbfilename)
    tmp_item = _pdb_to_pdbfixer(tmp_pdbfilename)
    _remove(tmp_pdbfilename)
    del(_pdb_to_pdbfixer, tmp_pdbfilename, _tempfile, _remove)
    return tmp_item

def to_pdbfixer(item):

    return to_pdbfixer_PDBFixer(item)

def to_parmed(item):

    return to_parmed_Structure(item)

def to_pdb(item,output_file):

    return item.save(output_file)

def to_nglview(item):

    from nglview import show_mdtraj as _show_mdtraj
    tmp_view = _show_mdtraj(item)
    return tmp_view

def get_shape(item):

    return item.n_frames, item.n_atoms

def select_with_mdtraj(item, selection):

    return item.topology.select(selection)

def extract_atoms_list(item, atoms_list):

    return item.atom_slice(atoms_list)
