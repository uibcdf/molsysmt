from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw

@arg_digest(form='mdtraj.XTCTrajectoryFile')
def to_molsysmt_Structures(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from molsysmt.native import Structures
    tmp_item = Structures()

    position = item.tell()
    try:
        item.seek(0)
        payload = item.read(
            atom_indices=atom_indices if not is_all(atom_indices) else None
        )
    finally:
        item.seek(position)

    coordinates = payload[0]
    time = payload[1]
    box = payload[3]
    if not is_all(structure_indices):
        coordinates = coordinates[structure_indices]
        if time is not None:
            time = time[structure_indices]
        if box is not None:
            box = box[structure_indices]

    coordinates = coordinates * puw.unit('nanometer')
    time = None if time is None else time * puw.unit('picosecond')
    box = None if box is None or len(box) == 0 else box * puw.unit('nanometer')

    tmp_item.append(structure_id=None, time=time, box=box, coordinates=coordinates)

    return tmp_item
