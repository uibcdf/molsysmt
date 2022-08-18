from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import pyunitwizard as puw

@digest()
def get_rmsd(molecular_system, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
          syntax='MolSysMT', engine='MolSysMT'):

    if engine=='MolSysMT':

        from molsysmt.basic import select, get

        n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True)
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        n_atom_indices = atom_indices.shape[0]
        if is_all(structure_indices):
            structure_indices = np.arange(n_structures)
        n_structure_indices = structure_indices.shape[0]

        coordinates = get(molecular_system, structure_indices='all', coordinates=True)
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_atom_indices = select(reference_molecular_system,
                selection=reference_selection, syntax=syntax)

        reference_coordinates = get(reference_molecular_system, element='atom', indices=reference_atom_indices,
                                    structure_indices=reference_structure_index, coordinates=True)

        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, to_unit=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        rmsd_val = librmsd.rmsd(coordinates, atom_indices, reference_coordinates, structure_indices,
                                 n_atoms, n_structures, n_atom_indices, n_structure_indices)

        rmsd_val = rmsd_val * units
        rmsd_val = puw.standardize(rmsd_val)
        del(coordinates, units)

        return rmsd_val

    else:

        raise NotImplementedMethodError()

