from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all
from molsysmt._private.backend_output import silence_backend_stdout
from depdigest import dep_digest

@arg_digest(form='file:dcd')
@dep_digest('mdtraj')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True, skip_digestion=False):
    """
    Extracting a subset of elements or structures from form file:dcd.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    copy_if_all : object, default=True
        Argument copy_if_all.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:dcd
        Resulting object in file:dcd form.


    .. versionadded:: 1.0.0
    """

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            output = output_filename

        else:

            output = item
    else:

        from mdtraj.formats import DCDTrajectoryFile

        with silence_backend_stdout():
            output = DCDTrajectoryFile(str(output_filename), 'w')
            fff = DCDTrajectoryFile(str(item), 'r')

        atom_indices_is_all = is_all(atom_indices)

        if not is_all(structure_indices):

            stop_reading = False

            ii=-1

            while not stop_reading:

                try:
                    xyz, cell_lengths, cell_angles = fff.read(n_frames=1)
                    ii+=1
                except Exception:
                    stop_reading=True

                if xyz.size==0:
                    stop_reading=True

                if (not stop_reading) and (ii in structure_indices):
                    if atom_indices_is_all:
                        output.write(xyz, cell_lengths, cell_angles)
                    else:
                        output.write(xyz[:, atom_indices,:], cell_lengths, cell_angles)
                    structure_indices.remove(ii)

                if len(structure_indices)==0:
                    stop_reading=True

            fff.close()
            output.close()

            del xyz, cell_lengths, cell_angles

        else:

            stop_reading = False

            ii=-1

            while not stop_reading:

                try:
                    xyz, cell_lengths, cell_angles = fff.read(n_frames=1)
                    ii+=1
                except Exception:
                    stop_reading=True

                if xyz.size==0:
                    stop_reading=True

                if (not stop_reading):
                    output.write(xyz[atom_indices,:], cell_lengths, cell_angles)

            fff.close()
            output.close()

            del xyz, cell_lengths, cell_angles

    return output_filename

