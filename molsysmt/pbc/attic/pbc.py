from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from molsysmt.lib import box as libbox
import numpy as np
from molsysmt import puw

#def minimum_image_convention(item, selection='all', reference_selection=None,
#                             reference_coordinates=None, center_of_selection='geometrical_center',
#                             center_of_reference_selection='geometrical_center', structure_indices='all',
#                             syntaxis='MDTraj', engine='MolSysMT'):
#
#    from molsysmt import convert, select, get, duplicate
#    from molsysmt import set as _set
#    from molsysmt.tools.math import serialized_lists
#    from molsysmt.centers import geometrical_center
#
#    n_atoms, n_structures = get(item, n_atoms=True, n_structures=True)
#    atom_indices = select(item, selection=selection, syntaxis=syntaxis)
#    n_atom_indices = len(atom_indices)
#    structure_indices = _digest_structure_indices(item, structure_indices)
#    n_structure_indices = len(structure_indices)
#
#    engine = _digest_engines(engine)
#    form_in, _ = _digest_forms(item, engine)
#    tmp_item = duplicate(item)
#
#    if engine=='MolSysMT':
#
#        if reference_coordinates is None:
#            if center_of_reference_selection == 'geometrical_center':
#                reference_coordinates = geometrical_center(tmp_item, selection=reference_selection,
#                                                        structure_indices=structure_indices, syntaxis=syntaxis, engine=engine)
#
#        molecules = get(tmp_item, molecules=True)
#
#        if selection not in [None, 'all']:
#            working_molecules = []
#            for molecule in molecules:
#                if len(_np.intersect1d(molecule, atom_indices)):
#                    working_molecules.append(molecule)
#            molecules=working_molecules
#
#        molecules_serialized = serialized_lists(molecules, dtype='int64')
#
#        if center_of_selection == 'geometrical_center':
#            centers_molecules = geometrical_center(tmp_item, selection_groups=molecules,
#                    structure_indices=structure_indices, syntaxis=syntaxis, engine=engine)
#
#        coordinates, box, box_shape = get(tmp_item, coordinates=True, box=True, box_shape=True, structure_indices='all')
#
#        units = puw.get_unit(coordinates)
#        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
#        reference_coordinates = np.asfortranarray(puw.get_value(reference_coordinates), dtype='float64')
#        box = np.asfortranarray(puw.get_value(box), dtype='float64')
#        orthogonal = 0
#        if box_shape=='cubic': orthogonal = 1
#
#        libbox.minimum_image_convention(coordinates, reference_coordinates, centers_molecules,
#                molecules_serialized.indices, molecules_serialized.values,
#                molecules_serialized.starts, structure_indices, box, orthogonal,
#                n_structures, n_atoms, molecules_serialized.n_indices, molecules_serialized.n_values,
#                n_structure_indices)
#
#        coordinates=np.ascontiguousarray(coordinates)*units
#
#        _set(tmp_item, coordinates=coordinates)
#
#        del(coordinates, box, length_units)
#        del(molecules, molecules_serialized)
#
#        return tmp_item
#
#    else:
#
#        raise NotImplementedError

#def keep_compact_molecules_in_pbc(item, selection='all', structure_indices='all', syntaxis='MDTraj', engine='MolSysMT'):
#
#    from molsysmt import convert, select, get, duplicate
#    from molsysmt import set as _set
#    from molsysmt.tools.math import serialized_lists
#
#    n_atoms, n_structures = get(item, n_atoms=True, n_structures=True)
#    atom_indices = select(item, selection=selection, syntaxis=syntaxis)
#    n_atom_indices = len(atom_indices)
#    structure_indices = _digest_structure_indices(item, structure_indices)
#    n_structure_indices = len(structure_indices)
#
#    engine = _digest_engines(engine)
#    form_in, _ = _digest_forms(item, engine)
#    tmp_item = duplicate(item)
#
#    if engine=='MolSysMT':
#
#        molecules = get(tmp_item, molecules=True)
#
#        if selection not in [None, 'all']:
#            working_molecules = []
#            for molecule in molecules:
#                if len(_np.intersect1d(molecule, atom_indices)):
#                    working_molecules.append(molecule)
#            molecules=working_molecules
#
#        molecules_serialized = serialized_lists(molecules, dtype='int64')
#
#        bonded_atoms = get(tmp_item, element='atom', indices=atom_indices, bonded_atoms=True)
#        bonded_atoms_serialized = serialized_lists(bonded_atoms, dtype='int64')
#
#        coordinates, box, box_shape = get(tmp_item, coordinates=True, box=True, box_shape=True, structure_indices='all')
#
#        units = puw.get_unit(coordinates)
#        coordinates = np.asfortranarray(puw.get_value(coordinates), dtype='float64')
#        box = np.asfortranarray(puw.get_value(box), dtype='float64')
#        orthogonal = 0
#        if box_shape=='cubic': orthogonal = 1
#
#        libbox.unwrap(coordinates, molecules_serialized.indices, molecules_serialized.values, molecules_serialized.starts,
#                       bonded_atoms_serialized.indices, bonded_atoms_serialized.values, bonded_atoms_serialized.starts,
#                       structure_indices, box, orthogonal, n_structures, n_atoms,
#                       molecules_serialized.n_indices, molecules_serialized.n_values,
#                       bonded_atoms_serialized.n_indices, bonded_atoms_serialized.n_values,
#                       n_structure_indices)
#
#        coordinates=_np.ascontiguousarray(coordinates)*units
#
#        _set(tmp_item, coordinates=coordinates)
#
#        del(coordinates, box, length_units)
#        del(molecules, molecules_serialized, bonded_atoms, bonded_atoms_serialized)
#
#        return tmp_item
#
#    else:
#
#        raise NotImplementedError


