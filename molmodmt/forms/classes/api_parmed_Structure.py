from os.path import basename as _basename
from molmodmt.utils.exceptions import *
from parmed.structure import Structure as _parmed_Structure

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _parmed_Structure : form_name
}

## Methods

def to_openmm_Modeller(item, selection=None, syntaxis='mdtraj'):

    from molmodmt import extract as _extract
    from simtk.openmm.app.modeller import Modeller as _openmm_Modeller
    tmp_item = _openm_Modeller(item.topology, item.positions)
    tmp_item = _extract(tmp_item, selection=selection, syntaxis=syntaxis)
    return tmp_item

def to_mdtraj(item, selection=None, syntaxis='mdtraj'):

    return to_mdtraj_Trajectory(item, selection=selection, syntaxis=syntaxis)

def to_mdtraj_Trajectory(item, selection=None, syntaxis='mdtraj'):

    from mdtraj.core.trajectory import Trajectory as mdtraj_trajectory
    from mdtraj.core.topology import Topology as mdtraj_topology
    from molmodel import extract as _extract

    tmp_item = mdtraj_trajectory(item.positions._value,mdtraj_topology.from_openmm(item.topology))

    if selection is not None:
        tmp_item = _extract(tmp_item, selection=selection, syntaxis='mdtraj')

    return tmp_item

def to_nglview(item):

    from nglview import show_parmed as _nglview_show_parmed
    return _nglview_show_parmed(item)

def to_pdb(item, filename):

    return item.save(filename)

def to_mol2(item,output_file):

    return item.save(filename)

def select_with_mdtraj(item, selection):
    tmp_form=to_mdtraj(item)
    tmp_sel=tmp_form.topology.select(selection)
    del(tmp_form)
    return tmp_sel

def select_with_parmed(item, selection):
    from parmed.amber import AmberMask as _AmberMask
    tmp_sel = list(_AmberMask(item,selection).Selected())
    del(_AmberMask)
    return tmp_sel

def extract_atom_indices(item, atom_indices):
    from molmodmt.utils.miscellanea import atom_indices2AmberMask
    from copy import deepcopy
    tmp_item = deepcopy(item)
    tmp_item.strip(atom_indices2AmberMask(atom_indices,len(item.atoms),inverse=True))
    return tmp_item


