from molsysmt import puw
from molsysmt.basic import convert, select, get
from molsysmt._private_tools._digestion import digest_engine, digest_target
import numpy as np

def get_sasa (molecular_system, target='atom', selection='all', structure_indices='all', syntaxis='MolSysMT',
          engine='MDTraj'):

    engine = digest_engine(engine)
    target = digest_target(target)

    if engine == 'MDTraj':

        from mdtraj import shrake_rupley

        tmp_item = convert(molecular_system, structure_indices=structure_indices, to_form='mdtraj.Trajectory')

        sasa_array = shrake_rupley(tmp_item, mode='atom') # tiene probe_radius y n_sphere_points

        if target=='atom':

            if selection is not 'all':

                atom_indices = select(molecular_system, selection=selection, syntaxis=syntaxis)
                sasa_array = sasa_array[:,atom_indices]

        else:

            sets_atoms = get(molecular_system, target=target, selection=selection, syntaxis=syntaxis, atom_index=True)

            n_sets = len(sets_atoms)
            n_frames = sasa_array.shape[0]

            new_sasa_array = np.empty([n_frames, n_sets], dtype='float')
            for ii in range(n_sets):
                new_sasa_array[:,ii] = sasa_array[:,sets_atoms[ii].astype(int)].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = puw.quantity(sasa_array, 'nm**2')
        sasa_array = puw.standardize(sasa_array)

    else:

        raise NotImplementedError("Engine not implemented yet")

    return sasa_array

