from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from molmodmt import MolMod as _molmodmt_MolMod

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _molmodmt_MolMod : form_name,
    'molmod': form_name,
    'MolMod': form_name,
    'molmodmt.MolMod': form_name
}


def to_aminoacids3_seq(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import convert as _convert
    tmp_item = _convert(item,'mdtraj.Topology')
    tmp_item = _convert(tmp_item,'aminoacids3:seq')
    return tmp_item

def to_aminoacids1(item, selection=None, syntaxis='mdtraj'):
    return to_aminoacids1_seq(item, selection=selection, syntaxis=syntaxis)

def to_aminoacids1_seq(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import convert as _convert
    tmp_item = to_aminoacids3_seq(item)
    tmp_item = _convert('aminoacids3:'+tmp_item,'aminoacids1:seq')
    return tmp_item

def to_biopython_Seq(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_Seq as _aminoacids1_to_biopython_Seq
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_Seq(tmp_item)
    del(_aminoacids1_to_biopython_Seq)
    return tmp_item

def to_biopython_SeqRecord(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.forms.seqs.api_aminoacids1 import to_biopython_SeqRecord as _aminoacids1_to_biopython_SeqRecord
    tmp_item = to_aminoacids1_seq(item)
    tmp_item = _aminoacids1_to_biopython_SeqRecord(tmp_item)
    del(_aminoacids1_to_biopython_SeqRecord)
    return tmp_item

def to_molmodmt(item):
    return item

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import to_mdtraj as _to_mdtraj
    from molmodmt import extract as _extract
    tmp_item = _to_mdtraj(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import to_mdtraj_Trajectory as _to_mdtraj_Trajectory
    from molmodmt import extract as _extract
    tmp_item = _to_mdtraj_Trajectory(item)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj_Topology(item, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import to_mdtraj_Topology as _to_mdtraj_Topology
    tmp_item = _to_mdtraj_Topology(item)
    return tmp_item

def to_pdb(item, filename=None, selection=None, syntaxis='mdtraj'):

    from molmodmt.native.io_molmod import to_pdb as _to_pdb

    return _to_pdb(item, filename=filename, selection=selection, syntaxis=syntaxis)

def select_with_mdtraj(item, selection=None, syntaxis='mdtraj'):
    return item.select_with_mdtraj(selection)

def extract_atom_indices(item, atom_indices):
    return item.extract(atom_indices)

def trim_atom_indices(item, atom_indices):
    pass

def add_atoms(item, atoms):
    pass

def to_nglview(item):

    from .api_mdtraj_Trajectory import to_nglview as _mdtraj_to_nglview

    if type(item) in [list,tuple]:
        tmp_item = []
        for ii in item:
            tmp_item.append(to_mdtraj_Trajectory(ii))
    else:
        tmp_item = to_mdtraj_Trajectory(item)

    return _mdtraj_to_nglview(tmp_item)


