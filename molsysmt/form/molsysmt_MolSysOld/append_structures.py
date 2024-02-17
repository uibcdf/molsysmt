from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.MolSysOld')
def append_structures(item, structure_id=None, time=None, coordinates=None, velocities=None,
        box=None, skip_digestion=True):

    item.structures.append_structures(structure_id=structure_id, time=time, coordinates=coordinates,
            velocities=velocities, box=box)

    pass

