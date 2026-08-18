from molsysmt._private.argdigest import arg_digest
import numpy as np

@arg_digest()
def add_contacts(view,
        selection=None, center_of_atoms=False, weights=None, structure_indices="all",
        selection_2=None, center_of_atoms_2=False, weights_2=None, structure_indices_2=None,
        threshold=None, pbc=False,
        atom_pairs=None,
        color='#808080', color_2=None, radius='0.1 angstroms',
        color_values=None, min_color_value=None, mid_color_value=None, max_color_value=None,
        color_values_scale='linear', colormap='bwr', color_values_2=None, min_color_value_2=None,
        mid_color_value_2=None, max_color_value_2=None,
        color_values_scale_2=None, colormap_2=None, syntax='MolSysMT',
        skip_digestion=False):
    """
    Adding visual contact lines or cylinders between atom pairs in NGLWidget.


    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer instance.
    selection : str, list, tuple, or numpy.ndarray, default=None
        Selection string or boolean/integer array specifying elements.
    center_of_atoms : bool, default=False
        Whether to compute distances relative to geometric centers.
    weights : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for center calculation.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    selection_2 : str, list, tuple, or numpy.ndarray, default=None
        Second selection string or boolean/integer array.
    center_of_atoms_2 : bool, default=False
        Whether to compute distances relative to geometric centers for selection_2.
    weights_2 : numpy.ndarray, list, or tuple, default=None
        Atomic mass weights array for selection_2.
    structure_indices_2 : int, list, tuple, or numpy.ndarray, default=None
        Structure indices (0-based) for the second selection.
    threshold : float or quantity, default=None
        Distance cutoff threshold quantity.
    pbc : bool, default=False
        Whether to take periodic boundary conditions into account.
    atom_pairs : numpy.ndarray, list, or tuple, default=None
        Explicit pairs of atom indices to visualize.
    color : object, default='#808080'
        Argument color.
    color_2 : object, default=None
        Secondary color string or RGB tuple.
    radius : object, default='0.1 angstroms'
        Argument radius.
    color_values : numpy.ndarray, list, or tuple, default=None
        Scalar numerical values used to color contacts.
    min_color_value : float or quantity, default=None
        Minimum value for contact colormap normalization.
    mid_color_value : float or quantity, default=None
        Midpoint value for contact colormap normalization.
    max_color_value : float or quantity, default=None
        Maximum value for contact colormap normalization.
    color_values_scale : str, default='linear'
        Scaling mode for contact colormap ('linear', 'log').
    colormap : str, default='bwr'
        Colormap name for contact coloring.
    color_values_2 : numpy.ndarray, list, or tuple, default=None
        Secondary scalar values array for coloring.
    min_color_value_2 : float or quantity, default=None
        Minimum value for secondary colormap.
    mid_color_value_2 : float or quantity, default=None
        Midpoint value for secondary colormap.
    max_color_value_2 : float or quantity, default=None
        Maximum value for secondary colormap.
    color_values_scale_2 : str, default=None
        Scaling mode for secondary colormap.
    colormap_2 : str, default=None
        Secondary colormap name.
    syntax : str, default='MolSysMT'
        Selection syntax used to evaluate `selection` (e.g., 'MolSysMT', 'MDTraj').
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, select
    from molsysmt.structure import get_contacts
    from . import add_cylinders

    if atom_pairs is None:

        atom_pairs = get_contacts(view, selection=selection, center_of_atoms=center_of_atoms,
                        weights=weights, structure_indices=structure_indices, selection_2=selection_2,
                        center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                        structure_indices_2=structure_indices_2, threshold=threshold, pbc=pbc,
                        output_type='pairs', output_indices='atom', syntax=syntax, skip_digestion=True)
        atom_pairs = np.array(atom_pairs[0])

    start = get(view, element='atom', selection=atom_pairs[:,0], coordinates=True)[0]
    end = get(view, element='atom', selection=atom_pairs[:,1], coordinates=True)[0]

    add_cylinders(view, start, end,
            color=color, color_2=color_2, radius=radius,
            color_values=color_values, min_color_value=min_color_value,
            mid_color_value=mid_color_value, max_color_value=max_color_value,
            color_values_scale=color_values_scale, colormap=colormap, color_values_2=color_values_2,
            min_color_value_2=min_color_value_2, mid_color_value_2=mid_color_value_2,
            max_color_value_2=max_color_value_2, color_values_scale_2=color_values_scale_2,
            colormap_2=colormap_2, skip_digestion=False)

    pass
