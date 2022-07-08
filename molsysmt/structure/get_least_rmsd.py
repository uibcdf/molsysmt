from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.arguments import is_all
from molsysmt.basic import select, get
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import puw

def get_least_rmsd (molecular_system=None, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          reference_coordinates=None, parallel=True, syntaxis='MolSysMT', engine='MolSysMT',
          check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntaxis = digest_syntaxis(syntaxis)
        selection = digest_selection(selection, syntaxis)
        structure_indices = digest_structure_indices(structure_indices)
        engine = digest_engine(engine)

        if reference_molecular_system is not None:
            digest_single_molecular_system(reference_molecular_system)

        if reference_selection is not None:
            reference_selection = digest_selection(reference_selection, syntaxis)

        reference_structure_index = digest_structure_indices(reference_structure_index)

    if engine=='MolSysMT':

        n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis, check=False)
        n_atom_indices = atom_indices.shape[0]
        structure_indices = digest_structure_indices(structure_indices)
        if is_all(structure_indices):
            structure_indices = np.arange(n_structures)
        n_structure_indices = structure_indices.shape[0]

        if reference_coordinates is None:

            if reference_molecular_system is None:
                reference_molecular_system = molecular_system

            if reference_selection is None:
                reference_selection = selection

            reference_atom_indices = select(reference_molecular_system,
                    selection=reference_selection, syntaxis=syntaxis, check=False)

            reference_coordinates = get(reference_molecular_system, element='atom', indices=reference_atom_indices,
                                        structure_indices=reference_structure_index, coordinates=True)

        coordinates = get(molecular_system, structure_indices='all', coordinates=True)
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, to_unit=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        rmsd_val = librmsd.least_rmsd(coordinates, atom_indices, reference_coordinates, structure_indices,
                                 n_atoms, n_structures, n_atom_indices, n_structure_indices)

        rmsd_val = rmsd_val * units
        rmsd_val = puw.standardize(rmsd_val)
        del(coordinates, units)
        return rmsd_val

    elif engine=='MDTraj':

        raise NotImplementedError

    else:
        raise NotImplementedError

