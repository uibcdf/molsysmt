from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def get_volume_from_lengths_and_angles(box_lengths, box_angles):
    """
    Computing box volume from lengths and angles.

    Parameters
    ----------
    box_lengths : quantity
        Edge lengths (a, b, c).
    box_angles : quantity
        Angles (alpha, beta, gamma).

    Returns
    -------
    quantity
        Volume in cubic nanometers.

    Notes
    -----
    The volume is evaluated directly as

    ``abc * sqrt(1 + 2 cos(alpha) cos(beta) cos(gamma)
    - cos(alpha)**2 - cos(beta)**2 - cos(gamma)**2)``.

    This avoids propagating the six-decimal matrix rounding performed by
    :func:`molsysmt.pbc.get_box_from_lengths_and_angles`.

    See Also
    --------
    :func:`molsysmt.pbc.get_volume_from_box`
        Computing the volume from a box matrix.

    Examples
    --------
    Computing the volume of a triclinic box with a 60-degree gamma angle:

    >>> import numpy as np
    >>> import molsysmt as msm
    >>> lengths = [[2.0, 2.0, 3.0]] * msm.pyunitwizard.unit('nm')
    >>> angles = [[90.0, 90.0, 60.0]] * msm.pyunitwizard.unit('degrees')
    >>> volume = msm.pbc.get_volume_from_lengths_and_angles(lengths, angles)
    >>> value = msm.pyunitwizard.get_value(volume, to_unit='nm**3')
    >>> np.testing.assert_allclose(value, [6.0 * np.sqrt(3.0)], atol=1.0e-12)

    .. admonition:: User guide

       See the User Guide tutorial for a worked example:
       :func:`molsysmt.pbc.get_volume_from_lengths_and_angles`.

    .. versionadded:: 1.0.0
    """

    if isinstance(box_lengths, np.ndarray):
        length_unit = puw.unit('nm')
        lengths = np.asarray(box_lengths, dtype=np.float64)
    else:
        lengths, length_unit = puw.get_value_and_unit(box_lengths)
        lengths = np.asarray(lengths, dtype=np.float64)

    angles = puw.get_value(box_angles, to_unit='radians')
    angles = np.asarray(angles, dtype=np.float64)

    cosines = np.cos(angles)
    radicand = (
        1.0
        + 2.0 * cosines[..., 0] * cosines[..., 1] * cosines[..., 2]
        - np.sum(cosines**2, axis=-1)
    )
    volume = np.prod(lengths, axis=-1) * np.sqrt(radicand)

    return puw.standardize(puw.quantity(volume, length_unit**3))
