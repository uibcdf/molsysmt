from os.path import basename as _basename
from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_PDBFixer

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _pdbfixer_PDBFixer : form_name
}

def to_nglview(item):

    from nglview import show_mdtraj as _nglview_show_mdtraj
    from molmodmt.formats.engines.api_pdbfixer import to_mdtraj as _pdbfixer_to_mdtraj
    return _nglview_show_mdtraj(_pdbfixer_to_mdtraj(item))

def to_aminoacids3_seq(item):

    return ''.join([ r.name for r in item.topology.residues() ])

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


def to_mdtraj_Topology(item):

    from mdtraj.core.topology import Topology as _mdtraj_Topology
    tmp_form = to_openmm_Topology(item)
    tmp_form = _mdtraj_Topology.from_openmm(tmp_form)
    del(_mdtraj_Topology)
    return tmp_form

def to_mdtraj_Trajectory(item):

    return to_mdtraj(item)

def to_mdtraj(item):

    ## This approach was commented since residue indices are not kept.
    #from mdtraj.core.trajectory import Trajectory as _mdtraj_trajectory
    #from mdtraj.core.topology import Topology as _mdtraj_topology
    #tmp_form = _mdtraj_trajectory(item.positions._value,_mdtraj_topology.from_openmm(item.topology))
    #del(_mdtraj_trajectory,_mdtraj_topology)
    #return tmp_form

    import tempfile as _tempfile
    from os import remove as _remove
    from mdtraj import load_pdb as _load_pdb

    tmp_pdbfilename = _tempfile.NamedTemporaryFile(suffix=".pdb").name
    tmp_system = to_pdb(item,tmp_pdbfilename)
    tmp_item = _load_pdb(tmp_pdbfilename)
    _remove(tmp_pdbfilename)
    del(_load_pdb, tmp_pdbfilename, _tempfile, _remove)
    return tmp_item


def to_modeller(item):

    from simtk.openmm.app import Modeller as _openmm_app_Modeller
    return _openmm_app_Modeller(item.topology, item.positions)

def to_openmm_Topology(item):

    return item.topology

def to_openmm_Positions(item):

    return item.positions

def to_yank_Topography(item):

    from yank import Topography as _yank_Topography
    tmp_form = to_openmm_Topology(item)
    tmp_form = _yank_Topography(tmp_form)
    del(_yank_Topography)
    return tmp_form

def to_parmed_Structure(item):

    from .api_openmm_Topology import to_parmed_Structure as _openmm_Topology_to_parmed_Structure
    tmp_form = to_openmm_Topology(item)
    tmp_form = _openmm_Topology_to_parmed_Structure(tmp_form)
    del(_openmm_Topology_to_parmed_Structure)
    return tmp_form

def to_pdb(item,output_file):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    return _openmm_app_PDBFILE.writeFile(item.topology, item.positions, open(output_file, 'w'),keepIds=True)

def select_with_mdtraj(item, selection):

    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def extract_atoms_list(item, atoms_list):

    from .api_mdtraj_Trajectory import extract_atoms_list as _mdtraj_extract_atoms_list
    from .api_mdtraj_Trajectory import to_pdbfixer as _mdtraj_to_pdbfixer

    tmp_form=to_mdtraj(item)
    tmp_extraction_mdtraj=_mdtraj_extract_atoms_list(tmp_form, atoms_list)
    tmp_extraction = _mdtraj_to_pdbfixer(tmp_extraction_mdtraj)
    del(tmp_form,tmp_extraction_mdtraj,_mdtraj_extract_atoms_list,_mdtraj_to_pdbfixer)
    return tmp_extraction

