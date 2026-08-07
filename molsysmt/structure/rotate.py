from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError, StructuralInconsistencyError
from smonitor import signal
import numpy as np
from molsysmt import pyunitwizard as puw
import gc

@signal(tags=['api', 'structure'])
@arg_digest()
def rotate(molecular_system, rotation=None, rotation_center=None, selection='all', structure_indices='all',
        syntax='MolSysMT', in_place=False, skip_digestion=False):
    """
    Rotate atomic coordinates of a selection by a given rotation.

    The rotation is applied frame-by-frame.  If a ``rotation_center`` is provided,
    the coordinates are first translated so that the center sits at the origin,
    rotated, then translated back.

    Two rotation representations are accepted:

    * Array-like matrices of shape ``(3, 3)``, ``(n_structures, 3, 3)``, or
      ``(n_structures, n_atoms, 3, 3)``.
    * An object providing an ``apply(coordinates)`` method, such as
      ``scipy.spatial.transform.Rotation``. SciPy is not required.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    rotation : array-like or rotation-like object
        Rotation to apply.

        * array-like of shape ``(n_structures, 3, 3)``: different
          rotation per frame, same rotation for all atoms within a frame.
        * array-like of shape ``(3, 3)``: single rotation broadcast to all frames.
        * array-like of shape ``(n_structures, n_atoms, 3, 3)``: one rotation
          per atom and frame.
        * rotation-like object: its ``apply`` method is used for every frame.
    rotation_center : quantity or None, default None
        Centre of rotation as a PyUnitWizard length quantity of shape
        ``(n_structures, 1, 3)`` or ``(1, 1, 3)``.  When provided, coordinates
        are shifted to the origin before rotation and shifted back afterwards.
        When ``None``, the rotation is applied around the global origin.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms whose coordinates are rotated.
    structure_indices : 'all' or array-like, default 'all'
        Frame indices over which the rotation is applied.
    syntax : str, default 'MolSysMT'
        Selection syntax used when ``selection`` is a string.
    in_place : bool, default False
        If ``True`` the molecular system is modified in-place and ``None`` is
        returned.  If ``False`` a new copy is returned with the rotated
        coordinates.
    skip_digestion : bool, default False
        Whether to skip argument digestion (for internal use on trusted hot paths).

    Returns
    -------
    molecular system or None
        A new molecular system with the rotated coordinates when
        ``in_place=False``; ``None`` when ``in_place=True``.

    Raises
    ------
    ArgumentError
        If a matrix has an invalid shape, non-finite values, is not orthonormal,
        or has a determinant other than +1.
    NotImplementedMethodError
        If ``rotation`` is not a supported type.
    StructuralInconsistencyError
        If the number of per-frame or per-atom matrices cannot be broadcast to
        the selected coordinates.

    Notes
    -----
    MolSysMT uses active proper rotations on row-vector coordinates. Distances
    and handedness are therefore preserved.

    See Also
    --------
    :func:`molsysmt.structure.translate`
        Translate selected coordinates.
    :func:`molsysmt.structure.least_rmsd_fit`
        Estimate and apply a least-RMSD rigid transformation.

    Examples
    --------
    >>> import molsysmt as msm
    >>> coordinates = msm.pyunitwizard.quantity([[[1.0, 0.0, 0.0]]], 'nm')
    >>> rotation = [[0.0, -1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]]
    >>> rotated = msm.structure.rotate(coordinates, rotation=rotation)
    >>> msm.pyunitwizard.get_value(rotated, to_unit='nm').round(12).tolist()
    [[[0.0, 1.0, 0.0]]]

    .. admonition:: Tutorial with more examples

       See :ref:`Tutorial_Rotate`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, set, select, copy
    from molsysmt.structure import translate

    coordinates = get(molecular_system, element='atom', selection=selection, structure_indices=structure_indices,
                      syntax=syntax, coordinates=True)

    if rotation_center is not None:

        coordinates = translate(coordinates, translation=-rotation_center)

    coordinates, length_unit =  puw.get_value_and_unit(coordinates)

    if isinstance(rotation, np.ndarray):

        shape=rotation.shape

        if shape[0] not in (1, coordinates.shape[0]):
            raise StructuralInconsistencyError(
                reason=(
                    f"Rotation matrices provide {shape[0]} frames but the "
                    f"coordinate selection contains {coordinates.shape[0]}."
                ),
                caller="molsysmt.structure.rotate",
            )
        if shape[1] not in (1, coordinates.shape[1]):
            raise StructuralInconsistencyError(
                reason=(
                    f"Rotation matrices provide {shape[1]} atoms but the "
                    f"coordinate selection contains {coordinates.shape[1]}."
                ),
                caller="molsysmt.structure.rotate",
            )

        if shape[:2]==(1,1):
            for ii in range(coordinates.shape[0]):
                coordinates[ii,:,:] = coordinates[ii,:,:] @ rotation[0,0,:,:].T
        elif shape[1]==1:
            for ii in range(coordinates.shape[0]):
                coordinates[ii,:,:] = coordinates[ii,:,:] @ rotation[ii,0,:,:].T
        else:
            for ii in range(coordinates.shape[0]):
                rotation_frame = 0 if shape[0] == 1 else ii
                for jj in range(coordinates.shape[1]):
                    coordinates[ii,jj,:] = (
                        coordinates[ii,jj,:] @ rotation[rotation_frame,jj,:,:].T
                    )

    elif callable(getattr(rotation, "apply", None)):

        for ii in range(coordinates.shape[0]):
            coordinates[ii,:,:] = rotation.apply(coordinates[ii,:,:])

    else:

        raise NotImplementedMethodError(caller='molsysmt.structure.rotate')

    coordinates = puw.quantity(coordinates, unit=length_unit)

    if rotation_center is not None:

        coordinates = translate(coordinates, translation=rotation_center)


    if in_place:

        set(molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates, rotation_center)
        gc.collect()

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection=selection, structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)
        del(coordinates, rotation_center)
        gc.collect()

        return tmp_molecular_system
