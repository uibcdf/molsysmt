from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.pbc import get_box_from_lengths_and_angles
from copy import copy
import numpy as np
from molsysmt._private.digestion import digest
from molsysmt._private.indices import indices_iterator

class StructuresIterator():

    @digest(form='mdtraj.DCDTrajectoryFile')
    def __init__(self, molecular_system, atom_indices='all', start=0, stop=None, step=1, chunk=1,
            structure_indices=None, output_type = 'values', **kwargs):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.structure_index = None

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)
                self._output_dictionary[key] = None


        if is_all(structure_indices):
            structure_indices=None

        if self.stop is None:
            if structure_indices is None:
                from .get import get_n_structures_from_system
                self.stop = get_n_structures_from_system(molecular_system)
            else:
                self.stop = len(structure_indices)

        self._indices_iterator = indices_iterator(indices=structure_indices, start=self.start,
                stop=self.stop, step=self.step, chunk=self.chunk)

        self._mdtraj_atom_indices = self.atom_indices
        if is_all(self.atom_indices):
            self._mdtraj_atom_indices = None

    def __iter__(self):

        return self

    def __next__(self):

        indices = self._indices_iterator.__next__()

        if indices is not None:

            coordinates = []
            box_lengths = []
            box_angles = []
            if isinstance(indices, (list,tuple)):

                for ii in indices:
                    self.molecular_system.seek(indices)
                    coordinates_aux, box_lengths_aux, box_angles_aux = self.molecular_system.read(1, 0, self._mdtraj_atom_indices)
                    coordinates.append(coordinates_aux)
                    box_lengths.append(box_lengths_aux)
                    box_angles.append(box_angles_aux)
                    del(coordinates_aux, box_lengths_aux, box_angles_aux)
            else:
                self.molecular_system.seek(indices)
                coordinates_aux, box_lengths_aux, box_angles_aux = self.molecular_system.read(1, 0, self._mdtraj_atom_indices)
                coordinates=coordinates_aux
                box_lengths=box_lengths_aux
                box_angles=box_angles_aux
                del(coordinates_aux, box_lengths_aux, box_angles_aux)

            for argument in self.arguments:

                if argument == 'coordinates':
                    self._output_dictionary['coordinates'] = puw.quantity(np.array(coordinates),'angstroms', standardized=True)
                    del(coordinates)
                elif argument == 'structure_id':
                    self._output_dictionary['structure_id'] = indices
                elif argument == 'box':
                    box_lengths = puw.quantity(np.array(box_lengths), 'angstroms', standardized=True)
                    box_angles = puw.quantity(np.array(box_angles), 'degrees', standardized=True)
                    self._output_dictionary['box'] = get_box_from_lengths_and_angles(box_lengths, box_angles)
                    del(box_lengths, box_angles)

            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary

            return  output

        else:

            raise StopIteration

