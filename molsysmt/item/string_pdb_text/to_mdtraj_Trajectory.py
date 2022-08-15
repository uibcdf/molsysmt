from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_mdtraj_Trajectory(item, atom_indices='all', structure_indices='all'):

    try:
        from mdtraj import load_pdb as mdtraj_pdb_loader
    except:
        raise LibraryNotFoundError('MDTraj')

    from io import StringIO
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = mdtraj_pdb_loader(tmp_io)

    return tmp_item

