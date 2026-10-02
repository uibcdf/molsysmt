import os

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.h5msm_units import legacy_dataset_unit
from molsysmt._private.variables import is_all


def _read_structure_rows(dataset, structure_indices):
    """Reading structure rows while preserving order and repeated indices."""

    if is_all(structure_indices):
        return dataset[:]
    return np.asarray([dataset[int(index)] for index in structure_indices])


def _requested_structure_indices(structures, structure_indices):
    """Returning logical structure indices for compressed structural series."""

    if is_all(structure_indices):
        n_structures = int(
            structures.attrs.get(
                "n_structures_written",
                structures["coordinates"].shape[0],
            )
        )
        return np.arange(n_structures, dtype=np.int64)
    return np.asarray(structure_indices, dtype=np.int64)


@arg_digest(form="molsysmt.H5MSMFileHandler")
def to_molsysmt_Structures(
    item, atom_indices="all", structure_indices="all", skip_digestion=False
):
    """
    Converting from molsysmt.H5MSMFileHandler to molsysmt.Structures.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.Structures
        Resulting object in molsysmt.Structures form.


    Raises
    ------
    FormatError
        If a populated structural dataset has missing, invalid, or contradictory units.

    Notes
    -----
    Legacy units must be explicit at dataset, structural-group, or root level.
    Duplicate declarations must describe the same scale and dimension.
    The native Structures object stores canonical physical quantities.

    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_H5MSMFileHandler.to_molsysmt_H5MSMFileHandler import (
        to_molsysmt_H5MSMFileHandler,
    )
    from molsysmt.native import Structures

    if isinstance(item, (str, os.PathLike)):
        item = to_molsysmt_H5MSMFileHandler(str(str(item)), skip_digestion=True)
        opened_here = True
    else:
        opened_here = False

    structures_ds = item.file["structures"]

    tmp_item = Structures()

    # Coordinates
    coordinates_ds = structures_ds["coordinates"]
    coordinates_unit = legacy_dataset_unit(coordinates_ds)
    coordinates = _read_structure_rows(coordinates_ds, structure_indices)
    if not is_all(atom_indices):
        coordinates = coordinates[:, atom_indices, :]
    tmp_item.coordinates = puw.quantity(
        coordinates.astype(np.float64), coordinates_unit
    )

    # Velocities
    velocities_ds = structures_ds.get("velocities")
    if velocities_ds is not None and velocities_ds.shape[0] > 0:
        velocities_unit = legacy_dataset_unit(velocities_ds)
        velocities = _read_structure_rows(velocities_ds, structure_indices)
        if not is_all(atom_indices):
            velocities = velocities[:, atom_indices, :]
        tmp_item.velocities = puw.quantity(
            velocities.astype(np.float64), velocities_unit
        )
    else:
        tmp_item.velocities = None

    # Box
    if "box" in structures_ds and structures_ds["box"].shape[0] > 0:
        box_ds = structures_ds["box"]
        box_unit = legacy_dataset_unit(box_ds)
        if structures_ds.attrs.get("constant_box", False):
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
    if "b_factor" in structures_ds and structures_ds["b_factor"].shape[0] > 0:
        b_factor_unit = legacy_dataset_unit(structures_ds["b_factor"])
        b_factor = _read_structure_rows(structures_ds["b_factor"], structure_indices)
        if not is_all(atom_indices):
            b_factor = b_factor[:, atom_indices]
        tmp_item.b_factor = puw.quantity(b_factor.astype(np.float64), b_factor_unit)
    else:
        tmp_item.b_factor = None

    # Time
    if "time" in structures_ds and structures_ds["time"].shape[0] > 0:
        time_ds = structures_ds["time"]
        time_unit = legacy_dataset_unit(time_ds)
        if structures_ds.attrs.get("constant_time_step", False):
            requested_indices = _requested_structure_indices(
                structures_ds, structure_indices
            )
            time = time_ds[0] + structures_ds.attrs["time_step"] * requested_indices
        else:
            time = _read_structure_rows(time_ds, structure_indices)
        tmp_item.time = puw.quantity(time.astype(np.float64), time_unit)
    else:
        tmp_item.time = None

    # Step
    if "step" in structures_ds and structures_ds["step"].shape[0] > 0:
        tmp_item.step = _read_structure_rows(structures_ds["step"], structure_indices)
    else:
        tmp_item.step = None

    # Structure ID
    if "id" in structures_ds and structures_ds["id"].shape[0] > 0:
        id_ds = structures_ds["id"]
        if structures_ds.attrs.get("constant_id_step", False):
            requested_indices = _requested_structure_indices(
                structures_ds, structure_indices
            )
            tmp_item.structure_id = (
                id_ds[0] + structures_ds.attrs["id_step"] * requested_indices
            )
        else:
            tmp_item.structure_id = _read_structure_rows(id_ds, structure_indices)
    else:
        tmp_item.structure_id = None

    # Thermodynamic series
    for attribute in ("temperature", "potential_energy", "kinetic_energy"):
        dataset = structures_ds.get(attribute)
        if dataset is None or dataset.shape[0] == 0:
            setattr(tmp_item, attribute, None)
            continue
        unit = legacy_dataset_unit(dataset)
        values = _read_structure_rows(dataset, structure_indices)
        setattr(
            tmp_item,
            attribute,
            puw.quantity(values.astype(np.float64), unit),
        )

    if opened_here:
        item.close()

    return tmp_item
