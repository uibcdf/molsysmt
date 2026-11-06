#######################################################################################
########### THE FOLLOWING LINES NEED TO BE CUSTOMIZED FOR EVERY CLASS  ################
#######################################################################################
import types

import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all

form = "mmcif.PdbxContainers.DataContainer"


## From atom


@arg_digest(form=form)
def get_coordinates_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting coordinates from atom in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import get_coordinates_from_atom as aux_get

    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    return output


@arg_digest(form=form)
def get_occupancy_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting occupancy from atom in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Parsed mmCIF or BinaryCIF DataContainer to inspect.
    indices : object, default='all'
        Canonical atom indices. Explicit order and repetitions are preserved.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray or None
        Dimensionless floating-point occupancies with shape
        ``(n_selected_structures, n_selected_atoms)``. Unknown cells are NaN;
        an entirely unavailable field is None. Structure order and repetitions
        follow ``structure_indices``.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.convert(msm.systems['chicken villin HP35']['1vii.bcif.gz'],
    ...                      to_form='mmcif.PdbxContainers.DataContainer')
    >>> get_occupancy_from_atom(source, indices=[2, 0, 2], structure_indices=[0, 0]).shape
    (2, 3)


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import get_occupancy_from_atom as aux_get

    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    return output


@arg_digest(form=form)
def get_alternate_location_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting alternate location from atom in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import (
        get_alternate_location_from_atom as aux_get,
    )

    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    return output


@arg_digest(form=form)
def get_b_factor_from_atom(
    item, indices="all", structure_indices="all", skip_digestion=False
):
    """
    Getting b factor from atom in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Parsed mmCIF or BinaryCIF DataContainer to inspect.
    indices : object, default='all'
        Canonical atom indices. Explicit order and repetitions are preserved.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity or None
        B factors on the selected structure/atom axes, carrying squared-length
        units. Source values are in squared angstroms; structure order and
        repetitions follow ``structure_indices``.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import get_b_factor_from_atom as aux_get

    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(
        tmp_item,
        indices=indices,
        structure_indices=structure_indices,
        skip_digestion=True,
    )

    return output


@arg_digest(form=form)
def get_formal_charge_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting formal charge from atom in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import (
        get_formal_charge_from_atom as aux_get,
    )
    from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanics import (
        to_molsysmt_MolecularMechanics,
    )

    tmp_item = to_molsysmt_MolecularMechanics(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


@arg_digest(form=form)
def get_partial_charge_from_atom(item, indices="all", skip_digestion=False):
    """
    Getting partial charge from atom in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    indices : object, default='all'
        Argument indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_MolecularMechanics import (
        get_partial_charge_from_atom as aux_get,
    )
    from molsysmt.form.molsysmt_MolecularMechanics.to_molsysmt_MolecularMechanics import (
        to_molsysmt_MolecularMechanics,
    )

    tmp_item = to_molsysmt_MolecularMechanics(item, skip_digestion=True)
    output = aux_get(tmp_item, indices=indices, skip_digestion=True)

    return output


## From system


@arg_digest(form=form)
def get_n_structures_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting n structures from system in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if is_all(structure_indices):
        from ._model_axis import model_axis

        _, labels = model_axis(item)
        return len(labels)
    else:
        return len(structure_indices)


@arg_digest(form=form)
def get_box_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting box from system in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.pbc import get_box_from_lengths_and_angles

    n_structures = get_n_structures_from_system(item, skip_digestion=True)

    check_if_cell = True
    if item.exists("exptl"):
        if "NMR" in item.getObj("exptl").getValue("method"):
            check_if_cell = False

    if item.exists("cell") and check_if_cell:
        index_att = {
            jj: ii for ii, jj in enumerate(item.getObj("cell").getAttributeList())
        }
        cell_data = item.getObj("cell").data[0]

        cell_lengths = np.empty([n_structures, 3], dtype="float64")
        cell_angles = np.empty([n_structures, 3], dtype="float64")

        cell_lengths[:, 0] = float(cell_data[index_att["length_a"]])
        cell_lengths[:, 1] = float(cell_data[index_att["length_b"]])
        cell_lengths[:, 2] = float(cell_data[index_att["length_c"]])

        cell_angles[:, 0] = float(cell_data[index_att["angle_alpha"]])
        cell_angles[:, 1] = float(cell_data[index_att["angle_beta"]])
        cell_angles[:, 2] = float(cell_data[index_att["angle_gamma"]])

        cell_lengths = puw.quantity(cell_lengths, "angstroms")
        cell_angles = puw.quantity(cell_angles, "degrees")

        box = get_box_from_lengths_and_angles(
            cell_lengths, cell_angles, skip_digestion=True
        )
        box = puw.standardize(box)

    else:
        box = None

    if not is_all(structure_indices):
        if box is not None:
            box = box[structure_indices, :, :]

    return box


@arg_digest(form=form)
def get_time_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting time from system in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    return None


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices="all", skip_digestion=False):
    """
    Getting deposited model labels on the mmCIF structure axis.


    Parameters
    ----------
    item : molecular system
        Parsed mmCIF or BinaryCIF container supplying atom_site model labels.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) in the reader's existing ascending numeric
        model order. Nonconsecutive order and repetitions are preserved; labels
        are independent of positional indices.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    numpy.ndarray or None
        Detached string model labels in the selected structure order. Original
        spelling, including leading zeros, is retained. Wholly unavailable
        labels remain None; IDs are never invented from array positions.

    Raises
    ------
    FormatError
        If labels are partly missing, are not supported integers or use
        conflicting spellings for the same numeric model.

    Notes
    -----
    This reads declared labels independently of model inventory compatibility.
    The native converter retains its separate mismatch warning/list behavior;
    each incompatible returned model still carries its own deposited label.

    Examples
    --------
    >>> import molsysmt as msm
    >>> source = msm.convert(msm.systems['chicken villin HP35']['1vii.bcif.gz'],
    ...                      to_form='mmcif.PdbxContainers.DataContainer')
    >>> get_structure_id_from_system(source, structure_indices=[0, 0]).tolist()
    ['1', '1']


    .. versionadded:: 1.0.0
    """
    if structure_indices is None:
        return None
    from ._model_axis import model_axis

    _, labels = model_axis(item)
    if not labels or all(label is None for label in labels.values()):
        return None
    output = np.asarray([labels[number] for number in sorted(labels)], dtype=object)
    return output if is_all(structure_indices) else output[structure_indices]


@arg_digest(form=form)
def get_bioassembly_from_system(item, skip_digestion=False):
    """
    Getting bioassembly from system in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.mmcif_PdbxContainers_DataContainer.to_molsysmt_MolSys import (
        to_molsysmt_MolSys,
    )

    tmp_item = to_molsysmt_MolSys(item, skip_digestion=True)
    return tmp_item.structures.bioassembly


@arg_digest(form=form)
def get_n_bioassemblies_from_system(item, skip_digestion=False):
    """
    Getting n bioassemblies from system in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    if item.exists("pdbx_struct_assembly_gen"):
        index_att = {
            jj: ii
            for ii, jj in enumerate(
                item.getObj("pdbx_struct_assembly_gen").getAttributeList()
            )
        }
        assembly_ids = {
            row[index_att["assembly_id"]]
            for row in item.getObj("pdbx_struct_assembly_gen").data
        }
        return len(assembly_ids)
    return 0


@arg_digest(form=form)
def get_alternate_location_from_system(
    item, structure_indices="all", skip_digestion=False
):
    """
    Getting alternate location from system in form mmcif.PdbxContainers.DataContainer.


    Parameters
    ----------
    item : molecular system
        Argument item.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    object
        Resulting object in object form.


    .. versionadded:: 1.0.0
    """
    from molsysmt.form.molsysmt_Structures import (
        get_alternate_location_from_system as aux_get,
    )

    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = to_molsysmt_Structures(item, skip_digestion=True)
    output = aux_get(tmp_item, structure_indices=structure_indices, skip_digestion=True)

    return output


# List of functions to be imported

__all__ = [
    name
    for name, obj in globals().items()
    if isinstance(obj, types.FunctionType) and name.startswith("get_")
]
