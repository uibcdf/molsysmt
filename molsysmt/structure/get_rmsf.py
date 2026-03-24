from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt.lib.structure._kernel_inputs import extract_coordinates_value_and_unit
from smonitor import signal
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


@signal(tags=['api', 'structure'])
@arg_digest()
def get_rmsf(molecular_system, selection='atom_type!="H"', structure_indices='all',
             syntax='MolSysMT', engine='MolSysMT'):
    """
    Root-mean-square fluctuation (RMSF) per atom over a set of structures.

    The RMSF of atom *i* is defined as:

    .. math::

        \\mathrm{RMSF}_i = \\sqrt{\\frac{1}{T} \\sum_{t=1}^{T}
        \\left| \\mathbf{r}_i(t) - \\langle \\mathbf{r}_i \\rangle \\right|^2}

    where :math:`\\langle \\mathbf{r}_i \\rangle` is the time-averaged position of atom *i*
    and *T* is the number of structures.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    selection : str, list, tuple or numpy.ndarray, default 'atom_type!="H"'
        Atom selection for which RMSF is computed.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend used for the computation.

    Returns
    -------
    quantity
        RMSF per selected atom as a PyUnitWizard quantity in length units.
        Shape: (n_atoms,).

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    Notes
    -----
    All structures must be pre-aligned to a common reference frame before calling
    this function if positional fluctuations relative to a reference are intended.
    Use :func:`molsysmt.structure.least_rmsd_align` to align first.

    .. versionadded:: 1.0.0
    """

    if engine == 'MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt import lib as msmlib

        coordinates = get(molecular_system, element='atom', selection=selection,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)
        coordinates, length_unit = extract_coordinates_value_and_unit(coordinates)

        rmsf_val = msmlib.structure.get_rmsf(coordinates)
        rmsf = puw.quantity(rmsf_val, length_unit)
        rmsf = puw.standardize(rmsf)

        del coordinates, length_unit
        gc.collect()

        return rmsf

    else:

        raise NotImplementedMethodError()
