from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np

@digest()
def get_distances(molecular_system, selection="all", groups_of_atoms=None, group_behavior=None, structure_indices="all",
             molecular_system_2=None, selection_2=None, groups_of_atoms_2=None, group_behavior_2=None, structure_indices_2=None,
             pairs=False, crossed_structures=False, pbc=True, output_type='numpy.ndarray',
             output_with_atom_indices=False, output_with_structure_indices=False, engine='MolSysMT',
             syntax='MolSysMT'):
    """get_distances(item, to_form='molsysmt.MolSys', selection='all', structure_indices='all', syntax='MolSysMT', **kwargs)

    This is a sentence

    This is a paragraph

    Parameters
    ----------

    Returns
    -------

    Examples
    --------

    See Also
    --------

    Notes
    -----

    """

    # group_behavior in
    # ['center_of_mass','geometric_center','minimum_distance','maximum_distance']
    # output in ['numpy.ndarray','dictionary']

    # crossed_structures es para cuando queremos calcular lista de structures1 contra lista de structures 2
    # (todos con todos), si crossed_structures=False entonces es sólo el primer structure de lista 1 contra
    # el primer structure de lista 2, el segundo contra el segundo, etc.

    # selection groups está por si quiero distancias entre centros de masas, necesita
    # hacer un lista de listas frente a otra lista de listas.

    from molsysmt.basic import select, get
    from . import get_center_of_mass
    from . import get_geometric_center

    same_system = False

    if molecular_system_2 is None:
        same_system = True
        molecular_system_2 = molecular_system

    if group_behavior=='minimum_distance' or group_behavior_2=='minimum_distance':
        if group_behavior=='minimum_distance' and group_behavior_2=='minimum_distance':
            raise NotImplementedMethodError
            #num_groups_1=len(groups_of_atoms)
            #num_groups_2=len(groups_of_atoms_2)
            #structure_indices = _digest_structure_indices(item, structure_indices)
            #num_structures=len(structure_indices)
            #dists = np.zeros((num_structures, num_groups_1, num_groups_2),dtype=float)
            #for ii in range(num_groups_1):
            #    group1 = groups_of_atoms_2[ii]
            #    for jj in range(num_groups_2):
            #        group2 = groups_of_atoms_2[jj]
            #        _, min_dist = min_distances(molecular_system=molecular_system, selection=group1,
            #                                    structure_indices=structure_indices,
            #                                    selection_2=group2,
            #                                    pbc=pbc, parallel=parallel, engine=engine)
            #        dists[:,ii,jj]=min_dist
            #del(num_groups1,num_groups2,structure_indices,num_structures,group1,group2)
            #return dists
        else:
            raise NotImplementedMethodError

    if engine=='MolSysMT':

        same_selection = False
        same_groups = False
        same_structures = False

        if groups_of_atoms is not None:
            selection=None

        if (selection is not None) and (selection_2 is None):
            if (groups_of_atoms_2 is None):
                selection_2 = selection
                same_selection = True

        if groups_of_atoms is not None:
            if (selection_2 is None) and (groups_of_atoms_2 is None):
                groups_of_atoms_2=groups_of_atoms
                same_groups = True

        if structure_indices_2 is None:
            structure_indices_2 = structure_indices
            same_structures = True

        if selection is not None:

            if group_behavior == 'center_of_mass':
                coordinates_1 = get_center_of_mass(molecular_system, selection=selection,
                                                   structure_indices=structure_indices)
                atom_indices_1 = [0]
            elif group_behavior == 'geometric_center':
                coordinates_1 = get_geometric_center(molecular_system, selection=selection,
                                                     structure_indices=structure_indices)
                atom_indices_1 = [0]
            else:
                atom_indices_1 = select(molecular_system, selection=selection, syntax=syntax)
                coordinates_1 = get(molecular_system, element='atom', indices=atom_indices_1,
                                    structure_indices=structure_indices, coordinates=True)
        else:

            if group_behavior == 'center_of_mass':
                coordinates_1 = get_center_of_mass(molecular_system,
                                                   groups_of_atoms=groups_of_atoms,
                                                   structure_indices=structure_indices)
                atom_indices_1 = np.range(coordinates_1.shape[1])
            elif group_behavior == 'geometric_center':
                coordinates_1 = get_geometric_center(molecular_system,
                                                     groups_of_atoms=groups_of_atoms,
                                                     structure_indices=structure_indices)
                atom_indices_1 = np.arange(coordinates_1.shape[1])
            else:
                raise ValueError("Value of argument group_behavior not recognized.")


        if selection_2 is not None:

            if same_system and same_selection and same_structures:

                atom_indices_2 = atom_indices_1
                coordinates_2 = coordinates_1

            else:

                if group_behavior_2 == 'center_of_mass':
                    coordinates_2 = get_center_of_mass(molecular_system_2, selection=selection_2,
                                                       structure_indices=structure_indices_2)
                    atom_indices_2 = [0]
                elif group_behavior_2 == 'geometric_center':
                    coordinates_2 = get_geometric_center(molecular_system_2, selection=selection_2,
                                                         structure_indices=structure_indices_2)
                    atom_indices_2 = [0]
                else:
                    atom_indices_2 = select(molecular_system_2, selection=selection_2, syntax=syntax)
                    coordinates_2 = get(molecular_system_2, element='atom', indices=atom_indices_2,
                                        structure_indices=structure_indices_2, coordinates=True)

        else:

            if same_system and same_groups and same_structures:
                atom_indices_2 = atom_indices_1
                coordinates_2 = coordinates_1
            else:
                if group_behavior_2 == 'center_of_mass':
                    coordinates_2 = get_center_of_mass(molecular_system_2,
                                                       groups_of_atoms=groups_of_atoms_2,
                                                       structure_indices=structure_indices_2)
                    atom_indices_2 = np.arange(coordinates_2.shape[1])
                elif group_behavior_2 == 'geometric_center':
                    coordinates_2 = get_geometric_center(molecular_system_2,
                                                         groups_of_atoms=groups_of_atoms_2,
                                                         structure_indices=structure_indices_2)
                    atom_indices_2 = np.arange(coordinates_2.shape[1])
                else:
                    raise ValueError("Value of argument group_behavior_2 not recognized.")

        diff_set = not ((same_system and same_selection and same_structures) or (same_system and same_groups and same_structures))

        length_units = puw.get_unit(coordinates_1)
        coordinates_1 = np.asfortranarray(puw.get_value(coordinates_1), dtype='float64')
        coordinates_2 = np.asfortranarray(puw.get_value(coordinates_2), dtype='float64')
        nstructures_1 = coordinates_1.shape[0]
        nstructures_2 = coordinates_2.shape[0]
        nelements1 = coordinates_1.shape[1]
        nelements2 = coordinates_2.shape[1]

        if pbc:

            box, box_shape = get(molecular_system, element='system', structure_indices=structure_indices, box=True,
                                 box_shape=True)

            orthogonal = 0
            if box_shape is None:
                raise ValueError("The system has no PBC box. The input argument 'pbc' can not be True.")
            elif box_shape == 'cubic':
                orthogonal =1

        else:

            box= np.zeros([nstructures_1, 3, 3])*length_units
            orthogonal = 1

        box = np.asfortranarray(puw.get_value(box), dtype='float64')

        if crossed_structures is False:
            if nstructures_1 != nstructures_2:
                raise ValueError("Both structure_indices and structure_indices_2 need the same number of structures.")
            else:
                if pairs is False:
                    dists = distance(diff_set, coordinates_1, coordinates_2, box, orthogonal, pbc)
                else:
                    if nstructures_1 != nstructures_2:
                        raise ValueError("Both selection and selection_2 need the same number of atoms.")
                    else:
                        dists = distance_pairs(coordinates_1, coordinates_2, box, orthogonal, pbc)
        else:
            raise NotImplementedMethodError

        del(coordinates_1, coordinates_2, box)

        dists = dists*length_units

        if output_type=='numpy.ndarray':
            if output_with_structure_indices:

                if is_all(structure_indices):
                    structure_indices = np.arange(nstructures_1)
                if is_all(structure_indices_2):
                    structure_indices_2 = np.arange(nstructures_2)

                if output_with_atom_indices:
                    return atom_indices_1, structure_indices, atom_indices_2, structure_indices_2, dists
                else:
                    return structure_indices, structure_indices_2, dists

            elif output_with_atom_indices:
                return atom_indices_1, atom_indices_2, dists
            else:
                return dists

        elif output_type=='dictionary':
            if is_all(structure_indices):
                structure_indices = np.arange(nstructures_1)
            if is_all(structure_indices_2):
                structure_indices_2 = np.arange(nstructures_2)
            if pairs is False:
                if crossed_structures is False:
                    tmp_dict={}
                    for ii in range(len(atom_indices_1)):
                        atom1=atom_indices_1[ii]
                        tmp_dict[atom1]={}
                        for jj in range(len(atom_indices_2)):
                            atom2=atom_indices_2[jj]
                            tmp_dict[atom1][atom2]={}
                            for kk in range(len(structure_indices)):
                                structure_index_1 = structure_indices[kk]
                                tmp_dict[atom1][atom2][structure_index_1]=dists[kk,ii,jj]
                    return tmp_dict
                else:
                    raise NotImplementedMethodError
            else:
                if crossed_structures is False:
                    tmp_dict={}
                    for ii in range(len(atom_indices_1)):
                        atom1=atom_indices_1[ii]
                        atom2=atom_indices_2[ii]
                        if atom1 not in tmp_dict:
                            tmp_dict[atom1]={}
                        if atom2 not in tmp_dict[atom1]:
                            tmp_dict[atom1][atom2]={}
                        for kk in range(len(structure_indices)):
                            structure_index_1 = structure_indices[kk]
                            tmp_dict[atom1][atom2][structure_index_1]=dists[kk,ii]
                    return tmp_dict
                else:
                    raise NotImplementedMethodError

        else:
            raise NotImplementedMethodError

    else:

        raise NotImplementedMethodError

