from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from smonitor import signal
import numpy as np
from scipy.spatial.transform import Rotation
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

    * **numpy.ndarray** of shape ``(n_structures, n_groups, 3, 3)`` or
      ``(1, 1, 3, 3)``: a per-structure (or broadcast) rotation matrix.
    * **scipy.spatial.transform.Rotation**: a single ``Rotation`` object applied
      to every frame.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any form supported by MolSysMT.
    rotation : numpy.ndarray or scipy.spatial.transform.Rotation or None
        Rotation to apply.

        * ``numpy.ndarray`` of shape ``(n_structures, 1, 3, 3)``: different
          rotation per frame, same rotation for all atoms within a frame.
        * ``numpy.ndarray`` of shape ``(1, 1, 3, 3)``: single rotation broadcast
          to all frames.
        * ``scipy.spatial.transform.Rotation``: single rotation applied to every
          frame.
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
    NotImplementedMethodError
        If ``rotation`` is not a supported type.

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

        if shape[:2]==(1,1):
            rotator = Rotation.from_matrix(rotation[0,0,:,:])
            for ii in range(coordinates.shape[0]):
                coordinates[ii,:,:] = rotator.apply(coordinates[ii,:,:])
        elif shape[1]==1:
            for ii in range(coordinates.shape[0]):
                rotator = Rotation.from_matrix(rotation[ii,0,:,:])
                coordinates[ii,:,:] = rotator.apply(coordinates[ii,:,:])
        else:
            for ii in range(coordinates.shape[0]):
                for jj in range(coordinates.shape[1]):
                    rotator = Rotation.from_matrix(rotation[ii,jj,:,:])
                    coordinates[ii,jj,:] = rotator.apply(coordinates[ii,jj,:])

    elif isinstance(rotation, Rotation):

        rotator = rotation
        for ii in range(coordinates.shape[0]):
            coordinates[ii,:,:] = rotator.apply(coordinates[ii,:,:])

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

