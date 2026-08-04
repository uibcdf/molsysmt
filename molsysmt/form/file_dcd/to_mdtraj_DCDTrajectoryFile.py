from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.files_and_directories import str_filename
from depdigest import dep_digest

@arg_digest(form='file:dcd')
@dep_digest('mdtraj')
def to_mdtraj_DCDTrajectoryFile(item, atom_indices='all', structure_indices='all', skip_digestion=False):

    from mdtraj.formats import DCDTrajectoryFile
    from molsysmt._private.backend_output import silence_backend_stdout
    from ..mdtraj_DCDTrajectoryFile.extract import extract as extract_mdtraj_DCDTrajectoryFile

    # MDTraj announces the detected DCD variant on stdout with no way to turn it off.
    with silence_backend_stdout():
        tmp_item = DCDTrajectoryFile(str_filename(item))
    tmp_item = extract_mdtraj_DCDTrajectoryFile(tmp_item, atom_indices=atom_indices,
                                                structure_indices=structure_indices,
                                                copy_if_all=False, skip_digestion=True)

    return tmp_item
