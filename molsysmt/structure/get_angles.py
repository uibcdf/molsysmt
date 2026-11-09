import numpy as np
from smonitor import signal

from molsysmt import pyunitwizard as puw
from molsysmt._private import rust_backend as _kernels
from molsysmt._private.argdigest import arg_digest
from molsysmt.configure import with_configure_overrides


@signal(tags=["api", "structure"])
@arg_digest()
@with_configure_overrides
def get_angles(
    molecular_system,
    triplets,
    structure_indices="all",
    pbc=False,
    use_gpu=None,
    gpu_backend=None,
    skip_digestion=False,
):
    """Computing geometric angles for ordered atom-index triplets.

    Parameters
    ----------
    molecular_system : molecular system
        Any supported form supplying coordinates for the requested atoms.
    triplets : list, tuple or numpy.ndarray
        Source atom indices with shape (n_triplets, 3), or one length-three
        triplet. The middle atom is the vertex. Order and repetitions remain.
    structure_indices : int, list, tuple or numpy.ndarray, default='all'
        Source structure indices, preserving their requested order/repetitions.
    pbc : bool, default=False
        Use minimum-image vectors from the vertex when a box is available.
        Without a stored box, the native calculation is nonperiodic.
    use_gpu : bool or None, default=None
        Override configured GPU dispatch. CPU execution uses the Rust backend.
    gpu_backend : str or None, default=None
        Optional GPU backend selector, or None for the configured backend.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    quantity
        Shape (n_structures, n_triplets) in the active PyUnitWizard angular
        standard. The initial MolSysMT default is radians; an existing
        application policy or enclosing context can choose degrees instead.

    Raises
    ------
    ArgumentError
        If the triplet shape is unsupported.

    Notes
    -----
    These are geometric observations; connectivity or chemical angle assignments
    are not inferred. Zero-length legs can produce undefined native values,
    which are not replaced with zero. Coordinates for all requested structures
    and participating atoms, and the complete output, are currently resident.
    No chunked or universal memory guarantee is provided by this API.

    Convert explicitly at numerical boundaries, for example
    puw.get_value(angles, to_unit='degrees'). Conversion for display does not
    change the native returned quantity or the application's unit policy.

    See Also
    --------
    get_dihedral_angles
        Compute signed angular observations for ordered atom quartets.
    get_vectors
        Compute directed vectors between endpoints.

    Examples
    --------
    >>> import molsysmt as msm
    >>> from molsysmt import pyunitwizard as puw
    >>> from molsysmt.native import Structures
    >>> molsys = Structures(coordinates=puw.quantity(
    ...     [[[1, 0, 0], [0, 0, 0], [0, 1, 0]]], 'nm'))
    >>> with puw.context(standard_units=['nm', 'ps', 'degrees']):
    ...     angles = msm.structure.get_angles(molsys, [[0, 1, 2]], use_gpu=False)
    ...     puw.get_unit(angles) == puw.unit('degrees')
    True
    >>> round(float(puw.get_value(angles, to_unit='degrees')[0, 0]), 6)
    90.0

    .. admonition:: User guide

       See :ref:`Tutorial_Get_angles` for triplets and structural ensembles.

    .. versionadded:: 1.0.0
    """

    import molsysmt.configure as config
    from molsysmt._private.gpu import resolve_use_gpu
    from molsysmt.basic import get
    from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit

    atom_indices = []
    n_triplets = triplets.shape[0]
    aux_triplets = np.zeros((n_triplets, 3), dtype=np.int64)
    aux_dict = {}
    mm = 0
    for ii in range(n_triplets):
        for jj in range(3):
            kk = triplets[ii, jj]
            if kk in aux_dict:
                aux_triplets[ii, jj] = aux_dict[kk]
            else:
                aux_dict[kk] = mm
                atom_indices.append(kk)
                aux_triplets[ii, jj] = mm
                mm += 1
    triplets = aux_triplets
    del (aux_dict, aux_triplets)

    coordinates = get(
        molecular_system,
        element="atom",
        selection=atom_indices,
        structure_indices=structure_indices,
        coordinates=True,
    )
    coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

    # Estimate payload size and resolve GPU execution
    payload = coordinates.shape[0] * triplets.shape[0]
    _use_gpu = resolve_use_gpu(use_gpu, payload)

    angles = None

    if _use_gpu:
        box = None
        if pbc:
            box = get(
                molecular_system,
                element="system",
                structure_indices=structure_indices,
                box=True,
            )
            if box is not None and box[0] is not None:
                box = np.asarray(
                    puw.get_value(box, to_unit=length_unit), dtype=np.float64
                )
            else:
                box = None
                pbc = False

        # Taichi Lang backend
        if config.gpu_backend == "taichi":
            try:
                __import__("taichi")

                taichi_available = True
            except ImportError:
                taichi_available = False
                from molsysmt._private.smonitor import GpuNotAvailableWarning, warn

                warn(
                    GpuNotAvailableWarning(reason="the taichi package is not installed")
                )

            if taichi_available:
                if pbc:
                    from molsysmt.lib.structure.get_angles_taichi import (
                        get_mic_angles as _kernel,
                    )

                    angles = _kernel(coordinates, box, triplets)
                else:
                    from molsysmt.lib.structure.get_angles_taichi import (
                        get_angles as _kernel,
                    )

                    angles = _kernel(coordinates, triplets)

        # Retired experimental CUDA branch.
        if angles is None:
            if pbc:
                from molsysmt.lib.structure.get_angles_cuda import (
                    get_mic_angles as _kernel,
                )

                angles = _kernel(coordinates, box, triplets)
            else:
                from molsysmt.lib.structure.get_angles_cuda import get_angles as _kernel

                angles = _kernel(coordinates, triplets)

        del (coordinates, box, triplets)

    # Fallback to CPU pipeline if GPU was not used
    if angles is None:
        if pbc:
            box = get(
                molecular_system,
                element="system",
                structure_indices=structure_indices,
                box=True,
            )
            if box is not None and box[0] is not None:
                box = np.asarray(
                    puw.get_value(box, to_unit=length_unit), dtype=np.float64
                )
                angles = _kernels.get_mic_angles(coordinates, box, triplets)
                del (coordinates, box, triplets)
            else:
                pbc = False
        if not pbc:
            angles = _kernels.get_angles(coordinates, triplets)
            del (coordinates, triplets)

    angles = puw.quantity(angles, "radians")
    angles = puw.standardize(angles)

    return angles
