from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.pbc import get_box_from_lengths_and_angles
from copy import copy
import numpy as np
from molsysmt._private.digestion import digest
from molsysmt._private.indices import indices_iterator

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

        self.structure_index = None

        self.arguments = []
        self._output_dictionary = {}
        self._output_type = output_type

        for ii, key in enumerate(kwargs.keys()):
            if kwargs[key]:
                self.arguments.append(key)
                self._output_dictionary[key] = None


        if self.stop is None:
            if structure_indices is None:
                from .get import get_n_structures_from_system
                self.stop = get_n_structures_from_system(molecular_system)
            else:
                self.stop = len(structure_indices)

        self._indices_iterator = indices_iterator(indices=structure_indices, start=self.start,
                stop=self.stop, step=self.step, chunk=self.chunk)

        self._node = {}
        self._node['cell_angles'] = self.molecular_system._get_node(where='/', name='cell_angles')
        self._node['cell_lengths'] = self.molecular_system._get_node(where='/', name='cell_lengths')
        self._node['time'] = self.molecular_system._get_node(where='/', name='time')
        self._node['coordinates'] = self.molecular_system._get_node(where='/', name='coordinates')
        self._node['temperature'] = self.molecular_system._get_node(where='/', name='temperature')
        self._node['kinetic_energy'] = self.molecular_system._get_node(where='/', name='kineticEnergy')
        self._node['potential_energy'] = self.molecular_system._get_node(where='/', name='potentialEnergy')


    def __iter__(self):

        return self

    def __next__(self):

        indices = self._indices_iterator.__next__()

        if indices is not None:

            for argument in self.arguments:

                if argument == 'coordinates':
                    coordinates = self._node['coordinates'][indices,:,:]
                    if isinstance(indices, (int, np.int64)):
                        coordinates = np.expand_dims(coordinates, axis=0)
                    if not is_all(self.atom_indices):
                        coordinates = coordinates[:, self.atom_indices, :]
                    self._output_dictionary['coordinates'] = puw.quantity(coordinates,'nm', standardized=True)
                    del(coordinates)
                elif argument == 'time':
                    self._output_dictionary['time'] = puw.quantity(self._node['time'][indices], 'ps', standardized=True)
                elif argument == 'structure_id':
                    self._output_dictionary['structure_id'] = indices
                elif argument == 'box':
                    box_lengths = puw.quantity(self._node['cell_lengths'][indices,:].astype(np.float64), 'nm', standardized=True)
                    box_angles = puw.quantity(self._node['cell_angles'][indices,:].astype(np.float64), 'degrees', standardized=True)
                    if isinstance(indices, int):
                        box_lengths = np.expand_dims(box_lengths, axis=0)
                        box_angles = np.expand_dims(box_angles, axis=0)
                    self._output_dictionary['box'] = get_box_from_lengths_and_angles(box_lengths, box_angles)
                    del(box_lengths, box_angles)
                elif argument == 'temperature':
                    self._output_dictionary['temperature'] = puw.quantity(self._node['temperature'][indices], 'K', standardized=True)
                elif argument == 'potential_energy':
                    self._output_dictionary['potential_energy'] = puw.quantity(self._node['potential_energy'][indices], 'kJ/mol', standardized=True)
                elif argument == 'kinetic_energy':
                    self._output_dictionary['kinetic_energy'] = puw.quantity(self._node['kinetic_energy'][indices], 'kJ/mol', standardized=True)

            #if self.chunk == 1:
            #    for key, value in self._output_dictionary.items():
            #        self._output_dictionary[key] = value[0]

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


