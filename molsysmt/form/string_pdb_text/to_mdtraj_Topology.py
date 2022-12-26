from molsysmt._private.exceptions import LibraryNotFoundError
from molsysmt._private.digestion import digest

@digest(form='string:pdb_text')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', digest=True):

    try:
        from mdtraj import load_topology as mdtraj_load_topology
    except:
        raise LibraryNotFoundError('MDTraj')

    from io import StringIO
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, digest=False)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = mdtraj_load_topology(tmp_io)

    return tmp_item

