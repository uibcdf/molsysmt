import os
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='molsysmt.H5MSMFileHandler')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures
    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_H5MSMFileHandler(str(str(item)), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    structures_ds = item.file['structures']

    tmp_item = Structures()

    # Coordinates
    coordinates_unit = structures_ds['coordinates'].attrs.get('unit', 'nm')
    
    if is_all(structure_indices):
        if is_all(atom_indices):
            tmp_item.coordinates = puw.quantity(structures_ds['coordinates'][:], coordinates_unit)
        else:
            tmp_item.coordinates = puw.quantity(structures_ds['coordinates'][:, atom_indices, :], coordinates_unit)
    else:
        if is_all(atom_indices):
            tmp_item.coordinates = puw.quantity(structures_ds['coordinates'][structure_indices, :, :], coordinates_unit)
        else:
            tmp_item.coordinates = puw.quantity(structures_ds['coordinates'][np.ix_(structure_indices, atom_indices, [0,1,2])], coordinates_unit)

    # Box
    if 'box' in structures_ds and structures_ds['box'].shape[0] > 0:
        box_unit = structures_ds['box'].attrs.get('unit', 'nm')
        if is_all(structure_indices):
            tmp_item.box = puw.quantity(structures_ds['box'][:], box_unit)
        else:
            tmp_item.box = puw.quantity(structures_ds['box'][structure_indices, :, :], box_unit)
    else:
        tmp_item.box = None

    # B factor
    if 'b_factor' in structures_ds and structures_ds['b_factor'].shape[0] > 0:
        b_factor_unit = structures_ds.attrs.get('b_factor_unit', 'nanometer**2')
        if is_all(structure_indices):
            if is_all(atom_indices):
                tmp_item.b_factor = puw.quantity(structures_ds['b_factor'][:], b_factor_unit)
            else:
                tmp_item.b_factor = puw.quantity(structures_ds['b_factor'][:, atom_indices], b_factor_unit)
        else:
            if is_all(atom_indices):
                tmp_item.b_factor = puw.quantity(structures_ds['b_factor'][structure_indices, :], b_factor_unit)
            else:
                tmp_item.b_factor = puw.quantity(structures_ds['b_factor'][np.ix_(structure_indices, atom_indices)], b_factor_unit)
    else:
        tmp_item.b_factor = None

    # Time
    if 'time' in structures_ds and structures_ds['time'].shape[0] > 0:
        time_unit = structures_ds['time'].attrs.get('unit', 'ps')
        if is_all(structure_indices):
            tmp_item.time = puw.quantity(structures_ds['time'][:], time_unit)
        else:
            tmp_item.time = puw.quantity(structures_ds['time'][structure_indices], time_unit)
    else:
        tmp_item.time = None

    # Step
    if 'step' in structures_ds and structures_ds['step'].shape[0] > 0:
        if is_all(structure_indices):
            tmp_item.step = structures_ds['step'][:]
        else:
            tmp_item.step = structures_ds['step'][structure_indices]
    else:
        tmp_item.step = None

    # Structure ID
    if 'id' in structures_ds and structures_ds['id'].shape[0] > 0:
        if is_all(structure_indices):
            tmp_item.structure_id = structures_ds['id'][:]
        else:
            tmp_item.structure_id = structures_ds['id'][structure_indices]
    else:
        tmp_item.structure_id = None

    if opened_here:
        item.close()

    return tmp_item
