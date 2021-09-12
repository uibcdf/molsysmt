from molsysmt._private_tools._digestion import *
from molsysmt._private_tools.exceptions import *
from molsysmt import puw
import numpy as np

def get_minimum_distances(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, as_entity=True, frame_indices="all",
                     selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, as_entity_2=True, frame_indices_2=None,
                     atom_indices=False, output_frame_indices=False, pairs=False, pbc=False, parallel=False, engine='MolSysMT', syntaxis='MolSysMT'):

    from molsysmt.structure.get_distances import get_distances

    if atom_indices:

        atom_indices_1, atom_indices_2, all_dists = get_distances(molecular_system=molecular_system, selection=selection,
                groups_of_atoms=groups_of_atoms, group_behavior=group_behavior, frame_indices=frame_indices,
                selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2, group_behavior_2=group_behavior_2, frame_indices_2=frame_indices_2, pairs=pairs, pbc=pbc,
                parallel=parallel, output_form='tensor', output_atom_indices=True, engine=engine, syntaxis=syntaxis)

    else:

        all_dists = get_distances(molecular_system=molecular_system, selection=selection, groups_of_atoms=groups_of_atoms, group_behavior=group_behavior,
                frame_indices=frame_indices, selection_2=selection_2, groups_of_atoms_2=groups_of_atoms_2,
                group_behavior_2=group_behavior_2, frame_indices_2=frame_indices_2, pairs=pairs, pbc=pbc, parallel=parallel, output_form='tensor',
                engine=engine, syntaxis=syntaxis)

    if pairs is False:

        nframes, nelements_1, nelements_2 = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity is True) and (as_entity_2 is True):

            pairs=np.empty((nframes,2),dtype=int)
            dists=np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii,jj = np.unravel_index(all_dists[indice_frame,:,:].argmin(), all_dists[indice_frame,:,:].shape)
                if atom_indices:
                    pairs[indice_frame,0] = atom_indices_1[ii]
                    pairs[indice_frame,1] = atom_indices_2[jj]
                else:
                    pairs[indice_frame,0] = ii
                    pairs[indice_frame,1] = jj
                dists[indice_frame] = all_dists[indice_frame,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity is False) and (as_entity_2 is True):

            pairs=np.empty((nframes, nelements_1), dtype=int)
            dists=np.empty((nframes, nelements_1), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_1):
                    jj = all_dists[indice_frame,ii,:].argmin()
                    if atom_indices:
                        pairs[indice_frame,ii]=atom_indices_2[jj]
                    else:
                        pairs[indice_frame,ii]=jj
                    dists[indice_frame,ii]=all_dists[indice_frame,ii,jj]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        elif (as_entity is True) and (as_entity_2 is False):

            pairs=np.empty((nframes, nelements_2), dtype=int)
            dists=np.empty((nframes, nelements_2), dtype=float)
            for indice_frame in range(nframes):
                for ii in range(nelements_2):
                    jj = all_dists[indice_frame,:,ii].argmin()
                    if atom_indices:
                        pairs[indice_frame,ii]=atom_indices_1[jj]
                    dists[indice_frame,ii]=all_dists[indice_frame,jj,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If both input arguments 'as_entity' and 'as_entity_2' are False, the method you are looking for is molsysmt.distance()")

    else:

        nframes, nelements = all_dists.shape
        length_units = puw.get_unit(all_dists)
        all_dists = puw.get_value(all_dists)

        if (as_entity is True) and (as_entity_2 is True):

            pairs=np.empty((nframes),dtype=int)
            dists=np.empty((nframes),dtype=float)
            for indice_frame in range(nframes):
                ii = all_dists[indice_frame,:].argmin()
                pairs[indice_frame] = ii
                dists[indice_frame] = all_dists[indice_frame,ii]

            del(all_dists)

            dists=dists*length_units

            return pairs, dists

        else:
            raise ValueError("If 'pairs=True' both input arguments 'as_entity' and 'as_entity_2' need to be True")

