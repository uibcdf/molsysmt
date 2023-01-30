from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.pbc import box_from_box_lengths_and_angles
from copy import copy
import numpy as np
from molsysmt._private.digestion import digest

class StructuresIterator():

    @digest(form='mdtraj.HDF5TrajectoryFile')
    def __init__(self, molecular_system, atom_indices='all', start=0, stop=None, step=1, chunk=1,
            structure_indices=None, output_type = 'values', **kwargs):

        self.molecular_system = molecular_system
        self.atom_indices = atom_indices
        self.structure_indices = structure_indices
        self.start = start
        self.step = step
        self.stop = stop
        self.chunk = chunk

        self.structure_index = 0

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)
                self._output_dictionary[key] = None

        if self.stop is None:
            from .get import get_n_structures_from_system
            self.stop = get_n_structures_from_system(molecular_system)

    def __iter__(self):

        return self

    def __next__(self):

        if self.structure_index <= self.stop:

            mdtraj_output = self.molecular_system.read(n_frames=self.chunk, stride=self.step, atom_indices=self.atom_indices)

            for argument in self.arguments:

                if argument == 'coordinates':

                    self._output_dictionary['coordinates'] = puw.quantity(mdtraj_output.coordinates, 'nm', standardized=True)

                elif argument == 'velocities':

                    self._output_dictionary['velocities'] = puw.quantity(mdtraj_output.coordinates, 'nm/ps', standardized=True)

                elif argument == 'time':

                    self._output_dictionary['time'] = puw.quantity(mdtraj_output.time, 'ps', standardized=True)

                elif argument == 'structure_id':

                    self._output_dictionary['structure_id'] = np.arange(self.structure_index, self.structure_index+self.chunk)

                elif argument == 'box':

                    box_lengths = puw.quantity(mdtraj_output.cell_lengths, 'nm', standardized=True)
                    box_angles = puw.quantity(mdtraj_output.cell_angles, 'degrees', standardized=True)
                    self._output_dictionary['box'] = box_from_box_lengths_and_angles(box_lengths, box_angles)

                elif argument == 'temperature':

                    self._output_dictionary['temperature'] = puw.quantity(mdtraj_output.temperature, 'K', standardized=True)

                elif argument == 'potential_energy':

                    self._output_dictionary['potentialEnergy'] = puw.quantity(mdtraj_output.time, 'kJ/mol', standardized=True)

                elif argument == 'kinetic_energy':

                    self._output_dictionary['kineticEnergy'] = puw.quantity(mdtraj_output.time, 'kJ/mol', standardized=True)

            self.structure_index += self.chunk

            if self.chunk == 1:
                for key, value in self._output_dictionary.items():
                    self._output_dictionary[key] = value[0]

            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary

            return  output

        else:

            raise StopIteration

class TopologyIterator():

    def __init__(self):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise NotImplementedIteration


