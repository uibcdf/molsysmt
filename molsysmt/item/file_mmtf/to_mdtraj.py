"""mmtf.py: Used for loading mmtf files.
"""
##############################################################################
# MDTraj: A Python Library for Loading, Saving, and Manipulating
#         Molecular Dynamics Trajectories.
# Copyright 2012-2015 Stanford University and the Authors
#
# Authors: Diego Prada-Gracia
# Contributors:
#
# MDTraj is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 2.1
# of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with MDTraj. If not, see <http://www.gnu.org/licenses/>.
#
# Portions of this code originate from the OpenMM molecular simulation
# toolkit, copyright (c) 2012 Stanford University and the Authors. Those
# portions are distributed under the following terms:
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS, CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
# OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.
##############################################################################

##############################################################################
# Imports
##############################################################################

import copy
import os
import itertools
from re import sub, match, findall

import mdtraj as mdt
import mdtraj.core.element as mdt_element
from mdtraj.utils import in_units_of, cast_indices, ensure_type
import xml.etree.ElementTree as ETree
from mdtraj.formats.registry import FormatRegistry
from mmtf import parse
import numpy as np


##############################################################################
# Code
##############################################################################


@FormatRegistry.register_loader('.mmtf')
def load_mmtf(filename, stride=None, atom_indices=None, frame=None):
    """Load an MMTF file.

    Parameters
    ----------
    filename : str
        Path to the MMTF file on disk.
    stride : int, default=None
        Only read every stride-th model from the file
    atom_indices : array_like, optional
        If not none, then read only a subset of the atoms coordinates from the
        file. These indices are zero-based.
    frame : int, optional
        Use this option to load only a single model from a MMTF file on disk.
        If frame is None, the default, all models in file will be loaded.
        If supplied, ``stride`` will be ignored.
    """
    from mdtraj.core.trajectory import _parse_topology, Trajectory

    with MMTFTrajectoryFile(filename, 'r') as f:
        topology = f.topology
        # if frame is not None:
        #    f.seek(frame)
        #    n_structures = 1
        # else:
        #    n_structures = None
        return f.read_as_traj(n_structures=n_structures, stride=stride,
                              atom_indices=atom_indices)


@FormatRegistry.register_fileobject('.gro')
class MMTFTrajectoryFile(object):
    """Interface for reading and writing to MMTF files.

    Parameters
    ----------
    filename : str
        The filename to open. A path to a file on disk.
    mode : {'r', 'w'}
        The mode in which to open the file, either 'r' for read or 'w' for write.
    force_overwrite : bool
        If opened in write mode, and a file by the name of `filename` already
        exists on disk, should we overwrite it?

    Attributes
    ----------
    n_atoms : int
        The number of atoms in the file
    topology : mdtraj.Topology
        The topology. TODO(rmcgibbo) note about chain

    See Also
    --------
    """
    distance_unit = 'nanometers'
    _residue_name_replacements = {}
    _atom_name_replacements = {}
    _chain_names = [chr(ord('A') + i) for i in range(26)]

    def __init__(self, filename, mode='r', force_overwrite=True):
        self._open = False
        self._filepath = None
        self._mode = mode

        if mode == 'r':
            self._open = False
            self._frame_index = 0
            self._filepath = filename
            self.n_atoms, self.topology = self._read_topology(self._filepath)
            _residue_name_replacements, _atom_name_replacements = self._load_name_replacement_tables()
        elif mode == 'w':
            # self._open = True
            # if os.path.exists(filename) and not force_overwrite:
            #    raise IOError('"%s" already exists' % filename)
            # self._frame_index = 0
            # self._file = open(filename, 'w')
            raise NotImplementedError("Not implemented yet")
        else:
            raise ValueError("invalid mode: %s" % mode)

    # def write(self, coordinates, topology, time=None, unitcell_vectors=None,
    #          precision=3):
    #    """Write one or more frames of a molecular dynamics trajectory to disk
    #    in the GROMACS GRO format.

    #    Parameters
    #    ----------
    #    coordinates : np.ndarray, dtype=np.float32, shape=(n_structures, n_atoms, 3)
    #        The cartesian coordinates of each atom, in units of nanometers.
    #    topology : mdtraj.Topology
    #        The Topology defining the model to write.
    #    time : np.ndarray, dtype=float32, shape=(n_structures), optional
    #        The simulation time corresponding to each frame, in picoseconds.
    #        If not supplied, the numbers 0..n_structures will be written.
    #    unitcell_vectors : np.ndarray, dtype=float32, shape=(n_structures, 3, 3), optional
    #        The periodic box vectors of the simulation in each frame, in nanometers.
    #    precision : int, optional
    #        The number of decimal places to print for coordinates. Default is 3
    #    """
    #    if not self._open:
    #        raise ValueError('I/O operation on closed file')
    #    if not self._mode == 'w':
    #        raise ValueError('file not opened for writing')

    #    coordinates = ensure_type(coordinates, dtype=np.float32, ndim=3, name='coordinates', can_be_none=False, warn_on_cast=False)
    #    time = ensure_type(time, dtype=float, ndim=1, name='time', can_be_none=True, shape=(len(coordinates),), warn_on_cast=False)
    #    unitcell_vectors = ensure_type(unitcell_vectors, dtype=float, ndim=3, name='unitcell_vectors',
    #        can_be_none=True, shape=(len(coordinates), 3, 3), warn_on_cast=False)

    #    for i in range(coordinates.shape[0]):
    #        frame_time = None if time is None else time[i]
    #        frame_box = None if unitcell_vectors is None else unitcell_vectors[i]
    #        self._write_frame(coordinates[i], topology, frame_time, frame_box, precision)

    def read_as_traj(self, n_structures=None, stride=None, atom_indices=None):
        """Read a trajectory from a gro file

        Parameters
        ----------
        n_structures : int, optional
            If positive, then read only the next `n_structures` frames. Otherwise read all
            of the frames in the file.
        stride : np.ndarray, optional
            Read only every stride-th frame.
        atom_indices : array_like, optional
            If not none, then read only a subset of the atoms coordinates from the
            file. This may be slightly slower than the standard read because it required
            an extra copy, but will save memory.

        Returns
        -------
        trajectory : Trajectory
            A trajectory object containing the loaded portion of the file.
        """
        from mdtraj.core.trajectory import Trajectory
        topology = self.topology
        if atom_indices is not None:
            topology = topology.subset(atom_indices)

        coordinates, time, unitcell_vectors = self.read(stride=stride, atom_indices=atom_indices)
        if len(coordinates) == 0:
            return Trajectory(xyz=np.zeros((0, topology.n_atoms, 3)), topology=topology)

        coordinates = in_units_of(coordinates, self.distance_unit, Trajectory._distance_unit, inplace=True)
        unitcell_vectors = in_units_of(unitcell_vectors, self.distance_unit, Trajectory._distance_unit, inplace=True)

        traj = Trajectory(xyz=coordinates, topology=topology, time=time)
        traj.unitcell_vectors = unitcell_vectors
        return traj

    def read(self, n_structures=None, stride=None, atom_indices=None):
        """Read data from a molecular dynamics trajectory in the GROMACS GRO
        format.

        Parameters
        ----------
        n_structures : int, optional
            If n_structures is not None, the next n_structures of data from the file
            will be read. Otherwise, all of the frames in the file will be read.
        stride : int, optional
            If stride is not None, read only every stride-th frame from disk.
        atom_indices : np.ndarray, dtype=int, optional
            The specific indices of the atoms you'd like to retrieve. If not
            supplied, all of the atoms will be retrieved.

        Returns
        -------
        coordinates : np.ndarray, shape=(n_structures, n_atoms, 3)
            The cartesian coordinates of the atoms, in units of nanometers.
        time : np.ndarray, None
            The time corresponding to each frame, in units of picoseconds, or
            None if no time information is present in the trajectory.
        unit_cell_vectors : np.ndarray, shape=(n_structures, 3, 3)
            The box vectors in each frame, in units of nanometers
        """
        if not self._open:
            raise ValueError('I/O operation on closed file')
        if not self._mode == 'r':
            raise ValueError('file not opened for reading')

        coordinates = []
        unit_cell_vectors = []
        time = []
        contains_time = True

        atom_indices = cast_indices(atom_indices)
        atom_slice = slice(None) if atom_indices is None else atom_indices

        if n_structures is None:
            frameiter = itertools.count()
        else:
            frameiter = range(n_structures)

        for i in frameiter:
            try:
                frame_xyz, frame_box, frame_time = self._read_frame()
                contains_time = contains_time and (frame_time is not None)
                coordinates.append(frame_xyz[atom_slice])
                unit_cell_vectors.append(frame_box)
                time.append(frame_time)
            except StopIteration:
                break

        coordinates, unit_cell_vectors, time = map(np.array,
                                                   (coordinates,
                                                    unit_cell_vectors,
                                                    time))

        if not contains_time:
            time = None
        else:
            time = time[::stride]

        return coordinates[::stride], time, unit_cell_vectors[::stride]

    @staticmethod
    def _load_name_replacement_tables():
        """ Load the list of atom and residue name replacements.

            Returns
            -------

            atom_name_replacements : Dict[str, Dict[str, str]]
                This is a map from residue names to a dictionary that maps
                pdb atom names to mdtraj atom names.

            residue_name_replacements : Dict[str, str]
                This is a dictionary that maps pdb residue names to mdtraj
                residue names.
        """
        residue_name_replacements = {}
        atom_name_replacements = {}

        tree = ETree.parse(os.path.join(os.path.dirname(__file__), 'data', 'pdbNames.xml'))
        all_residues = {}
        protein_residues = {}
        nucleic_acid_residues = {}
        for residue in tree.getroot().findall('Residue'):
            name = residue.attrib['name']
            if name == 'All':
                MMTFTrajectoryFile.parse_residue_atoms(residue, all_residues)
            elif name == 'Protein':
                MMTFTrajectoryFile.parse_residue_atoms(residue, protein_residues)
            elif name == 'Nucleic':
                MMTFTrajectoryFile.parse_residue_atoms(residue, nucleic_acid_residues)
        for atom in all_residues:
            protein_residues[atom] = all_residues[atom]
            nucleic_acid_residues[atom] = all_residues[atom]
        for residue in tree.getroot().findall('Residue'):
            name = residue.attrib['name']
            for id_ in residue.attrib:
                if id_ == 'name' or id_.startswith('alt'):
                    residue_name_replacements[residue.attrib[id_]] = name
            if 'type' not in residue.attrib:
                atoms = copy.copy(all_residues)
            elif residue.attrib['type'] == 'Protein':
                atoms = copy.copy(protein_residues)
            elif residue.attrib['type'] == 'Nucleic':
                atoms = copy.copy(nucleic_acid_residues)
            else:
                atoms = copy.copy(all_residues)

            MMTFTrajectoryFile.parse_residue_atoms(residue, atoms)
            atom_name_replacements[name] = atoms

        return residue_name_replacements, atom_name_replacements

    @staticmethod
    def parse_residue_atoms(residue, dictionary):
        for atom in residue.findall('Atom'):
            name = atom.attrib['name']
            for id_ in atom.attrib:
                dictionary[atom.attrib[id_]] = name

    @staticmethod
    def _read_topology(file_path):
        """ Reads the topology of the mmtf file. It returns
            a 2-tuple where the first element is the number of atoms
            and the second is the topology.

            Parameters
            ----------
            file_path : str
                Path to the mmft file.

            Returns
            -------
            n_atoms : int
                Number of atoms in the system.

            topology : mdtraj.Topology
                The topology of the system.

        """
        if not len(MMTFTrajectoryFile._residue_name_replacements):
            MMTFTrajectoryFile._residue_name_replacements, MMTFTrajectoryFile._atom_name_replacements = \
                MMTFTrajectoryFile._load_name_replacement_tables()

        decoder = parse(file_path)

        n_atoms = decoder.num_atoms
        topology = mdt.Topology()

        # mmtf follows the following structure hierarchy:
        # Models -> Chains -> Groups -> Atoms
        # mdtraj has the following hierarchy:
        # Chains -> Residues -> Atoms
        # Residues are equivalent to Groups.
        model_index = 0
        atom_index = 0
        chain_index = 0
        group_index = 0

        for model_chain_count in decoder.chains_per_model:
            for chain in range(model_chain_count):
                # Number of groups per chain
                chain_group_count = decoder.groups_per_chain[chain_index]
                chain = topology.add_chain()
                for ii in range(chain_group_count):
                    group = decoder.group_list[decoder.group_type_list[group_index]]
                    group_name = group["groupName"]
                    # Get the residue name for mdtraj
                    try:
                        residue_name = MMTFTrajectoryFile._residue_name_replacements[group_name]
                    except KeyError:
                        residue_name = group_name
                    residue = topology.add_residue(name=residue_name,
                                                   chain=chain,
                                                   resSeq=decoder.sequence_index_list[group_index])

                    atom_offset = atom_index  # To retrieve bonds later
                    group_atom_count = len(group["atomNameList"])
                    for jj in range(group_atom_count):
                        atom_name = group["atomNameList"][jj]
                        element_symbol = group["elementList"][jj]
                        element = mdt_element.get_by_symbol(element_symbol)
                        try:
                            atom_name = MMTFTrajectoryFile._atom_name_replacements[residue_name][atom_name]
                        except KeyError:
                            pass

                        topology.add_atom(name=atom_name,
                                          element=element,
                                          residue=residue)
                        atom_index += 1

                    group_bond_count = int(len(group["bondAtomList"]) / 2)
                    # Traverse bonds between atoms inside groups
                    for kk in range(group_bond_count):
                        atom_1_index = atom_offset + group["bondAtomList"][kk * 2]
                        atom_2_index = atom_offset + group["bondAtomList"][kk * 2 + 1]
                        topology.add_bond(topology.atom(atom_1_index),
                                          topology.atom(atom_2_index),
                                          order=group["bondOrderList"][kk]
                                          )

                    group_index += 1
                chain_index += 1
            model_index += 1

        # Add inter bond groups
        for ii in range(int(len(decoder.bond_atom_list) / 2)):
            topology.add_bond(
                topology.atom(ii * 2),
                topology.atom(ii * 2 + 1),
                order=decoder.bond_order_list[ii]
            )

        return n_atoms, topology

    def _read_frame(self):
        """ Reads a gro file and returns the atoms coordinates,
            the unit cell vectors and time.

            Returns
            -------
            xyz: np.ndarray of shape(n_atoms, 3)
                The coordinates of the atoms.

            unit_cell_vectors: np.ndarray of shape(3, 3)
                THe unit cell vectors.

            time: float or None
                The time specified in the file. Null if there isn't a time
                in the file.
        """
        if not self._open:
            raise ValueError('I/O operation on closed file')
        if not self._mode == 'r':
            raise ValueError('file not opened for reading')

        atom_counter = itertools.count()
        comment = None
        box_vectors = None
        xyz = np.zeros((self.n_atoms, 3), dtype=np.float32)

        got_line = False
        first_decimal_pos = None
        atom_index = -1
        for ln, line in enumerate(self._file):
            got_line = True
            if ln == 0:
                comment = line.strip()
                continue
            elif ln == 1:
                assert self.n_atoms == int(line.strip())
                continue
            if first_decimal_pos is None:
                try:
                    first_decimal_pos = line.index('.', 20)
                    second_decimal_pos = line.index('.', first_decimal_pos + 1)
                except ValueError:
                    first_decimal_pos = None
                    second_decimal_pos = None
            crd = _parse_gro_coord(line, first_decimal_pos, second_decimal_pos)
            if crd is not None and atom_index < self.n_atoms - 1:
                atom_index = next(atom_counter)
                xyz[atom_index, :] = (crd[0], crd[1], crd[2])
            elif _is_gro_box(line) and ln == self.n_atoms + 2:
                split_line = line.split()
                box_vectors = tuple([float(i) for i in split_line])
                # the gro_box line comes at the end of the record
                break
            else:
                raise Exception("Unexpected line in .gro file: " + line)

        if not got_line:
            raise StopIteration()

        time = None
        if 't=' in comment:
            # title string (free format string, optional time in ps after 't=')
            time = float(findall(r't= *(\d+\.\d+)', comment)[-1])

        # box vectors (free format, space separated reals), values: v1(x) v2(y)
        # v3(z) v1(y) v1(z) v2(x) v2(z) v3(x) v3(y), the last 6 values may be
        # omitted (they will be set to zero).
        box = [box_vectors[i] if i < len(box_vectors) else 0 for i in range(9)]
        unit_cell_vectors = np.array([
            [box[0], box[3], box[4]],
            [box[5], box[1], box[6]],
            [box[7], box[8], box[2]]])

        return xyz, unit_cell_vectors, time

    def _write_frame(self, coordinates, topology, time, box, precision):
        comment = 'Generated with MDTraj'
        if time is not None:
            comment += ', t= %s' % time

        var_width = precision + 5
        fmt = '%%5d%%-5s%%5s%%5d%%%d.%df%%%d.%df%%%d.%df' % (
            var_width, precision, var_width, precision, var_width, precision)
        assert topology.n_atoms == coordinates.shape[0]
        lines = [comment, ' %d' % topology.n_atoms]
        if box is None:
            box = np.zeros((3, 3))

        for i in range(topology.n_atoms):
            atom = topology.atom(i)
            residue = atom.residue
            serial = atom.serial
            if serial is None:
                serial = atom.index
            if serial >= 100000:
                serial -= 100000
            lines.append(fmt % (residue.resSeq, residue.name, atom.name, serial,
                                coordinates[i, 0], coordinates[i, 1], coordinates[i, 2]))

        lines.append('%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f%10.5f' % (
            box[0, 0], box[1, 1], box[2, 2],
            box[0, 1], box[0, 2], box[1, 0],
            box[1, 2], box[2, 0], box[2, 1]))

        self._file.write('\n'.join(lines))
        self._file.write('\n')

    def seek(self, offset, whence=0):
        """Move to a new file position

        Parameters
        ----------
        offset : int
            A number of frames.
        whence : {0, 1, 2}
            0: offset from start of file, offset should be >=0.
            1: move relative to the current position, positive or negative
            2: move relative to the end of file, offset should be <= 0.
            Seeking beyond the end of a file is not supported
        """
        raise NotImplementedError()

    def tell(self):
        """Current file position

        Returns
        -------
        offset : int
            The current frame in the file.
        """
        return self._frame_index

    def close(self):
        """Close the file"""
        if self._open:
            self._file.close()
            self._open = False

    def __enter__(self):
        """Support the context manager protocol"""
        return self

    def __exit__(self, *exc_info):
        """Support the context manager protocol"""
        self.close()


##############################################################################
# Utilities
##############################################################################


def _isint(word):
    """ONLY matches integers! If you have a decimal point? None shall pass!

    @param[in] word String (for instance, '123', '153.0', '2.', '-354')
    @return answer Boolean which specifies whether the string is an integer (only +/- sign followed by digits)

    """
    return match(r'^[-+]?\d+$', word)


def _isfloat(word):
    """Matches ANY number; it can be a decimal, scientific notation, what have you
    CAUTION - this will also match an integer.

    @param[in] word String (for instance, '123', '153.0', '2.', '-354')
    @return answer Boolean which specifies whether the string is any number

    """
    return match(r'^[-+]?\d*\.?\d*([eEdD][-+]?\d+)?$', word)


def _parse_gro_coord(line, first_decimal, second_decimal):
    """ Determines whether a line contains GROMACS data or not

    @param[in] line The line to be tested

    """
    if first_decimal is None or second_decimal is None:
        return None
    digits = second_decimal - first_decimal
    try:
        return tuple(float(line[20 + i * digits:20 + (i + 1) * digits]) for i in range(3))
    except ValueError:
        return None


def _is_gro_box(line):
    """ Determines whether a line contains a GROMACS box vector or not

    @param[in] line The line to be tested

    """
    split_line = line.split()
    if len(split_line) == 9 and all([_isfloat(i) for i in split_line]):
        return True
    elif len(split_line) == 3 and all([_isfloat(i) for i in split_line]):
        return True
    else:
        return False
