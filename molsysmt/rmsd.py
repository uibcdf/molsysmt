from molsysmt._private_tools._digestion import digest_molecular_system, digest_engine
import numpy as np
from .lib import rmsd as librmsd
from molsysmt import puw

def rmsd (molecular_system, selection='backbone', frame_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
          reference_coordinates=None, parallel=True, syntaxis='MolSysMT', engine='MolSysMT'):

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        from molsysmt.multitool import select, get
        from molsysmt._private_tools._digestion import digest_frame_indices

        n_atoms, n_frames = get(molecular_system, n_atoms=True, n_frames=True)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
        n_atom_indices = atom_indices.shape[0]
        frame_indices = digest_frame_indices(frame_indices)
        if frame_indices is 'all':
            frame_indices = np.arange(n_frames)
        n_frame_indices = frame_indices.shape[0]

        if reference_coordinates is None:

            if reference_molecular_system is None:
                reference_molecular_system = molecular_system

            if reference_selection is None:
                reference_selection = selection

            reference_atom_indices = select(reference_molecular_system, selection=reference_selection, syntaxis=syntaxis)

            reference_coordinates = get(reference_molecular_system, target='atom', indices=reference_atom_indices, frame_indices=reference_frame_index, coordinates=True)

        coordinates = get(molecular_system, coordinates=True, frame_indices='all')
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, in_units=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        rmsd_val = librmsd.rmsd(coordinates, atom_indices, reference_coordinates, frame_indices,
                                 n_atoms, n_frames, n_atom_indices, n_frame_indices)

        rmsd_val = rmsd_val * units
        rmsd_val = puw.standardize(rmsd_val)
        del(coordinates, units)
        return rmsd_val

    elif engine=='MDTraj':

        #from mdtraj import rmsd as mdtraj_rmsd
        #from molsysmt.multitool import convert

        #tmp_molecular_system = convert(molecular_system, to_form='mdtraj.Trajectory')

        #rmsd_val = mdtraj_rmsd(tmp_molecular_system, ref_item, frame=ref_frame_indices,
        #                        ref_atom_indices=ref_atom_indices, atom_indices=atom_indices,
        #                        parallel=parallel, precentered=precentered)

        #rmsd_val = puw.standardize(rmsd_val)

        #return rmsd_val

        raise NotImplementedError

    else:

        raise NotImplementedError

def least_rmsd (molecular_system=None, selection='backbone', frame_indices='all',
          reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
          reference_coordinates=None, parallel=True, syntaxis='MolSysMT', engine='MolSysMT'):

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        from molsysmt.multitool import select, get
        from molsysmt._private_tools._digestion import digest_frame_indices

        n_atoms, n_frames = get(molecular_system, n_atoms=True, n_frames=True)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
        n_atom_indices = atom_indices.shape[0]
        frame_indices = digest_frame_indices(frame_indices)
        if frame_indices is 'all':
            frame_indices = np.arange(n_frames)
        n_frame_indices = frame_indices.shape[0]

        if reference_coordinates is None:

            if reference_molecular_system is None:
                reference_molecular_system = molecular_system

            if reference_selection is None:
                reference_selection = selection

            reference_atom_indices = select(reference_molecular_system, selection=reference_selection, syntaxis=syntaxis)

            reference_coordinates = get(reference_molecular_system, target='atom', indices=reference_atom_indices, frame_indices=reference_frame_index, coordinates=True)

        coordinates = get(molecular_system, coordinates=True, frame_indices='all')
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, in_units=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        rmsd_val = librmsd.least_rmsd(coordinates, atom_indices, reference_coordinates, frame_indices,
                                 n_atoms, n_frames, n_atom_indices, n_frame_indices)

        rmsd_val = rmsd_val * units
        rmsd_val = puw.standardize(rmsd_val)
        del(coordinates, units)
        return rmsd_val

    elif engine=='MDTraj':

        raise NotImplementedError

    else:
        raise NotImplementedError

def least_rmsd_fit (molecular_system=None, selection='backbone', frame_indices='all',
                    reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
                    to_form=None, parallel=True, syntaxis='MolSysMT', engine='MolSysMT'):

    molecular_system = digest_molecular_system(molecular_system)
    engine = digest_engine(engine)

    if engine=='MolSysMT':

        from molsysmt.multitool import select, get, set, convert
        from molsysmt._private_tools._digestion import digest_frame_indices

        n_atoms, n_frames = get(molecular_system, n_atoms=True, n_frames=True)
        atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
        n_atom_indices = atom_indices.shape[0]
        frame_indices = digest_frame_indices(frame_indices)
        if frame_indices is 'all':
            frame_indices = np.arange(n_frames)
        n_frame_indices = frame_indices.shape[0]

        if reference_molecular_system is None:
            reference_molecular_system = molecular_system

        if reference_selection is None:
            reference_selection = selection

        reference_atom_indices = select(reference_molecular_system, selection=reference_selection, syntaxis=syntaxis)

        reference_coordinates = get(reference_molecular_system, target='atom', indices=reference_atom_indices,
                                    frame_indices=reference_frame_index, coordinates=True)

        coordinates = get(molecular_system, coordinates=True, frame_indices='all')
        units = puw.get_unit(coordinates)
        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates, in_units=units), dtype='float64')

        if reference_coordinates.shape[1]!=n_atom_indices:
            raise ValueError("reference selection and selection needs to have the same number of atoms")

        librmsd.least_rmsd_fit(coordinates, atom_indices, reference_coordinates, frame_indices,
                                n_atoms, n_frames, n_atom_indices, n_frame_indices)

        coordinates=np.ascontiguousarray(coordinates)*units
        coordinates=puw.standardize(coordinates)

        if to_form is None:

            set(molecular_system, target='system', coordinates=coordinates)
            del(coordinates, units)
            pass

        else:

            tmp_item = convert(molecular_system, to_form=to_form)
            set(tmp_item, target='system', coordinates=coordinates)
            del(coordinates, units)
            return tmp_item

    elif engine=='MDTraj':

        #tmp_item.superpose(tmp_ref_item,frame=ref_frame_indices,atom_indices=atom_indices,ref_atom_indices=ref_atom_indices,parallel=parallel)

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

#def angular_rmsd (item=None, selection='backbone', frame_indices='all',
#          reference_molecular_system=None, reference_selection=None, reference_frame_index=0,
#          reference_coordinates=None, parallel=True, syntaxis='MolSysMT', engine='MolSysMT'):
#
#    raise NotImplementedError

