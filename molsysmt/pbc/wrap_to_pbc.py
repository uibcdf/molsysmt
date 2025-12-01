from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt import lib as msmlib
import numpy as np
import gc

@digest()
def wrap_to_pbc(molecular_system, selection='all', structure_indices='all',
                box_origin='[0,0,0] nanometers', box_center=None,
                center_of_selection=None, weights=None, center_coordinates='[0,0,0] nanometers',
                keep_covalent_bonds=False, syntax='MolSysMT', engine='MolSysMT', in_place=False,
                skip_digestion=False):
    """
    Wrap coordinates into the primary periodic box.

    Parameters
    ----------
    molecular_system : molecular system
        Input system.
    selection : str, list, tuple or numpy.ndarray, default 'all'
        Atoms to wrap.
    structure_indices : 'all' or array-like, default 'all'
        Structures/frames to process.
    box_origin : quantity, default '[0,0,0] nanometers'
        Origin of the periodic box.
    box_center : quantity, optional
        Center of the box; if provided, uses center-based wrapping.
    center_of_selection : str or array-like, optional
        Selection to center before wrapping (uses `center_coordinates`).
    weights : array-like, optional
        Weights for centering when `center_of_selection` is given.
    center_coordinates : quantity, default '[0,0,0] nanometers'
        Target coordinates for centering the `center_of_selection`.
    keep_covalent_bonds : bool, default False
        Placeholder (not implemented) to preserve covalent connectivity across PBC.
    syntax : str, default 'MolSysMT'
        Selection syntax for string selections.
    engine : {'MolSysMT'}, default 'MolSysMT'
        Backend.
    in_place : bool, default False
        If True, modify the input system; otherwise return a wrapped copy.
    skip_digestion : bool, default False
        Whether to skip argument digestion.

    Returns
    -------
    molecular system or None
        Wrapped system when `in_place=False`, otherwise `None`.

    Raises
    ------
    NotImplementedMethodError
        If an unsupported engine is requested.

    .. versionadded:: 1.0.0
    """

    if engine=='MolSysMT':

        from molsysmt.basic import select, get, set, extract, copy
        from molsysmt.structure import center

        atom_indices = select(molecular_system, selection=selection, syntax=syntax)

        if center_of_selection is not None:

            molecular_system = center(molecular_system, selection=atom_indices,
                                      center_of_selection=center_of_selection, weights=weights,
                                      center_coordinates=center_coordinates, syntax=syntax, in_place=False,
                                      skip_digestion=True)

        coordinates= get(molecular_system, element='atom', selection=atom_indices, structure_indices=structure_indices,
                         coordinates=True, skip_digestion=True)
        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True, skip_digestion=True)

        original_length_units = puw.get_unit(coordinates)
        coordinates, length_units = puw.get_value_and_unit(coordinates, standardized=True)
        box = puw.get_value(box, standardized=True)

        n_structures = coordinates.shape[0]
        if box.shape[0]==1 and n_structures>1:
            box = np.repeat(box, repeats=n_structures, axis=0)

        if box_center is None:

            box_origin = puw.get_value(box_origin, standardized=True)

            if np.all(np.isclose(box_origin, 0, atol=1e-4)):
                box_origin = np.zeros((3), dtype=np.float64)

            msmlib.pbc.wrap_to_pbc(coordinates, box, box_origin)

        else:

            box_center = puw.get_value(box_center, standardized=True)

            if np.all(np.isclose(box_center, 0, atol=1e-4)):
                box_origin = np.zeros((3), dtype=np.float64)

            msmlib.pbc.wrap_to_pbc_center(coordinates, box, box_center)


        coordinates=puw.quantity(coordinates, length_units)
        coordinates=puw.convert(coordinates, to_unit=original_length_units)

        del(box)

    else:

        raise NotImplementedMethodError()



    if in_place:

        set(molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        pass

    else:

        tmp_molecular_system = copy(molecular_system)
        set(tmp_molecular_system, selection='atom_index in @atom_indices', structure_indices=structure_indices,
            syntax=syntax, coordinates=coordinates)

        del(coordinates, atom_indices, structure_indices)

        gc.collect()

        return tmp_molecular_system
