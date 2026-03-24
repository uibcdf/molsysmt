from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from smonitor import signal
from molsysmt import pyunitwizard as puw
import numpy as np


@signal(tags=['api', 'physchem'])
@arg_digest()
def get_sasa(molecular_system, element='atom', selection='all', structure_indices='all',
             syntax='MolSysMT', engine='MDTraj'):
    """
    Solvent-accessible surface area (SASA) per atom or residue group.

    Uses the Shrake–Rupley rolling-sphere algorithm.  The default engine
    delegates to :func:`mdtraj.shrake_rupley`.

    Parameters
    ----------
    molecular_system : molecular system
        Input system in any supported form.
    element : {'atom', 'group', 'component', 'molecule', 'chain', 'entity'}, default 'atom'
        Hierarchical element over which SASA is accumulated.
        When ``element='atom'``, the raw per-atom SASA is returned.
        For any other element, per-atom values are summed within each element.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Selection of elements to return.  The full system is always used for
        the SASA calculation; this parameter only filters the output.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to include.
    syntax : str, default 'MolSysMT'
        Selection syntax.
    engine : {'MDTraj'}, default 'MDTraj'
        Backend used for the SASA calculation.

    Returns
    -------
    quantity
        SASA values as a PyUnitWizard quantity in area units (nm²).
        Shape: ``(n_structures, n_elements)``.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    Notes
    -----
    Non-protein atoms (e.g. solvent) are included in the SASA calculation
    but their contribution to neighbouring atoms is accounted for.

    .. versionadded:: 1.0.0
    """

    if engine == 'MDTraj':

        from mdtraj import shrake_rupley
        from molsysmt.basic import convert, select, get

        tmp_item = convert(molecular_system, to_form='mdtraj.Trajectory',
                           structure_indices=structure_indices)

        sasa_array = shrake_rupley(tmp_item, mode='atom')

        if element == 'atom':

            if not is_all(selection):
                atom_indices = select(molecular_system, selection=selection, syntax=syntax)
                sasa_array = sasa_array[:, atom_indices]

        else:

            sets_atoms = get(molecular_system, element=element, selection=selection,
                             syntax=syntax, atom_index=True)

            n_sets = len(sets_atoms)
            n_structures = sasa_array.shape[0]

            new_sasa_array = np.empty([n_structures, n_sets], dtype='float')
            for ii in range(n_sets):
                new_sasa_array[:, ii] = sasa_array[:, sets_atoms[ii]].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = puw.quantity(sasa_array, 'nm**2')
        sasa_array = puw.standardize(sasa_array)

    else:

        raise NotImplementedMethodError()

    return sasa_array
