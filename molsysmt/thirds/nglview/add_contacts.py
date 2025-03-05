from molsysmt._private.digestion import digest
import numpy as np

@digest()
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

