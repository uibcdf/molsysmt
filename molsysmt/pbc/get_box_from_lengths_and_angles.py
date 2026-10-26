import numpy as np

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest


@arg_digest()
def get_box_from_lengths_and_angles(box_lengths, box_angles=None, skip_digestion=False):
    """
    Building a box matrix from lengths and angles.


    Parameters
    ----------
    box_lengths : PyUnitWizard quantity
        Box lengths with shape (3,) or (n_structures, 3), in units of
        length. A plain numpy array is interpreted in nanometers. Each row
        defines one output structure.
    box_angles : PyUnitWizard quantity or None, default=None
        Alpha, beta and gamma angles, in angular units. Shape (3,) or (1, 3)
        shares one triple across all length rows; shape (n_structures, 3)
        supplies a triple for each row. None uses 90 degrees for all angles.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Row-vector box matrices with shape (n_structures, 3, 3), including
        (1, 3, 3) for one box and (0, 3, 3) for an empty length axis.
        Output follows the active PyUnitWizard length standard.


    Raises
    ------
    ArgumentError
        If units or input shapes are invalid, or the angle-row count is
        neither one nor the number of length rows.

    Notes
    -----
    The public route normalizes lengths to nanometers and rounds the matrix
    to six decimal places in those units before output standardization.
    Shared angles are broadcast before the compiled kernel; the kernel always
    receives aligned length and angle rows. Supplied angular units are
    converted to radians without requiring an application angle standard;
    only the returned length quantity needs an active length standard.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> box = msm.pbc.get_box_from_lengths_and_angles('[2, 3, 4] nm')
    >>> box.shape
    (1, 3, 3)
    >>> np.allclose(msm.pyunitwizard.get_value(box, to_unit='nm'), [np.diag([2, 3, 4])])
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_box_from_lengths_and_angles` for orthogonal and
       triclinic construction.

    .. versionadded:: 1.0.0
    """

    if isinstance(box_lengths, np.ndarray):
        units = puw.unit("nm")
        lengths_value = box_lengths
    else:
        units = puw.get_unit(box_lengths)
        lengths_value = puw.get_value(box_lengths)
    if box_angles is None:
        angles_value = np.full((1, 3), np.pi / 2, dtype=np.float64)
    else:
        angles_value = puw.get_value(box_angles, to_unit="radians")
    if angles_value.shape[0] not in (1, lengths_value.shape[0]):
        from molsysmt._private.smonitor import ArgumentError

        raise ArgumentError(
            "box_angles",
            caller="molsysmt.pbc.get_box_from_lengths_and_angles",
            message="Supply one angle triple or one per length row.",
        )
    angles_value = np.broadcast_to(angles_value, lengths_value.shape)

    box = _kernels.get_box_from_lengths_and_angles(
        np.array(lengths_value, dtype=np.float64),
        np.array(angles_value, dtype=np.float64),
    )
    box = box.round(6) * units

    del (lengths_value, angles_value)

    box = puw.standardize(box)

    return box
