from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt._private.variables import is_all
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import puw

def fit (molecular_system=None, selection='backbone', structure_indices='all',
         reference_molecular_system=None, reference_selection=None, reference_structure_index=0,
         to_form=None, parallel=True, syntax='MolSysMT', method='least rmsd', engine='MolSysMT',
         check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        syntax = digest_syntax(syntax)
        selection = digest_selection(selection, syntax)
        structure_indices = digest_structure_indices(structure_indices)
        engine = digest_engine(engine)

        if reference_molecular_system is not None:
            digest_single_molecular_system(reference_molecular_system)

        if reference_selection is not None:
            reference_selection = digest_selection(reference_selection, syntax)

        if reference_structure_index is not None:
            reference_structure_index = digest_structure_indices(reference_structure_index)

    from molsysmt.basic import select, get, set, convert, copy, is_molecular_system

    if engine=='MolSysMT':

        n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True)
        atom_indices = select(molecular_system, selection=selection, syntax=syntax, check=False)
        n_atom_indices = atom_indices.shape[0]
        structure_indices = digest_structure_indices(structure_indices)
        if is_all(structure_indices):
            structure_indices = np.arange(n_structures)
        n_structure_indices = structure_indices.shape[0]

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_atom_indices = select(reference_molecular_system, selection=reference_selection,
                syntax=syntax, check=False)

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
            tmp_molecular_system = copy(molecular_system, check=False)
        else:
            tmp_molecular_system = convert(molecular_system, to_form=to_form)

        set(tmp_molecular_system, element='system', coordinates=coordinates)
        del(coordinates, units)
        return tmp_molecular_system

    elif engine=='MDTraj':

        #tmp_item.superpose(tmp_ref_item,frame=ref_structure_indices,atom_indices=atom_indices,ref_atom_indices=ref_atom_indices,parallel=parallel)

        #if in_form==x_form:
        #    item=tmp_item
        #elif in_form=='molsysmt.Trajectory':
        #    item._import_mdtraj_data(tmp_item)
        #elif in_form=='molsysmt.MolSys':
        #    item.trajectory._import_mdtraj_data(tmp_item)
        #else:
        #    item=_convert(tmp_item, to_form=in_form)

        raise NotImplementedMethodError()

    else:

        raise NotImplementedMethodError()

