import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import ArgumentError


@signal(tags=["api", "structure"])
@arg_digest()
def flip(
    molecular_system,
    vector=None,
    point="[0,0,0] nm",
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    in_place=False,
):
    """
    Reflecting an atom population across a plane defined by a normal and a point.

    Every selected coordinate is mirrored across the same plane. A finite nonzero
    scaling, including a sign reversal, of the normal describes the same plane.
    The normal is normalized at the public boundary before calling the Rust kernel.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing readable and writable
        coordinates and the attributes required to resolve the selection.
    vector : array-like or None, default=None
        Finite nonzero unit-free plane normal with shape (3,). None uses
        [0, 0, 1], the normal to a plane parallel to the xy plane. Its magnitude
        does not affect the result; the caller's vector is not modified.
    point : quantity or str, default='[0,0,0] nm'
        One finite point on the plane, with shape (3,) or (1, 3) and length units.
        The same point is used for every selected structure. Per-structure plane
        points are not supported. Lengths are converted through PyUnitWizard.
    selection : str, list, tuple, or numpy.ndarray, default='all'
        Atoms to reflect. Other atoms remain unchanged.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices to process. Nonconsecutive and repeated indices are
        supported. Other structures remain unchanged.
    syntax : str, default='MolSysMT'
        Syntax used to resolve the atom selection.
    in_place : bool, default=False
        If True, update the input and return None; otherwise return an independent
        copy in the input form.

    Returns
    -------
    molecular system or None
        Independent reflected system when ``in_place=False``; None otherwise.

    Raises
    ------
    ArgumentError
        If the normal is zero, nonfinite or malformed; the plane point is missing,
        nonfinite or has unsupported shape/units; or the reflected coordinates
        are nonfinite. Invalid plane inputs reject before coordinate writes.

    Notes
    -----
    For a unit normal n and plane point p, the reflected coordinate is
    ``r - 2 * dot(r-p, n) * n``. Reflection preserves pair distances within the
    reflected population and reverses handedness. Stored topology and chemical
    assignments remain unchanged. Boxes are preserved; no periodic wrapping or
    reconstruction is performed. Native coordinate publication invalidates stored
    interaction coverage only for the edited structures. Rejected plane inputs
    preserve coordinates, boxes and that coverage.

    See Also
    --------
    molsysmt.structure.rotate : Applying a proper spatial rotation.
    molsysmt.structure.center : Placing a source center at a target.

    Examples
    --------
    >>> import molsysmt as msm
    >>> import numpy as np
    >>> molsys = msm.convert(msm.systems['alanine dipeptide']['alanine_dipeptide.h5msm'])
    >>> reflected = msm.structure.flip(molsys, vector=[2, 0, 0])
    >>> before = msm.pyunitwizard.get_value(msm.get(molsys, coordinates=True), to_unit='nm')
    >>> after = msm.pyunitwizard.get_value(msm.get(reflected, coordinates=True), to_unit='nm')
    >>> np.allclose(after[..., 0], -before[..., 0])
    True
    >>> np.allclose(after[..., 1:], before[..., 1:])
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Flip` for normal scaling, selected scopes and rejection rules.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import copy, get, set

    if point is None:
        raise ArgumentError("point", caller="molsysmt.structure.flip")
    point = np.asarray(puw.get_value(point, to_unit="nm"), dtype=np.float64)
    if point.shape != (1, 3) or not np.all(np.isfinite(point)):
        raise ArgumentError(
            "point",
            caller="molsysmt.structure.flip",
            message="Supply one finite plane point with shape (3,) or (1, 3) and length units.",
        )

    coordinates = get(
        molecular_system,
        element="atom",
        selection=selection,
        structure_indices=structure_indices,
        syntax=syntax,
        coordinates=True,
    )

    coordinates = puw.get_value(coordinates, to_unit="nm")

    coordinates = np.asarray(coordinates, dtype=np.float64)
    if vector is None:
        vector = [0.0, 0.0, 1.0]
    vector = np.asarray(vector, dtype=np.float64)
    point = np.asarray(point, dtype=np.float64)

    point = point[0]

    coordinates = _kernels.flip(coordinates, vector, point)
    if not np.all(np.isfinite(coordinates)):
        raise ArgumentError(
            "molecular_system",
            caller="molsysmt.structure.flip",
            message="Reflection requires finite coordinates and a finite representable result.",
        )

    coordinates = puw.standardize(puw.quantity(coordinates, unit="nm"))

    if in_place:
        set(
            molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
        )
        del coordinates

    else:
        tmp_molecular_system = copy(molecular_system)
        set(
            tmp_molecular_system,
            selection=selection,
            structure_indices=structure_indices,
            syntax=syntax,
            coordinates=coordinates,
        )
        del coordinates

        return tmp_molecular_system
