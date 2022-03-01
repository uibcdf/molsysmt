from molsysmt._private_tools._digestion import digest_molecular_system, digest_engine
from molsysmt._private_tools._digestion import digest_structure_indices
from molsysmt.basic import select, get, set, convert, copy
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import puw

def fit (molecular_system=None, selection='backbone', structure_indices='all',
         reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
         to_form=None, parallel=True, syntaxis='MolSysMT', method='least rmsd', engine='MolSysMT'):

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        n_atoms, n_frames = get(molecular_system, n_atoms=True, n_frames=True)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
        n_atom_indices = atom_indices.shape[0]
        structure_indices = digest_structure_indices(structure_indices)
        if structure_indices is 'all':
            structure_indices = np.arange(n_frames)
        n_structure_indices = structure_indices.shape[0]

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_atom_indices = select(reference_molecular_system, selection=reference_selection, syntaxis=syntaxis)

        reference_coordinates = get(reference_molecular_system, target='atom', indices=reference_atom_indices,
                                    structure_indices=reference_frame_index, coordinates=True)

        coordinates = get(molecular_system, coordinates=True, structure_indices='all')
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, to_unit=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        librmsd.least_rmsd_fit(coordinates, atom_indices, reference_coordinates, structure_indices,
                                n_atoms, n_frames, n_atom_indices, n_structure_indices)

        coordinates=np.ascontiguousarray(coordinates)*units
        coordinates=puw.standardize(coordinates)

        if to_form is None:
            tmp_molecular_system = copy(molecular_system)
        else:
            tmp_molecular_system = convert(molecular_system, to_form=to_form)

        set(tmp_molecular_system, target='system', coordinates=coordinates)
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

        raise NotImplementedError

    else:

        raise NotImplementedError

