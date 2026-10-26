import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import (
    NotImplementedMethodError,
    StructuralInconsistencyError,
)
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit


@signal(tags=["api", "structure"])
@arg_digest()
def set_dihedral_angles(
    molecular_system,
    dihedral_quartets=None,
    angles=None,
    blocks=None,
    structure_indices="all",
    pbc=True,
    in_place=False,
    engine="MolSysMT",
):
    """
    Setting finite target torsions by rotating selected atom blocks.

    For each dihedral quartet ``(i, j, k, l)``, the function determines which
    atoms form a covalently connected block on the side of atom ``l`` after the
    bond ``j-k`` is removed.  That block is then rotated about the ``j-k`` axis
    so that the dihedral angle reaches the target value.

    When ``pbc=True`` and the system has a periodic box the minimum-image
    dihedral kernel is used; otherwise the standard (non-periodic) kernel is
    applied.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    dihedral_quartets : list, tuple, numpy.ndarray, or None, default=None
        Nonempty zero-based atom-index quartets with shape ``(n_quartets, 4)``.
        A single quartet can be given as a vector. Each quartet contains four
        distinct, in-range integer atom indices.
    angles : PyUnitWizard quantity or None, default=None
        Finite real target angles, as an angular quantity or unit-bearing string.
        A scalar broadcasts over structures and quartets. A vector is interpreted
        per quartet; a matrix has shape ``(n_structures, n_quartets)``. Either
        matrix axis may have size one for broadcasting.
    blocks : list, tuple, numpy.ndarray, or None, default=None
        Pool of nonempty one-dimensional integer atom-index lists. For each
        quartet, the union of all blocks containing its fourth atom is rotated.
        Every fourth atom must belong to a block. Indices must be in range.
        None computes covalent blocks after cutting each central bond.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    pbc : bool, default=True
        Whether to take periodic boundary conditions into account.
    in_place : bool, default=False
        Whether to modify the input molecular system in place.
    engine : str, default='MolSysMT'
        Backend used to perform the calculation.

    Returns
    -------
    molecular system or None
        A new molecular system with the updated dihedral angles when
        ``in_place=False``; ``None`` when ``in_place=True``.


    Raises
    ------
    ArgumentError
        If edit values are nonfinite, complex or empty, or quartets/blocks are invalid.
    ArgumentLengthError
        If angular dimensions cannot broadcast to the selected structures/quartets.
    StructuralInconsistencyError
        If the rotation produces nonfinite moving coordinates.
    NotImplementedMethodError
        If an unsupported engine is requested.


    Notes
    -----
    All validation and rotation finish before coordinates are published. Rejection
    preserves the input coordinates, box, topology and named interaction coverage.
    A successful edit invalidates interactions on edited structures, including
    previously evaluated empty structures; no interaction detector is rerun.
    Explicit blocks define the moving population and are used as supplied. They
    are a shared pool, not one row assigned to each quartet. Box matrices and
    chemical assignments are unchanged. Read-only undefined-angle measurements
    retain their existing semantics; editing requests must be finite.

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])
    >>> quartet = msm.topology.get_dihedral_quartets(molsys, phi=True)[2]
    >>> changed = set_dihedral_angles(molsys, dihedral_quartets=quartet,
    ...                              angles='0 degrees', pbc=False)
    >>> angle = msm.structure.get_dihedral_angles(changed, dihedral_quartets=quartet)
    >>> bool(abs(msm.pyunitwizard.get_value(angle, to_unit='radians')[0, 0]) < 1e-10)
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Set_dihedral_angles`.

    .. versionadded:: 1.0.0
    """

    if engine == "MolSysMT":
        from molsysmt.basic import copy, get, set

        from ._dihedral_edits import (
            angular_values,
            block_mask,
            check_angle_shape,
            quartet_indices,
        )

        caller = "molsysmt.structure.set_dihedral_angles"
        angles = angular_values(angles, "angles", caller)

        coordinates = get(
            molecular_system,
            element="system",
            structure_indices=structure_indices,
            coordinates=True,
        )
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        dihedral_quartets = quartet_indices(
            dihedral_quartets, coordinates.shape[1], caller
        )
        check_angle_shape(
            angles, coordinates.shape[0], len(dihedral_quartets), "angles", caller
        )
        on_in_blocks = block_mask(
            molecular_system,
            dihedral_quartets,
            blocks,
            coordinates.shape[1],
            structure_indices,
            caller,
        )
        # A private selected-coordinate buffer protects every input form until publication.
        coordinates = np.array(coordinates, dtype=np.float64, order="C", copy=True)

        if pbc:
            box = get(
                molecular_system,
                element="system",
                structure_indices=structure_indices,
                box=True,
            )

            if box is not None:
                if box[0] is not None:
                    box = np.asarray(
                        puw.get_value(box, to_unit=length_unit), dtype=np.float64
                    )
                    _kernels.set_mic_dihedral_angles(
                        coordinates, box, angles, dihedral_quartets, on_in_blocks
                    )
                    del box
                else:
                    pbc = False
            else:
                pbc = False

        if not pbc:
            _kernels.set_dihedral_angles(
                coordinates, angles, dihedral_quartets, on_in_blocks
            )

        if not np.isfinite(coordinates[:, np.any(on_in_blocks, axis=0), :]).all():
            raise StructuralInconsistencyError(
                reason="The requested torsion edit produces nonfinite moving coordinates.",
                caller=caller,
            )

        coordinates = puw.quantity(coordinates, length_unit)

        if in_place:
            set(
                molecular_system,
                structure_indices=structure_indices,
                coordinates=coordinates,
            )
            del coordinates
        else:
            tmp_molecular_system = copy(molecular_system)
            set(
                tmp_molecular_system,
                structure_indices=structure_indices,
                coordinates=coordinates,
            )
            del coordinates
            return tmp_molecular_system

    else:
        raise NotImplementedMethodError()
