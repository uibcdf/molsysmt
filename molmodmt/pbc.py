from .utils.engines import digest as _digest_engines
from .utils.forms import digest as _digest_forms
from molmodmt.lib import box as _libbox
import numpy as _np

def minimum_image_convention(item, selection='all', reference_selection=None,
                             syntaxis='MDTraj', engine='MolModMT'):

    from molmodmt import convert, select, get
    from molmodmt.utils.math import serialized_lists
    from molmodmt.centers import geometrical_center

    syntaxis = _digest_engines(syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = convert(item, engine)

    if engine=='MolModMT':

        molecules = get(tmp_item, molecules=True)

        if selection not in [None, 'all']:
            atom_indices = select(tmp_item, selection, syntaxis)
            working_molecules = []
            for molecule in molecules:
                if len(_np.intersect1d(molecule, atom_indices)):
                    working_molecules.append(molecule)
            molecules=working_molecules

        molecules_serialized = serialized_lists(molecules, fortran=True, dtype='int64')

        reference_coordinates = geometrical_center(tmp_item, selection=reference_center_selection,
                                                   syntaxis=syntaxis, engine=engine)

        aux = tmp_item.trajectory
        aux.coordinates=_np.asfortranarray(aux.coordinates, dtype='float64')
        aux.box=_np.asfortranarray(aux.box, dtype='float64')
        aux.invbox=_np.asfortranarray(aux.invbox, dtype='float64')

        _libbox.minimum_image_convention(aux.coordinates, molecules_serialized.values,
                       molecules_serialized.starts, reference_coordinates,
                       aux.box, aux.invbox, aux.orthogonal,
                       aux.n_frames, aux.n_atoms,
                       molecules_serialized.n_values, molecules_serialized.n_starts,
                       atom_indices_reference.shape[0])

        aux.coordinates=_np.ascontiguousarray(aux.coordinates)
        aux.box=_np.ascontiguousarray(aux.box)
        aux.invbox=_np.ascontiguousarray(aux.invbox)

        out_item = convert(tmp_item, form_out)
        del(tmp_item, aux, molecules, molecules_serialized)

        return out_item

    else:

        raise NotImplementedError

def unwrap_molecules_from_pbc_cell(item, selection='all', syntaxis='MDTraj', engine='MolModMT'):

    from molmodmt import convert, select, get, set, duplicate
    from molmodmt.utils.math import serialized_lists

    atom_indices = select(item, selection=selection, syntaxis=syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = duplicate(item)


    if engine=='MolModMT':

        molecules = get(tmp_item, element='atom', indices=atom_indices, molecules=True)
        molecules_serialized = serialized_lists(molecules, dtype='int64')

        bonded_atoms = get(tmp_item, element='atom', indices=atom_indices, bonded_atoms=True)
        bonded_atoms_serialized = serialized_lists(bonds, dtype='int64')

        coordinates, box = get(tmp_item, coordinates=True, box=True, frame_indices='all') 

        length_units = coordinates.unit
        coordinates = _np.asfortranarray(coordinates._value, dtype='float64')
        box = _np.asfortranarray(box._value, dtype='float64')

        _libbox.unwrap(aux.coordinates, molecules_serialized.values,
                       molecules_serialized.starts, bonds_serialized.values, bonds_serialized.starts,
                       aux.box, aux.invbox, aux.orthogonal,
                       aux.n_frames, aux.n_atoms,
                       molecules_serialized.n_values, molecules_serialized.n_starts,
                       bonds_serialized.n_values, bonds_serialized.n_starts)

        coordinates=_np.ascontiguousarray(coordinates)*length_units
        box=_np.ascontiguousarray(aux.box)*length_units

        set(tmp_item, coordinates=coordinates, box=box)

        del(coordinates, box, molecules, molecules_serialized, bonds, bonds_serialized)

        return out_item

    else:

        raise NotImplementedError

def wrap_molecules_to_pbc_cell(self):
    #self.coors=asfortran_np.array(self.coors)
    #libbox.wrap_all_inplace(self.coors,self.box,self.invbox,self.orthogonal,self.coors.shape[0])
    #self.coors=ascontiguous_np.array(self.coors)
    raise NotImplementedError

