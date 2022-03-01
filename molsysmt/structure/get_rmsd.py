from molsysmt._private_tools._digestion import digest_molecular_system, digest_engine
import numpy as np
from molsysmt.lib import rmsd as librmsd
from molsysmt import puw

def get_rmsd(molecular_system, selection='backbone', structure_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
          reference_coordinates=None, parallel=True, syntaxis='MolSysMT', engine='MolSysMT'):

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        from molsysmt.basic import select, get
        from molsysmt._private_tools._digestion import digest_structure_indices

        n_atoms, n_frames = get(molecular_system, n_atoms=True, n_frames=True)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
        n_atom_indices = atom_indices.shape[0]
        structure_indices = digest_structure_indices(structure_indices)
        if structure_indices is 'all':
            structure_indices = np.arange(n_frames)
        n_structure_indices = structure_indices.shape[0]

        if reference_coordinates is None:

            if reference_molecular_system is None:
                reference_molecular_system = molecular_system

            if reference_selection is None:
                reference_selection = selection

            reference_atom_indices = select(reference_molecular_system, selection=reference_selection, syntaxis=syntaxis)

            reference_coordinates = get(reference_molecular_system, target='atom', indices=reference_atom_indices, structure_indices=reference_frame_index, coordinates=True)

        coordinates = get(molecular_system, coordinates=True, structure_indices='all')
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, to_unit=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        rmsd_val = librmsd.rmsd(coordinates, atom_indices, reference_coordinates, structure_indices,
                                 n_atoms, n_frames, n_atom_indices, n_structure_indices)

        rmsd_val = rmsd_val * units
        rmsd_val = puw.standardize(rmsd_val)
        del(coordinates, units)
        return rmsd_val

    elif engine=='MDTraj':

        #from mdtraj import rmsd as mdtraj_rmsd
        #from molsysmt.basic import convert

        #tmp_molecular_system = convert(molecular_system, to_form='mdtraj.Trajectory')

        #rmsd_val = mdtraj_rmsd(tmp_molecular_system, ref_item, frame=ref_structure_indices,
        #                        ref_atom_indices=ref_atom_indices, atom_indices=atom_indices,
        #                        parallel=parallel, precentered=precentered)

        #rmsd_val = puw.standardize(rmsd_val)

        #return rmsd_val

        raise NotImplementedError

    else:

        raise NotImplementedError

