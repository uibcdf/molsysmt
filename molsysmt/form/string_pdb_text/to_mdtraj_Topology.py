from molsysmt._private.digestion import digest
from molsysmt.dependencies import requires

@digest(form='string:pdb_text')
@requires('MDTraj')
def to_mdtraj_Topology(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from mdtraj import load_topology as mdtraj_load_topology

    from io import StringIO
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices, skip_digestion=True)

    tmp_io = StringIO()
    tmp_io.write(tmp_item)
    tmp_io.close()

    tmp_item = mdtraj_load_topology(tmp_io)

    return tmp_item

