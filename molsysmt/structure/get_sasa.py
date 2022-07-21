from molsysmt._private.exceptions.not_implemented import NotImplementedError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import puw
import numpy as np

@digest
def get_sasa (molecular_system, element='atom', selection='all', structure_indices='all', syntax='MolSysMT',
          engine='MDTraj'):

    if engine == 'MDTraj':

        from mdtraj import shrake_rupley
        from molsysmt.basic import convert, select, get

        tmp_item = convert(molecular_system, to_form='mdtraj.Trajectory', structure_indices=structure_indices)

        sasa_array = shrake_rupley(tmp_item, mode='atom') # tiene probe_radius y n_sphere_points

        if element=='atom':

            if not is_all(selection):

                atom_indices = select(molecular_system, selection=selection, syntax=syntax)
                sasa_array = sasa_array[:,atom_indices]

        else:

            sets_atoms = get(molecular_system, element=element, selection=selection, syntax=syntax, atom_index=True)

            n_sets = len(sets_atoms)
            n_structures = sasa_array.shape[0]

            new_sasa_array = np.empty([n_structures, n_sets], dtype='float')
            for ii in range(n_sets):
                new_sasa_array[:,ii] = sasa_array[:,sets_atoms[ii].astype(int)].sum(axis=1)
            sasa_array = new_sasa_array

        sasa_array = puw.quantity(sasa_array, 'nm**2')
        sasa_array = puw.standardize(sasa_array)

    else:

        raise NotImplementedError("Engine not implemented yet")

    return sasa_array

