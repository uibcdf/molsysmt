from molsysmt._private.digestion import digest

@digest(form='file:gro')
def to_mdtraj_GroTrajectoryFile(item, atom_indices='all', structure_indices='all', digest=True):

    from mdtraj.formats import GroTrajectoryFile
    from . import extract

    tmp_item = extract(item, atom_indices=atom_indices, structure_indices=structure_indices,
            copy_if_all=False, digest=False)
    tmp_item = GromacsGroFile(tmp_item)

    return tmp_item

