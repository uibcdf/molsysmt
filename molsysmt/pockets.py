from ._private_tools.engines import digest_engine
from ._private_tools.frame_indices import digest_frame_indices

def alpha_spheres(item, selection='all', frame_indices='all', syntaxis='MDTraj',
                  engine='OpenPocket'):

    engine = _digest_engines(engine)

    if engine=='OpenPocket':

        from openpocket import alpha_spheres as op_alpha_spheres
        from molsysmt import convert, select, get

        atom_indices_1 = select(item, selection=selection, syntaxis=syntaxis)
        coordinates = coordinates_1 = get(item_1, target='atom', indices=atom_indices_1,
                frame_indices=frame_indices_1, coordinates=True)

        return op_alpha_spheres

    else:

        raise NotImplementedError(NotImplementedMessage)


