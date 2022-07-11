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
import xml.etree.ElementTree as ETree
import mdtraj as mdt
import mdtraj.core.element as mdt_element
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
    with MMTFTrajectoryFile(filename, 'r') as fh:
        # time = np.arange(len(fh.positions))
        return mdt.Trajectory(
            xyz=fh.positions,
            topology=fh.topology,
            # time=time,
            unitcell_lengths=fh.unit_cell_lengths,
            unitcell_angles=fh.unit_cell_angles,
        )


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

    """
    distance_unit = 'nanometers'
    _residue_name_replacements = {}
    _atom_name_replacements = {}
    _chain_names = [chr(ord('A') + i) for i in range(26)]

    def __init__(self, filename, mode='r', force_overwrite=True, standard_names=True):
        self._open = False
        self._filepath = None
        self._mode = mode
        self._standard_names = True
        self._positions = None
        self._topology = None
        self._unit_cell_lengths = None
        self._unit_cell_angles = None

        if mode == 'r':
            _residue_name_replacements, _atom_name_replacements = self._load_name_replacement_tables()
            self._frame_index = 0
            self._filepath = filename
            self.n_atoms, self._topology = self._read_topology(self._filepath)
            self._positions = np.zeros((1, self.n_atoms, 3))

        elif mode == 'w':
            self._open = True
            if os.path.exists(filename) and not force_overwrite:
                raise IOError('"%s" already exists' % filename)
        else:
            raise ValueError("invalid mode: %s" % mode)

        self._open = True

    @property
    def positions(self):
        """ Returns the cartesian coordinates of the atoms if mode='r'. If mode='w' returns
            none.
        """
        return self._positions

    @property
    def topology(self):
        """ Returns the topology of the mmtf file if mode='r'. If mode='w' returns
            none.
        """
        return self._topology

    @property
    def unit_cell_lengths(self):
        """ Returns the unit cell lengths of the mmtf file if mode='r'. If mode='w' returns
            none.
        """
        return self._unit_cell_lengths

    @property
    def unit_cell_angles(self):
        """ Returns the unit cell angles of the mmtf file if mode='r'. If mode='w' returns
            none.
        """
        return self._unit_cell_angles

    @property
    def closed(self):
        """ Whether the file is closed. """
        return not self._open

    def write(self):
        """ Write a mmtf file to disk
        """
        if not self._open:
            raise ValueError('I/O operation on closed file')
        if not self._mode == 'w':
            raise ValueError('file not opened for writing')

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

    def close(self):
        """Close the file"""
        self._open = not self._open

    def __enter__(self):
        """Support the context manager protocol"""
        return self

    def __exit__(self, *exc_info):
        """Support the context manager protocol"""
        self.close()
