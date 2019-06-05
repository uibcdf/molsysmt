from os.path import basename as _basename
from pdbfixer.pdbfixer import PDBFixer as _pdbfixer_PDBFixer

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _pdbfixer_PDBFixer : form_name
}

## Methods

from .get.api_get_pdbfixer_PDBFixer import getting
from .set.api_set_pdbfixer_PDBFixer import setting

def get_total_n_atoms(item):
    return item.topology.getNumAtoms()

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview
    tmp_item = to_mdtraj(item)
    return _mdtraj_to_nglview(tmp_item)

def to_aminoacids3_seq(item):

    return ''.join([ r.name for r in item.topology.residues() ])

def to_aminoacids1_seq(item):

    from molmodmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as _aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _aminoacids3_to_aminoacids1(tmp_item)
    del(_aminoacids3_to_aminoacids1)
    return tmp_item

def to_biopython_Seq(item):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_Seq as _aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_Seq(tmp_item)
    del(_aminoacids1_to_biopython_Seq)
    return tmp_item

def to_biopython_SeqRecord(item):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_SeqRecord as _aminoacids1_to_biopython_SeqRecord
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

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    import simtk.unit as _unit
    from molmodmt import extract as _extract
    from .api_openmm_Topology import to_mdtraj_Topology as _openmm_Topology_to_mdtraj_Topology
    from mdtraj.core.trajectory import Trajectory as _mdtraj_Trajectory

    tmp_item_topol = _openmm_Topology_to_mdtraj_Topology(item.topology)
    tmp_item = _mdtraj_Trajectory(item.positions/_unit.nanometers, tmp_item_topol)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_openmm_Modeller(item, selection=None, syntaxis='mdtraj'):

    from simtk.openmm.app import Modeller as _openmm_app_Modeller
    return _openmm_app_Modeller(item.topology, item.positions)

def to_openmm_Topology(item, selection=None, syntaxis='mdtraj'):

    return item.topology

def to_openmm_Positions(item, selection=None, syntaxis='mdtraj'):

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

def to_pdbfixer(item, selection=None, syntaxis="mdtraj"):
    return item

def to_pdb(item, filename=None, selection=None, syntaxis="mdtraj"):

    from simtk.openmm.app import PDBFile as _openmm_app_PDBFILE
    return _openmm_app_PDBFILE.writeFile(item.topology, item.positions, open(filename, 'w'), keepIds=True)

def select_with_mdtraj(item, selection):

    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def extract_atom_indices(item, atom_indices):

    from molmodmt import convert, extract
    tmp_item = convert(item, 'openmm.Modeller')
    tmp_item = extract(tmp_item, atom_indices)
    tmp_item = convert(tmp_item, 'pdbfixer.PDBFixer')
    return tmp_item

def trim_atom_indices(item, atom_indices):

    from molmodmt import convert, trim
    tmp_item = convert(item, 'openmm.Modeller')
    tmp_item = trim(tmp_item, atom_indices)
    tmp_item = convert(tmp_item, 'pdbfixer.PDBFixer')
    return tmp_item

def duplicate(item):

    from os import remove
    from molmodmt import convert
    from molmodmt.utils.pdb import tmp_pdb_filename
    tmp_file = tmp_pdb_filename()
    convert(item, tmp_file)
    tmp_item = convert(tmp_file,'pdbfixer.PDBFixer')
    remove(tmp_file)
    return tmp_item

