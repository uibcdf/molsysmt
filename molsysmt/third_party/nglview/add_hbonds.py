from molsysmt._private.arg_digestion import arg_digest
import numpy as np


#@arg_digest()
def add_hbonds(view, hbonds, selection=None, selection_2=None, hbond_level='atom',
        color='#FFC300', radius='0.1 angstroms', syntax='MolSysMT'):
    """Render hydrogen bonds as cylinders on an NGLview widget."""

    from molsysmt.basic import get, select
    from . import add_cylinders

    if hbond_level=='atom':

        start = get(view, element='atom', selection=hbonds[:,1], coordinates=True)[0]
        end = get(view, element='atom', selection=hbonds[:,2], coordinates=True)[0]

        add_cylinders(view, start, end, color=color, color_2=color, radius=radius)
        pass

    elif hbond_level=='group':

        group_indices, CA_indices = get(view, element='atom', selection='atom_name=="CA"', group_index=True,
                                        atom_index=True)
        aux_dict = { ii:jj for ii,jj in zip(group_indices, CA_indices) }

        group_indices_start = get(view, element='atom', selection=hbonds[:,1], group_index=True)
        CAs_start = [aux_dict[ii] for ii in group_indices_start]
        start = get(view, element='atom', selection=CAs_start, coordinates=True)[0]

        group_indices_end = get(view, element='atom', selection=hbonds[:,2], group_index=True)
        CAs_end = [aux_dict[ii] for ii in group_indices_end]
        end = get(view, element='atom', selection=CAs_end, coordinates=True)[0]

        add_cylinders(view, start, end, color=color, color_2=color, radius=radius)
        pass
