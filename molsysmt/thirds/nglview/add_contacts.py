from molsysmt._private.digestion import digest
import numpy as np


#@digest()
def add_contacts(view, contacts, selection=None, selection_2=None, input_indices='atom_index',
        color='#808080', color_2=None, radius='0.1 angstroms',
        color_values=None, min_color_value=None, mid_color_value=None, max_color_value=None,
        color_values_scale='linear', colormap='bwr', color_values_2=None, min_color_value_2=None,
        mid_color_value_2=None, max_color_value_2=None, center_color_value_2=None,
        color_values_scale_2=None, colormap_2=None, syntax='MolSysMT'):

    from molsysmt.basic import get, select
    from . import add_cylinders

    if isinstance(contacts, np.ndarray):
        if contacts.dtype == bool:

            pairs = np.nonzero(np.triu(contacts,k=1)==True)
            pairs = np.column_stack(pairs)

            atom_indices = select(view, selection=selection, syntax=syntax)

            if selection_2 is None:
                pairs=atom_indices[pairs]
            else:
                atom_indices_2 = select(view, selection=selection_2, syntax=syntax)
                pairs=np.column_stack(atom_indices[pairs[:,0]],
                            atom_indices_2[pairs[:,1]])
        else:
            pairs=contacts
    else:
        pairs=contacts

    start = get(view, element='atom', selection=pairs[:,0], coordinates=True)[0]
    end = get(view, element='atom', selection=pairs[:,1], coordinates=True)[0]

    add_cylinders(view, start, end,
            color=color, color_2=color_2, radius=radius,
            color_values=color_values, min_color_value=min_color_value,
            mid_color_value=mid_color_value, max_color_value=max_color_value,
            color_values_scale=color_values_scale, colormap=colormap, color_values_2=color_values_2,
            min_color_value_2=min_color_value_2, mid_color_value_2=mid_color_value_2,
            max_color_value_2=max_color_value_2, center_color_value_2=center_color_value_2,
            color_values_scale_2=color_values_scale_2, colormap_2=colormap_2)

    pass

