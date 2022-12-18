from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import pyunitwizard as puw

@digest()
def fit (molecular_system=None, selection=None, structure_indices='all',
         reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
         to_form=None, syntax='MolSysMT', method='least rmsd', engine='MolSysMT'):

    from molsysmt.basic import select, get, set, convert, copy, is_a_molecular_system

    if engine=='MolSysMT':

        n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True)
        atom_indices = select(molecular_system, selection=selection, syntax=syntax)
        n_atom_indices = atom_indices.shape[0]
        if is_all(structure_indices):
            structure_indices = np.arange(n_structures)
        n_structure_indices = structure_indices.shape[0]

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_atom_indices = select(reference_molecular_system, selection=reference_selection,
                syntax=syntax)

        reference_coordinates = get(reference_molecular_system, element='atom', indices=reference_atom_indices,
                                    structure_indices=reference_structure_index, coordinates=True)

        coordinates = get(molecular_system, structure_indices='all', coordinates=True)
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, to_unit=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        librmsd.least_rmsd_fit(coordinates, atom_indices, reference_coordinates, structure_indices,
                                n_atoms, n_structures, n_atom_indices, n_structure_indices)

        coordinates=np.ascontiguousarray(coordinates)*units
        coordinates=puw.standardize(coordinates)

        if to_form is None:
            tmp_molecular_system = copy(molecular_system)
        else:
            tmp_molecular_system = convert(molecular_system, to_form=to_form)

        set(tmp_molecular_system, element='system', coordinates=coordinates)
        del(coordinates, units)
        return tmp_molecular_system

    else:

        raise NotImplementedMethodError()

