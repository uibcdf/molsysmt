from molsysmt._private.argdigest import arg_digest
import numpy as np


#@arg_digest()
def add_hbonds(view, hbonds, selection=None, selection_2=None, hbond_level='atom',
        color='#FFC300', radius='0.1 angstroms', syntax='MolSysMT'):
    """
    Adding hydrogen bond interaction cylinders in NGLWidget.

    Parameters
    ----------
    view : nglview.NGLWidget
        Target molecular viewer.
    hbonds : list of tuple or numpy.ndarray
        Donor-acceptor or donor-hydrogen-acceptor atom index tuples.
    color : str, default='blue'
        Color for hydrogen bond visualization cylinders.
    radius : float, default=0.05
        Cylinder radius in nanometers.

    .. versionadded:: 1.0.0
    """

    from molsysmt.basic import get, select
    from . import add_cylinders

    if hbond_level=='atom':

        start = get(view, element='atom', selection=hbonds[:,1], coordinates=True)[0]
        end = get(view, element='atom', selection=hbonds[:,2], coordinates=True)[0]

        add_cylinders(view, start, end, color=color, color_2=color, radius=radius)
        pass

    elif hbond_level=='group':

        atom_group_indices = np.asarray(
            get(view, element='atom', selection='all', group_index=True)
        )
        group_indices, CA_indices = get(
            view,
            element='atom',
            selection='atom_name=="CA"',
            group_index=True,
            atom_index=True,
        )
        ca_by_group = {
            group_index: atom_index
            for group_index, atom_index in zip(group_indices, CA_indices)
        }
        ca_start = [
            ca_by_group[group_index]
            for group_index in atom_group_indices[hbonds[:, 1]]
        ]
        ca_end = [
            ca_by_group[group_index]
            for group_index in atom_group_indices[hbonds[:, 2]]
        ]
        coordinates = get(
            view,
            element='atom',
            selection='all',
            coordinates=True,
        )[0]
        start = coordinates[ca_start]
        end = coordinates[ca_end]

        add_cylinders(view, start, end, color=color, color_2=color, radius=radius)
        pass
