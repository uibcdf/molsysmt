from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError


@signal(tags=["api", "structure"])
@arg_digest()
def shift_dihedral_angles(
    molecular_system,
    dihedral_quartets=None,
    shifts=None,
    blocks=None,
    structure_indices="all",
    pbc=True,
    in_place=False,
    engine="MolSysMT",
    skip_digestion=False,
):
    """
    Shifting torsions by finite increments within selected atom blocks.

    Reads the current dihedral angles with ``get_dihedral_angles``, adds the
    requested shifts, and writes the result back with ``set_dihedral_angles``.
    All covalent-block detection and PBC handling are delegated to
    ``set_dihedral_angles``.


    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported MolSysMT format.
    dihedral_quartets : list, tuple, numpy.ndarray, or None, default=None
        Nonempty zero-based atom-index quartets with shape ``(n_quartets, 4)``.
        A single quartet can be given as a vector. Each quartet contains four
        distinct, in-range integer atom indices.
    shifts : PyUnitWizard quantity or None, default=None
        Finite real angular increments, as a quantity or unit-bearing string.
        Scalars broadcast over structures and quartets; vectors specify one
        increment per quartet. A matrix has shape ``(n_structures, n_quartets)``;
        either axis may have size one for broadcasting.
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
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molecular system or None
        A new molecular system with the shifted dihedral angles when
        ``in_place=False``; ``None`` when ``in_place=True``.


    Raises
    ------
    ArgumentError
        If increments are nonfinite, complex or empty, or quartets/blocks are invalid.
    ArgumentLengthError
        If angular dimensions cannot broadcast to the selected structures/quartets.
    StructuralInconsistencyError
        If the resulting rotation produces nonfinite moving coordinates.
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
    >>> import numpy as np
    >>> import molsysmt as msm
    >>> molsys = msm.convert(msm.systems['Met-enkephalin']['met_enkephalin.h5msm'])
    >>> quartet = msm.topology.get_dihedral_quartets(molsys, phi=True)[2]
    >>> before = msm.structure.get_dihedral_angles(molsys, dihedral_quartets=quartet)
    >>> changed = shift_dihedral_angles(molsys, dihedral_quartets=quartet,
    ...                                shifts='.2 radians', pbc=False)
    >>> after = msm.structure.get_dihedral_angles(changed, dihedral_quartets=quartet)
    >>> delta = msm.pyunitwizard.get_value(after - before, to_unit='radians')
    >>> bool(np.allclose(np.arctan2(np.sin(delta), np.cos(delta)), .2))
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Shift_dihedral_angles`.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get

    from . import get_dihedral_angles, set_dihedral_angles
    from ._dihedral_edits import angular_values, check_angle_shape, quartet_indices

    if engine != "MolSysMT":
        raise NotImplementedMethodError()
    caller = "molsysmt.structure.shift_dihedral_angles"
    shifts_value = angular_values(shifts, "shifts", caller)
    n_atoms, n_structures = get(
        molecular_system,
        structure_indices=structure_indices,
        n_atoms=True,
        n_structures=True,
    )
    dihedral_quartets = quartet_indices(dihedral_quartets, n_atoms, caller)
    check_angle_shape(
        shifts_value, n_structures, len(dihedral_quartets), "shifts", caller
    )
    shifts = puw.quantity(shifts_value, "radians")

    angles = get_dihedral_angles(
        molecular_system,
        dihedral_quartets=dihedral_quartets,
        structure_indices=structure_indices,
        pbc=pbc,
    )
    angles = angles + shifts

    return set_dihedral_angles(
        molecular_system,
        dihedral_quartets=dihedral_quartets,
        angles=angles,
        blocks=blocks,
        structure_indices=structure_indices,
        pbc=pbc,
        in_place=in_place,
        engine=engine,
    )
