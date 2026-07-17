from molsysmt import pyunitwizard as puw
from molsysmt._private.variables import is_all
from molsysmt.pbc import get_box_from_lengths_and_angles
from copy import copy
import numpy as np
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.indices import indices_iterator

class StructuresIterator():

    @arg_digest(form='mdtraj.DCDTrajectoryFile')
    def __init__(self, molecular_system, atom_indices='all', start=0, stop=None, step=1, chunk=1,
            structure_indices=None, output_type='values', skip_digestion=False, **kwargs):

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
                from .get_structural_attributes import get_n_structures_from_system
                self.stop = get_n_structures_from_system(molecular_system, skip_digestion=True)
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
            box_is_available = True
            if isinstance(indices, (list, tuple, np.ndarray)):

                for ii in indices:
                    self.molecular_system.seek(int(ii))
                    coordinates_aux, box_lengths_aux, box_angles_aux = self.molecular_system.read(1, 0, self._mdtraj_atom_indices)
                    coordinates.append(np.float64(coordinates_aux[0]))
                    if box_lengths_aux is None or box_angles_aux is None:
                        box_is_available = False
                    elif box_is_available:
                        box_lengths.append(np.float64(box_lengths_aux[0]))
                        box_angles.append(np.float64(box_angles_aux[0]))
                    del(coordinates_aux, box_lengths_aux, box_angles_aux)
            else:
                self.molecular_system.seek(int(indices))
                coordinates_aux, box_lengths_aux, box_angles_aux = self.molecular_system.read(1, 0, self._mdtraj_atom_indices)
                coordinates=np.float64(coordinates_aux)
                if box_lengths_aux is None or box_angles_aux is None:
                    box_is_available = False
                else:
                    box_lengths=np.float64(box_lengths_aux)
                    box_angles=np.float64(box_angles_aux)
                del(coordinates_aux, box_lengths_aux, box_angles_aux)

            for argument in self.arguments:

                if argument == 'coordinates':
                    self._output_dictionary['coordinates'] = puw.quantity(np.array(coordinates),'angstroms', standardized=True)
                    del(coordinates)
                elif argument == 'structure_id':
                    self._output_dictionary['structure_id'] = indices
                elif argument == 'box':
                    if box_is_available:
                        box_lengths = puw.quantity(np.array(box_lengths), 'angstroms', standardized=True)
                        box_angles = puw.quantity(np.array(box_angles), 'degrees', standardized=True)
                        self._output_dictionary['box'] = get_box_from_lengths_and_angles(box_lengths, box_angles,
                                                                                         skip_digestion=True)
                        del(box_lengths, box_angles)
                    else:
                        self._output_dictionary['box'] = None

            if self._output_type=='values':
                output = list(self._output_dictionary.values())
                if len(output) == 1:
                    output = output[0]
            elif self._output_type=='dictionary':
                output = self._output_dictionary

            return  output

        else:

            raise StopIteration

    def __enter__(self):
        return self

    def __exit__(self, *args):
        if hasattr(self.molecular_system, 'close'):
            self.molecular_system.close()
