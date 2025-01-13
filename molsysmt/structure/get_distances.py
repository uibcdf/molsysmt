from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all, is_iterable_of_iterables
from molsysmt._private.variables import is_iterable_of_pairs
from molsysmt import lib as msmlib
from molsysmt import pyunitwizard as puw
import numpy as np
import gc


@digest()
def get_distances(molecular_system, selection="all", structure_indices="all", center_of_atoms=False, weights=None,
        molecular_system_2=None, selection_2=None, structure_indices_2=None, center_of_atoms_2=False, weights_2=None,
        pairs=False, pbc=True, output_type='numpy.ndarray', output_indices=None, output_structure_indices=None,
        engine='MolSysMT', syntax='MolSysMT', skip_digestion=False):
    """
    To be written soon...

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

    # center_of_atoms and center_of_atoms_2: bool
    # output_type in ['numpy.ndarray','dictionary']

    from molsysmt.basic import select
    from molsysmt.pbc import has_pbc

    if pbc:
        pbc=has_pbc(molecular_system)

    if pairs and (selection_2 is None):
        if is_iterable_of_pairs(selection):
            if not isinstance(selection, np.ndarray):
                selection=np.array(selection)
            selection_2 = selection[:,1]
            selection = selection[:,0]
        elif len(selection)==2:
            selection_2 = selection[1]
            selection = selection[0]

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)

    if molecular_system_2 is not None:
        if selection_2 is None:
            selection_2 = selection
        if structure_indices_2 is None:
            structure_indices_2 = structure_indices
        atom_indices_2 = select(molecular_system_2, selection=selection_2)
    else:
        if selection_2 is not None:
            atom_indices_2 = select(molecular_system, selection=selection_2)
        else:
            atom_indices_2 = None

    if is_iterable_of_iterables(atom_indices):
        center_of_atoms = True

    if is_iterable_of_iterables(atom_indices_2):
        center_of_atoms_2 = True

    if engine=='MolSysMT':

        from molsysmt.basic import get
        from molsysmt.file import is_file

        in_memory = True
        if is_file(molecular_system):
            in_memory = False

        if in_memory:
            if molecular_system_2 is not None:
                if is_file(molecular_system_2):
                    in_memory = False

        if in_memory:

            distances = _get_distances_in_memory(molecular_system, selection=atom_indices,
                    structure_indices=structure_indices, center_of_atoms=center_of_atoms, weights=weights,
                    molecular_system_2=molecular_system_2, selection_2=atom_indices_2,
                    structure_indices_2=structure_indices_2, center_of_atoms_2=center_of_atoms_2, weights_2=weights_2,
                    pairs=pairs, pbc=pbc, syntax=syntax)

        else:

            raise NotImplementedMethodError

    else:

        raise NotImplementedMethodError


    if output_type=='numpy.ndarray':

        output_list = []

        if output_indices is not None:

            if pairs:

                raise NotImplementedError()

            else:

                if output_indices == 'selection': # works also with center of atoms

                    atom_indices = list(range(distances.shape[-2]))
                    output_list.append( atom_indices )

                    if atom_indices_2 is not None:

                        atom_indices_2 = list(range(distances.shape[-1]))
                        output_list.append( atom_indices_2 )

                elif output_indices == 'atom':

                    output_list.append( atom_indices )

                    if atom_indices_2 is not None:

                        output_list.append( atom_indices_2 )

                elif output_indices == 'group':

                    raise NotImplementedError()

        if output_structure_indices is not None:

            if output_structure_indices == 'selection':

                structure_indices = list(range(distances.shape[0]))
                output_list.append( structure_indices )

                if structure_indices_2 is not None:

                    structure_indices_2 = list(range(distances.shape[0]))
                    output_list.append( structure_indices_2 )

            elif output_structure_indices == 'structure':

                if is_all(structure_indices):
                    structure_indices = list(range(distances.shape[0]))
                    output_list.append( structure_indices )
                else:
                    output_list.append( structure_indices.tolist() )

                if structure_indices_2 is not None:
                    if is_all(structure_indices_2):
                        structure_indices_2 = list(range(distances.shape[0]))
                        output_list.append( structure_indices_2 )
                    else:
                        output_list.append( structure_indices_2.tolist() )

        output_list.append(distances)

        if len(output_list)==1:
            output = output_list[0]
        else:
            output = tuple(output_list)

    elif output_type=='dictionary':

        output_dictionary = {}

        if pairs:

            if output_indices is None:
                output_indices = 'atom'
            
            if output_indices is not None:

                if output_indices == 'selection': # works also with center of atoms
                    if output_structure_indices is None:
                        for ii in range(distances.shape[-1]):
                            output_dictionary[ii] = distances[:,ii]
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for ii in range(distances.shape[-1]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for ll,kk in enumerate(structure_indices):
                                    aux_ii[kk]=distances[ll,ii]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[1]))
                            for ii in range(distances.shape[-1]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for ll,kk in enumerate(structure_indices):
                                    aux_ii[kk]={}
                                    aux_ii_kk = aux_ii[kk]
                                    for mm,nn in enumerate(structure_indices_2):
                                        aux_ii_kk[nn]=distances[ll,mm,ii]

                elif output_indices == 'atom':
                    if output_structure_indices is None:
                        for aa,xx in enumerate(zip(atom_indices, atom_indices_2)):
                            if xx[0] not in output_dictionary:
                                output_dictionary[xx[0]] = {}
                            output_dictionary[xx[0]][xx[1]] = distances[:,aa]
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for aa,xx in enumerate(zip(atom_indices, atom_indices_2)):
                                if xx[0] not in output_dictionary:
                                    output_dictionary[xx[0]] = {}
                                aux_0_1 = output_dictionary[xx[0]][xx[1]]
                                for ll,kk in enumerate(structure_indices):
                                    aux_0_1[kk]=distances[ll,aa]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[1]))
                            for aa,xx in enumerate(zip(atom_indices, atom_indices_2)):
                                if xx[0] not in output_dictionary:
                                    output_dictionary[xx[0]] = {}
                                aux_0_1 = output_dictionary[xx[0]][xx[1]]
                                for ll,kk in enumerate(structure_indices):
                                    aux_0_1[kk]={}
                                    aux_0_1_kk=aux_0_1[kk]
                                    for mm,nn in enumerate(structure_indices_2):
                                        aux_0_1_kk[nn]=distances[ll,mm,aa]

                elif output_indices == 'group':

                    raise NotImplementedError()

        else:

            if output_indices is None:
                output_indices = 'atom'
            
            if output_indices is not None:

                if output_indices == 'selection': # works also with center of atoms
                    if output_structure_indices is None:
                        for ii in range(distances.shape[-2]):
                            output_dictionary[ii] = {jj:distances[:,ii,jj] for jj in range(distances.shape[-1])}
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for ii in range(distances.shape[-2]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for jj in range(distances.shape[-1]):
                                    aux_ii[jj] = {}
                                    aux_ii_jj = aux_ii[jj]
                                    for ll,kk in enumerate(structure_indices):
                                        kk = ll
                                        aux_ii_jj[kk]=distances[ll,ii,jj]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[0]))
                            for ii in range(distances.shape[-2]):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                for jj in range(distances.shape[-1]):
                                    aux_ii[jj] = {}
                                    aux_ii_jj = aux_ii[jj]
                                    for ll,kk in enumerate(structure_indices):
                                        nn = ll
                                        kk = ll
                                        aux_ii_jj[kk]={}
                                        aux_ii_jj_kk = aux_ii_jj[kk]
                                        aux_ii_jj_kk[nn]=distances[ll,ii,jj]

                elif output_indices == 'atom':
                    if output_structure_indices is None:
                        for aa,ii in enumerate(atom_indices):
                            output_dictionary[ii] = {}
                            aux_ii = output_dictionary[ii]
                            if atom_indices_2 is None:
                                for bb,jj in enumerate(atom_indices):
                                    aux_ii[jj] = distances[:,aa,bb]
                            else:
                                for bb,jj in enumerate(atom_indices_2):
                                    aux_ii[jj] = distances[:,aa,bb]
                    else:
                        if is_all(structure_indices):
                            structure_indices = list(range(distances.shape[0]))
                        if structure_indices_2 is None:
                            for aa,ii in enumerate(atom_indices):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                if atom_indices_2 is None:
                                    for bb,jj in enumerate(atom_indices):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            aux_ii_jj[kk]=distances[ll,aa,bb]
                                else:
                                    for bb,jj in enumerate(atom_indices_2):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            aux_ii_jj[kk]=distances[ll,aa,bb]
                        else:
                            if is_all(structure_indices_2):
                                structure_indices_2 = list(range(distances.shape[1]))
                            for aa,ii in enumerate(atom_indices):
                                output_dictionary[ii] = {}
                                aux_ii = output_dictionary[ii]
                                if atom_indices_2 is None:
                                    for bb,jj in enumerate(atom_indices):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            aux_ii_jj[kk]=distances[ll,aa,bb]
                                else:
                                    for bb,jj in enumerate(atom_indices_2):
                                        aux_ii[jj] = {}
                                        aux_ii_jj = aux_ii[jj]
                                        for ll,kk in enumerate(structure_indices):
                                            nn=structure_indices_2[ll]
                                            aux_ii_jj[kk] = {}
                                            aux_ii_jj_kk=aux_ii_jj[kk]
                                            aux_ii_jj_kk[nn]=distances[ll,aa,bb]

                elif output_indices == 'group':

                    raise NotImplementedError()

        output = output_dictionary

    return output


def _get_distances_in_memory(molecular_system, selection="all", structure_indices="all",
        center_of_atoms=False, weights=None,
        molecular_system_2=None, selection_2=None, structure_indices_2=None,
        center_of_atoms_2=False, weights_2=None,
        pairs=False, pbc=True, syntax='MolSysMT'):

    from molsysmt.basic import get
    from .get_center import get_center

    print(selection, selection_2, pairs, pbc)

    if center_of_atoms:

        coordinates = get_center(molecular_system, selection=selection,
                structure_indices=structure_indices, weights=weights)

    else:

        coordinates = get(molecular_system, element='atom', selection=selection,
                          structure_indices=structure_indices, syntax=syntax,
                          coordinates=True)

    if center_of_atoms_2:

        if molecular_system_2 is None:

            molecular_system_2 = molecular_system

        if structure_indices_2 is None:

            structure_indices_2 = structure_indices

        coordinates_2 = get_center(molecular_system_2, selection=selection_2,
            structure_indices=structure_indices_2, weights=weights_2)

    else:

        if (selection_2 is None) and (structure_indices_2 is None):

            if molecular_system_2 is None:

                coordinates_2 = None

            else:

                structure_indices_2 = structure_indices
                selection_2 = selection

                coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                                    structure_indices=structure_indices_2, syntax=syntax,
                                    coordinates=True)

        else:

            if structure_indices_2 is None:

                structure_indices_2 = structure_indices

            if selection_2 is None:

                selection_2 = selection

            if molecular_system_2 is None:

                molecular_system_2 = molecular_system

            coordinates_2 = get(molecular_system_2, element='atom', selection=selection_2,
                                structure_indices=structure_indices_2, syntax=syntax,
                                coordinates=True)

    if not pairs:

        if coordinates_2 is None:

            coordinates, length_unit = puw.get_value_and_unit(coordinates)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
                        box = puw.get_value(box, to_unit=length_unit)
                        distances = msmlib.structure.get_mic_distances_single_system(coordinates,
                                    box)
                        del(coordinates, box)
                    else:
                        pbc = False
                else:
                    pbc = False

            if not pbc:
                distances = msmlib.structure.get_distances_single_system(coordinates)
                del(coordinates)

            distances = puw.quantity(distances, length_unit)

        else:

            coordinates, length_unit = puw.get_value_and_unit(coordinates)
            coordinates_2 = puw.get_value(coordinates_2, to_unit=length_unit)

            if pbc:
                box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
                if box is not None:
                    if box[0] is not None:
                        box = puw.get_value(box, to_unit=length_unit)
                        distances = msmlib.structure.get_mic_distances(coordinates,
                                    coordinates_2, box)
                        del(coordinates, coordinates_2, box)
                    else:
                        pbc = False
                else:
                    pbc = False

            if not pbc:
                distances = msmlib.structure.get_distances(coordinates, coordinates_2)
                del(coordinates, coordinates_2)

            distances = puw.quantity(distances, length_unit)

    else: # coordinates_2 is always not None

        #if coordinates_2 is None:

        #    coordinates, length_unit = puw.get_value_and_unit(coordinates)

        #    if pbc:
        #        box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
        #        if box is not None:
        #            if box[0] is not None:
        #                box = puw.get_value(box, to_unit=length_unit)
        #                distances = msmlib.structure.get_mic_distances_pairs_single_system(coordinates,
        #                            box)
        #                del(coordinates, box)
        #            else:
        #                pbc = False
        #        else:
        #            pbc = False

        #    if not pbc:
        #        distances = msmlib.structure.get_distances_pairs_single_system(coordinates)
        #        del(coordinates)

        #    distances = puw.quantity(distances, length_unit)

        #else:

        coordinates, length_unit = puw.get_value_and_unit(coordinates)
        coordinates_2 = puw.get_value(coordinates_2, to_unit=length_unit)

        if pbc:
            box = get(molecular_system, element='system', structure_indices=structure_indices, box=True)
            if box is not None:
                if box[0] is not None:
                    box = puw.get_value(box, to_unit=length_unit)
                    distances = msmlib.structure.get_mic_distances_pairs(coordinates,
                                coordinates_2, box)
                    del(coordinates, coordinates_2, box)
                else:
                    pbc = False
            else:
                pbc = False

        if not pbc:
            distances = msmlib.structure.get_distances_pairs(coordinates, coordinates_2)
            del(coordinates, coordinates_2)

        distances = puw.quantity(distances, length_unit)

    distances = puw.standardize(distances)

    gc.collect()

    return distances


