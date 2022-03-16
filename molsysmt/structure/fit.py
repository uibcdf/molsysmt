from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt.basic import select, get, set, convert, copy
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import puw

def fit (molecular_system=None, selection='backbone', structure_indices='all',
         reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
         to_form=None, parallel=True, syntaxis='MolSysMT', method='least rmsd', engine='MolSysMT',
         check=True):

    if check:
        from molsysmt.tools.molecular_system import is_molecular_system
        if not is_molecular_system(molecular_system):
            raise MolecularSystemNeededError()

    engine = digest_engine(engine)

    if engine=='MolSysMT':

        n_atoms, n_structures = get(molecular_system, n_atoms=True, n_structures=True, check=False)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis, check=False)
        n_atom_indices = atom_indices.shape[0]
        structure_indices = digest_structure_indices(structure_indices)
        if structure_indices is 'all':
            structure_indices = np.arange(n_structures)
        n_structure_indices = structure_indices.shape[0]

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_atom_indices = select(reference_molecular_system, selection=reference_selection,
                syntaxis=syntaxis, check=False)

        reference_coordinates = get(reference_molecular_system, target='atom', indices=reference_atom_indices,
                                    structure_indices=reference_frame_index, coordinates=True,
                                    check=False)

        coordinates = get(molecular_system, coordinates=True, structure_indices='all', check=False)
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
            tmp_molecular_system = convert(molecular_system, to_form=to_form, check=False)

        set(tmp_molecular_system, target='system', coordinates=coordinates, check=False)
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

