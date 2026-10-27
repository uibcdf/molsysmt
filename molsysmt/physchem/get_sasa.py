import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError, warn
from molsysmt._private.variables import is_all
from molsysmt.configure import with_configure_overrides

# Atom-count threshold above which ``use_cell_list='auto'`` enables the
# cell-list occlusion search on the native CPU path. Below it the brute-force
# kernel is used, where the neighbour-list build does not pay off.
CELL_LIST_MIN_ATOMS = 1000


@signal(tags=["api", "physchem"])
@arg_digest()
@with_configure_overrides
def get_sasa(
    molecular_system,
    element="atom",
    selection="all",
    structure_indices="all",
    syntax="MolSysMT",
    engine="MolSysMT",
    probe_radius="1.4 angstroms",
    n_sphere_points=240,
    use_cell_list="auto",
    use_gpu=None,
    gpu_backend=None,
    parallel=None,
    num_threads=None,
    skip_digestion=False,
    *,
    pbc=True,
):
    """
    Computing solvent-accessible surface areas with Shrake–Rupley sampling.

    Evaluate atomic areas with all atoms present as occluders, then select or
    aggregate the requested output elements. The native engine uses bundled
    Rust kernels; the optional MDTraj engine evaluates Cartesian coordinates.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any supported form providing coordinates and the
        topology required by the selected engine.
    element : str, default='atom'
        Output level: 'atom', 'group', 'component', 'molecule', 'chain' or
        'entity'. Non-atomic outputs sum their constituent atomic areas.
    selection : str, list, tuple or numpy.ndarray, default='all'
        Selection of output elements. Atoms outside this selection still
        occlude the selected atoms; extract a subsystem first to exclude them.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Zero-based indices of structures to evaluate, preserving order and
        repeated indices.
    syntax : str, default='MolSysMT'
        Selection syntax used to interpret string selections.
    engine : str, default='MolSysMT'
        Calculation provider: 'MolSysMT' or 'MDTraj'. MDTraj requires its
        optional dependency and supports Cartesian SASA only.
    probe_radius : str or quantity, default='1.4 angstroms'
        Solvent-probe radius with length units. Explicit compatible units are
        converted to the engine's working length unit.
    n_sphere_points : int, default=240
        Positive number of sampling points per atom. Increasing this number
        improves surface quadrature at additional computational cost.
    use_cell_list : bool or str, default='auto'
        Native CPU occlusion search. True enables cell lists, False uses
        brute force; 'auto' enables cell lists at 1,000 atoms or more.
        This choice does not affect the MDTraj engine.
    use_gpu : bool or None, default=None
        Compatibility selector, inheriting configuration when None. No GPU
        backend is supported in 1.0; GPU requests warn and use the CPU.
    gpu_backend : str or None, default=None
        Compatibility configuration override for the retired GPU selectors.
    parallel : bool or None, default=None
        Override native CPU parallel execution; None inherits configuration.
    num_threads : int or None, default=None
        Override the native CPU thread count; None inherits configuration.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.
    pbc : bool, default=True
        Keyword-only periodic control. With a box, the native engine applies
        minimum-image occlusion by other atoms. Without a box it evaluates
        Cartesian coordinates. False requests Cartesian SASA for either
        engine, ignoring the box. MDTraj with a box and pbc=True raises an
        error rather than silently ignoring periodicity.

    Returns
    -------
    quantity
        Areas with shape ``(n_structures, n_elements)`` in the square of the
        configured standard length unit (nm² by default). Convert explicitly
        with PyUnitWizard when a particular area unit is required.

    Raises
    ------
    NotImplementedMethodError
        If the engine is unsupported, or periodic MDTraj SASA is requested
        for a system with a box.

    Notes
    -----
    Shrake–Rupley sampling estimates the accessible fraction of a sphere whose
    radius is the atom's van der Waals radius plus the solvent-probe radius
    [1]_. The result depends on the radii and sampling density. Both supported
    engines include all input atoms as occluders, including solvent.

    Native periodic screening applies the minimum-image convention between
    each sample point and other atom indices. It does not include an atom's
    own periodic images; do not interpret it as a general all-images surface
    calculation for cells small enough for self-image occlusion. Cartesian
    SASA may require reconstructing whole molecules before calculation.
    MDTraj's public Shrake–Rupley interface has no periodic control [2]_.

    See Also
    --------
    get_atomic_radius : Querying atomic radii.
    molsysmt.pbc.unwrap : Reconstructing molecular coordinates across structures.

    References
    ----------
    .. [1] Shrake, A. and Rupley, J. A. (1973). Environment and exposure to
       solvent of protein atoms. Lysozyme and insulin. J. Mol. Biol. 79,
       351–371. https://doi.org/10.1016/0022-2836(73)90011-9
    .. [2] MDTraj Shrake–Rupley documentation:
       https://mdtraj.readthedocs.io/en/latest/api/generated/mdtraj.shrake_rupley.html

    Examples
    --------
    >>> import molsysmt as msm
    >>> molsys = msm.systems['Trp-Cage']['1l2y.h5msm']
    >>> area = msm.physchem.get_sasa(molsys, selection=[0],
    ...                            structure_indices=0, pbc=False, use_gpu=False)
    >>> area.shape
    (1, 1)
    >>> bool(msm.pyunitwizard.get_value(area, to_unit='nm**2')[0, 0] >= 0)
    True

    .. admonition:: Tutorial

       See :ref:`Tutorial_Get_sasa` for aggregation, units and periodic choices.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import convert, get, select

    if engine not in {"MolSysMT", "MDTraj"}:
        raise NotImplementedMethodError(
            method=engine, caller="molsysmt.physchem.get_sasa"
        )

    # Read the requested box population once. Cartesian requests do not use it.
    periodic_box = (
        get(
            molecular_system,
            element="system",
            structure_indices=structure_indices,
            box=True,
        )
        if pbc
        else None
    )

    if engine == "MDTraj":
        if periodic_box is not None:
            raise NotImplementedMethodError(
                method="MDTraj periodic SASA",
                arguments="pbc=True with a periodic box",
                caller="molsysmt.physchem.get_sasa",
                message=(
                    "MDTraj does not implement periodic SASA. Set pbc=False "
                    "for Cartesian coordinates or select engine='MolSysMT' "
                    "for minimum-image occlusion."
                ),
            )
        tmp_item = convert(
            molecular_system,
            to_form="mdtraj.Trajectory",
            structure_indices=structure_indices,
        )

        from mdtraj import shrake_rupley

        if isinstance(probe_radius, str):
            probe_radius = puw.parse.parse(probe_radius)
        mdtraj_probe_radius = puw.get_value(probe_radius, to_unit="nm")
        sasa_array = shrake_rupley(
            tmp_item,
            probe_radius=mdtraj_probe_radius,
            n_sphere_points=n_sphere_points,
            mode="atom",
        )

        if element == "atom":
            if not is_all(selection):
                atom_indices = select(
                    molecular_system, selection=selection, syntax=syntax
                )
                sasa_array = sasa_array[:, atom_indices]

        else:
            sets_atoms = get(
                molecular_system,
                element=element,
                selection=selection,
                syntax=syntax,
                atom_index=True,
            )

            n_sets = len(sets_atoms)
            n_structures = sasa_array.shape[0]

            new_sasa_array = np.empty([n_structures, n_sets], dtype="float")
            for ii in range(n_sets):
                new_sasa_array[:, ii] = sasa_array[:, sets_atoms[ii]].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = puw.quantity(sasa_array, "nm**2")
        sasa_array = puw.standardize(sasa_array)

    elif engine == "MolSysMT":
        import molsysmt.configure as config
        from molsysmt._private.gpu import resolve_use_gpu
        from molsysmt.lib.structure._kernel_inputs import (
            extract_coordinates_value_and_unit,
        )
        from molsysmt.physchem import get_atomic_radius

        # Shrake-Rupley requires the full system to calculate occlusion correctly
        coordinates = get(
            molecular_system,
            element="atom",
            selection="all",
            structure_indices=structure_indices,
            coordinates=True,
        )
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        radii = get_atomic_radius(
            molecular_system, element="atom", selection="all", definition="vdw"
        )
        radii_val = puw.get_value(radii, to_unit=length_unit)

        # Rolling solvent probe radius (default: 1.4 angstroms, the standard water probe)
        if isinstance(probe_radius, str):
            probe_radius = puw.parse.parse(probe_radius)
        probe_radius = puw.get_value(probe_radius, to_unit=length_unit)

        payload = coordinates.shape[0] * coordinates.shape[1]
        _use_gpu = resolve_use_gpu(use_gpu, payload)

        box = None
        if periodic_box is not None:
            from molsysmt._private.pbc_validation import validate_box_array

            # The shared validator owns shape, finite/singular checks and
            # constant-box broadcasting on the canonical nm boundary.
            box_nm = validate_box_array(
                puw.get_value(periodic_box, to_unit="nm"),
                coordinates.shape[0],
                caller="molsysmt.physchem.get_sasa",
            )
            box = np.asarray(
                puw.get_value(puw.quantity(box_nm, "nm"), to_unit=length_unit),
                dtype=np.float64,
            )

        sasa_array = None

        if _use_gpu:
            # Taichi backend
            if config.gpu_backend == "taichi":
                try:
                    __import__("taichi")

                    taichi_available = True
                except ImportError:
                    taichi_available = False
                    from molsysmt._private.smonitor import GpuNotAvailableWarning

                    warn(
                        GpuNotAvailableWarning(
                            reason="the taichi package is not installed"
                        )
                    )

                if taichi_available:
                    if box is not None:
                        from molsysmt.lib.structure.get_sasa_taichi import (
                            get_mic_sasa as _kernel,
                        )

                        sasa_array = _kernel(
                            coordinates,
                            box,
                            radii_val,
                            probe_radius,
                            n_points=n_sphere_points,
                        )
                    else:
                        from molsysmt.lib.structure.get_sasa_taichi import (
                            get_sasa as _kernel,
                        )

                        sasa_array = _kernel(
                            coordinates,
                            radii_val,
                            probe_radius,
                            n_points=n_sphere_points,
                        )

            # Retired experimental CUDA branch.
            if sasa_array is None:
                if box is not None:
                    from molsysmt.lib.structure.get_sasa_cuda import (
                        get_mic_sasa as _kernel,
                    )

                    sasa_array = _kernel(
                        coordinates,
                        box,
                        radii_val,
                        probe_radius,
                        n_points=n_sphere_points,
                    )
                else:
                    from molsysmt.lib.structure.get_sasa_cuda import get_sasa as _kernel

                    sasa_array = _kernel(
                        coordinates, radii_val, probe_radius, n_points=n_sphere_points
                    )

        # Supported Rust CPU path (also used by retired GPU selectors)
        if sasa_array is None:
            from molsysmt._private import rust_backend as _kernels
            from molsysmt.lib.structure.sphere_points import (
                get_fibonacci_sphere_points,
            )

            sphere_pts = get_fibonacci_sphere_points(n_sphere_points)

            radii_val = np.ascontiguousarray(radii_val, dtype=np.float64)
            coordinates = np.ascontiguousarray(coordinates, dtype=np.float64)

            n_atoms_total = coordinates.shape[1]
            if use_cell_list == "auto":
                _use_cell_list = n_atoms_total >= CELL_LIST_MIN_ATOMS
            else:
                _use_cell_list = bool(use_cell_list)

            if _use_cell_list:
                # Safe candidate cutoff: an occluder l can reach a test point of
                # atom i only within (r_i + probe) + (r_l + probe); bound it above
                # by 2*max_radius + 2*probe for a single global cutoff. The kernels
                # build a per-structure cell list internally and run in parallel over
                # structures.
                cutoff = 2.0 * float(radii_val.max()) + 2.0 * probe_radius
                if box is not None:
                    sasa_array = _kernels.get_mic_sasa_cell_list(
                        coordinates, box, radii_val, sphere_pts, probe_radius, cutoff
                    )
                else:
                    sasa_array = _kernels.get_sasa_cell_list(
                        coordinates, radii_val, sphere_pts, probe_radius, cutoff
                    )
            elif box is not None:
                sasa_array = _kernels.get_mic_sasa(
                    coordinates, box, radii_val, sphere_pts, probe_radius
                )
            else:
                sasa_array = _kernels.get_sasa(
                    coordinates, radii_val, sphere_pts, probe_radius
                )

        # Filter and accumulate results based on selection
        if element == "atom":
            if not is_all(selection):
                atom_indices = select(
                    molecular_system, selection=selection, syntax=syntax
                )
                sasa_array = sasa_array[:, atom_indices]
        else:
            sets_atoms = get(
                molecular_system,
                element=element,
                selection=selection,
                syntax=syntax,
                atom_index=True,
            )
            n_sets = len(sets_atoms)
            n_structures = sasa_array.shape[0]
            new_sasa_array = np.empty([n_structures, n_sets], dtype="float")
            for ii in range(n_sets):
                new_sasa_array[:, ii] = sasa_array[:, sets_atoms[ii]].sum(axis=1)
            sasa_array = new_sasa_array

        # Both native execution branches return squared working-length values.
        sasa_array = puw.quantity(sasa_array, length_unit**2)
        sasa_array = puw.standardize(sasa_array)

    else:
        raise NotImplementedMethodError()

    return sasa_array
