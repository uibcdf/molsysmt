from molmodmt.utils.exceptions import *
from os.path import basename as _basename
from mdtraj.core.topology import Topology as _mdtraj_Topology

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdtraj_Topology : form_name,
    'mdtraj.Topology': form_name
}

def to_aminoacids3_seq(item, selection=None, syntaxis='mdtraj'):

    return ''.join([ r.name for r in item.residues ])

def to_aminoacids1_seq(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.forms.seqs.api_aminoacids3 import to_aminoacids1_seq as _aminoacids3_to_aminoacids1
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _aminoacids3_to_aminoacids1(tmp_item)
    del(_aminoacids3_to_aminoacids1)
    return tmp_item

def to_openmm_Topology(item, selection=None, syntaxis='mdtraj'):

    return item.to_openmm()

def to_yank_Topography(item, selection=None, syntaxis='mdtraj'):

    from .api_openmm_Topology import to_yank_Topography as _opennn_Topology_to_yank_Topography
    tmp_form = to_openmm_Topology(item)
    tmp_form = _opennn_Topology_to_yank_Topography(tmp_form)
    del(_opennn_Topology_to_yank_Topography)
    return tmp_form

def to_parmed_Structure(item, selection=None, syntaxis='mdtraj'):

    from .api_openmm_Topology import to_parmed_Structure as _opennn_Topology_to_parmed_Structure
    tmp_form = to_openmm_Topology(item)
    tmp_form = _opennn_Topology_to_parmed_Structure(tmp_form)
    del(_opennn_Topology_to_parmed_Structure)
    return tmp_form

def to_parmed_GromacsTopologyFile(item):
    from parmed.gromacs import GromacsTopologyFile as _GromacsTopologyFile
    tmp_form = to_parmed_Structure(item)
    return _GromacsTopologyFile.from_structure(item)

def to_top(item,filename):
    from .api_parmed_GromacsTopologyFile import to_top as _to_top
    tmp_form = to_parmed_GromacsTopologyFile(item)
    return _to_top(tmp_form,filename)

def select_with_mdtraj(item, selection):
    return item.select(selection)

def extract_atom_indices(item, atoms_selection):
    return item.subset(atoms_selection)

def merge_two_items(item1, item2, in_place=False):

    if in_place:
        item1.join(item2)
        pass
    else:
        tmp_item=item1.copy()
        return tmp_item.join(item2)


