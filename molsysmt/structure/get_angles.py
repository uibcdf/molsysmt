import numpy as np
from molsysmt import pyunitwizard as puw
from smonitor import signal
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private import rust_backend as _kernels
from molsysmt.configure import with_configure_overrides
import gc


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
    """
    Calculating bond angles for given atom triplets.

    Parameters
    ----------
    molecular_system : molecular system
        System providing coordinates.
    triplets : numpy.ndarray
        Array of shape (n_triplets, 3) with atom indices defining each angle.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to compute over.
    pbc : bool, default False
        Whether to apply minimum image convention using the box.
    use_gpu : bool or 'auto' or None, default None
        Whether to run calculation on GPU.
    gpu_backend : {'cuda', 'taichi'} or None, default None
        The preferred GPU framework to execute calculations on.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    quantity
        Angles in radians as a PyUnitWizard quantity.
    """

    from molsysmt.basic import get
    from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
    from molsysmt._private.gpu import resolve_use_gpu
    import molsysmt.configure as config

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
                import taichi

                taichi_available = True
            except ImportError:
                taichi_available = False
                import warnings
                from molsysmt._private.smonitor import GpuNotAvailableWarning

                warnings.warn(
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

    gc.collect()

    return angles
