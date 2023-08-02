from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from matplotlib.colors import to_rgb
import numpy as np
from molsysmt import pyunitwizard as puw

# https://github.com/arose/ngl/blob/master/doc/usage/selection-language.md

#@digest()
def add_hbonds(view, hbonds, color='#d6c20f', radius='0.2 angstroms', representation='wideline'):

    hbonds=hbonds[0]

    from molsysmt import get

    if isinstance(color, str):

        color=to_rgb(color)

    atom_indices = np.unique(hbonds[:,1:])
    aux_dict = {jj:ii for ii,jj in enumerate(atom_indices)}
    coordinates = get(view, element='atom', selection=atom_indices, coordinates=True)

    ngl_coordinates = puw.get_value(coordinates[0], to_unit='angstroms')
    ngl_radius = puw.get_value(radius, to_unit='angstroms')

    print(ngl_coordinates)

    n_hbonds = hbonds.shape[0]

    if representation=='wideline':

        # view: github:nglviewer/ngl/:/src/buffer/wideline-buffer.ts

        for ii in range(n_hbonds):

            atom1 = hbonds[ii,1]
            atom2 = hbonds[ii,2]

            kwargs = {'position1':ngl_coordinates[aux_dict[atom1]].tolist(),
                      'position2':ngl_coordinates[aux_dict[atom2]].tolist(),
                      'color': color,
                      }

            msg = view._get_remote_call_msg("addBuffer",
                                        target="Widget",
                                        args=["wideline"],
                                        kwargs=kwargs,
                                        fire_embed=True)

            def callback(widget, msg=msg):
                widget.send(msg)

            callback._method_name = 'addBuffer'
            callback._ngl_msg = msg

            view._ngl_displayed_callbacks_before_loaded.append(callback)

            view._ngl_msg_archive.append(msg)

    pass

