from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt.dependencies import dep_digest

@arg_digest(form='file:dcd')
@dep_digest('mdtraj')
def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all:

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            output = output_filename

        else:

            output = item
    else:

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
                except:
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
                except:
                    stop_reading=True

                if xyz.size==0:
                    stop_reading=True

                if (not stop_reading):
                    output.write(xyz[atom_indices,:], cell_lengths, cell_angles)

            fff.close()
            output.close()

            del xyz, cell_lengths, cell_angles

    return output_filename

