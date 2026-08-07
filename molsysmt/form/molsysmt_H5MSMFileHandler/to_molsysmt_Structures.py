import os
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np


def _read_structure_rows(dataset, structure_indices):
    """Reading structure rows while preserving order and repeated indices."""

    if is_all(structure_indices):
        return dataset[:]
    return np.asarray([dataset[int(index)] for index in structure_indices])


def _dataset_unit(dataset, file, root_attribute, fallback):
    """Returning a dataset unit with a root-level compatibility fallback."""

    return dataset.attrs.get(
        'unit',
        file.attrs.get(root_attribute, fallback),
    )


def _requested_structure_indices(structures, structure_indices):
    """Returning logical structure indices for compressed structural series."""

    if is_all(structure_indices):
        n_structures = int(structures.attrs.get(
            'n_structures_written',
            structures['coordinates'].shape[0],
        ))
        return np.arange(n_structures, dtype=np.int64)
    return np.asarray(structure_indices, dtype=np.int64)


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
    coordinates_ds = structures_ds['coordinates']
    coordinates_unit = _dataset_unit(
        coordinates_ds, item.file, 'length_unit', 'nm'
    )
    coordinates = _read_structure_rows(coordinates_ds, structure_indices)
    if not is_all(atom_indices):
        coordinates = coordinates[:, atom_indices, :]
    tmp_item.coordinates = puw.quantity(
        coordinates.astype(np.float64), coordinates_unit
    )

    # Velocities
    velocities_ds = structures_ds.get('velocities')
    if velocities_ds is not None and velocities_ds.shape[0] > 0:
        velocities_unit = _dataset_unit(
            velocities_ds, item.file, 'velocity_unit',
            (
                f"{item.file.attrs.get('length_unit', 'nm')}/"
                f"{item.file.attrs.get('time_unit', 'ps')}"
            ),
        )
        velocities = _read_structure_rows(velocities_ds, structure_indices)
        if not is_all(atom_indices):
            velocities = velocities[:, atom_indices, :]
        tmp_item.velocities = puw.quantity(
            velocities.astype(np.float64), velocities_unit
        )
    else:
        tmp_item.velocities = None

    # Box
    if 'box' in structures_ds and structures_ds['box'].shape[0] > 0:
        box_ds = structures_ds['box']
        box_unit = _dataset_unit(box_ds, item.file, 'length_unit', 'nm')
        if structures_ds.attrs.get('constant_box', False):
            requested_indices = _requested_structure_indices(
                structures_ds, structure_indices
            )
            box = np.repeat(
                box_ds[0][np.newaxis, :, :],
                len(requested_indices),
                axis=0,
            )
        else:
            box = _read_structure_rows(box_ds, structure_indices)
        tmp_item.box = puw.quantity(box.astype(np.float64), box_unit)
    else:
        tmp_item.box = None

    # B factor
    if 'b_factor' in structures_ds and structures_ds['b_factor'].shape[0] > 0:
        b_factor_unit = structures_ds.attrs.get('b_factor_unit', 'nanometer**2')
        b_factor = _read_structure_rows(
            structures_ds['b_factor'], structure_indices
        )
        if not is_all(atom_indices):
            b_factor = b_factor[:, atom_indices]
        tmp_item.b_factor = puw.quantity(
            b_factor.astype(np.float64), b_factor_unit
        )
    else:
        tmp_item.b_factor = None

    # Time
    if 'time' in structures_ds and structures_ds['time'].shape[0] > 0:
        time_ds = structures_ds['time']
        time_unit = _dataset_unit(time_ds, item.file, 'time_unit', 'ps')
        if structures_ds.attrs.get('constant_time_step', False):
            requested_indices = _requested_structure_indices(
                structures_ds, structure_indices
            )
            time = (
                time_ds[0]
                + structures_ds.attrs['time_step'] * requested_indices
            )
        else:
            time = _read_structure_rows(time_ds, structure_indices)
        tmp_item.time = puw.quantity(time.astype(np.float64), time_unit)
    else:
        tmp_item.time = None

    # Step
    if 'step' in structures_ds and structures_ds['step'].shape[0] > 0:
        tmp_item.step = _read_structure_rows(
            structures_ds['step'], structure_indices
        )
    else:
        tmp_item.step = None

    # Structure ID
    if 'id' in structures_ds and structures_ds['id'].shape[0] > 0:
        id_ds = structures_ds['id']
        if structures_ds.attrs.get('constant_id_step', False):
            requested_indices = _requested_structure_indices(
                structures_ds, structure_indices
            )
            tmp_item.structure_id = (
                id_ds[0]
                + structures_ds.attrs['id_step'] * requested_indices
            )
        else:
            tmp_item.structure_id = _read_structure_rows(
                id_ds, structure_indices
            )
    else:
        tmp_item.structure_id = None

    # Thermodynamic series
    for attribute, root_unit, fallback in (
        ('temperature', 'temperature_unit', 'K'),
        ('potential_energy', 'energy_unit', 'kJ/mol'),
        ('kinetic_energy', 'energy_unit', 'kJ/mol'),
    ):
        dataset = structures_ds.get(attribute)
        if dataset is None or dataset.shape[0] == 0:
            setattr(tmp_item, attribute, None)
            continue
        unit = _dataset_unit(dataset, item.file, root_unit, fallback)
        values = _read_structure_rows(dataset, structure_indices)
        setattr(
            tmp_item,
            attribute,
            puw.quantity(values.astype(np.float64), unit),
        )

    if opened_here:
        item.close()

    return tmp_item
