from .utils.engines import digest as _digest_engines
from .utils.forms import digest as _digest_forms
from molmodmt.lib import box as _libbox
import numpy as _np

def minimum_image_convention(item, selection='all', reference_selection=None, syntaxis='MDTraj',
                             engine='MolModMT'):

    from molmodmt import convert, select, get
    from molmodmt.math import serialize_list_of_lists

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

        molecules_array_all, molecules_array_starts = serialize_list_of_lists(molecules,
                                                                              fortran=True,
                                                                              dtype='int64')

        atom_indices_reference = select(tmp_item, reference_selection, syntaxis)

        aux = tmp_item.trajectory
        aux.coordinates=_np.asfortranarray(aux.coordinates, dtype='float64')
        aux.box=_np.asfortranarray(aux.box, dtype='float64')
        aux.invbox=_np.asfortranarray(aux.invbox, dtype='float64')

        _libbox.minimum_image_convention(aux.coordinates, molecules_array_all,
                       molecules_array_starts, atom_indices_reference,
                       aux.box, aux.invbox, aux.orthogonal,
                       aux.n_frames, aux.n_atoms,
                       molecules_array_all.shape[0], molecules_array_starts.shape[0],
                       atom_indices_reference.shape[0])

        aux.coordinates=_np.ascontiguousarray(aux.coordinates)
        aux.box=_np.ascontiguousarray(aux.box)
        aux.invbox=_np.ascontiguousarray(aux.invbox)

        return convert(tmp_item, form_out)

    else:

        raise NotImplementedError

def unwrap_molecules(self, selection='all', reference_selection=None, syntaxis='mdtraj'):

    from molmodmt import convert, select, get
    from molmodmt.math import serialize_list_of_lists

    syntaxis = _digest_engines(syntaxis)
    engine = _digest_engines(engine)
    form_in, form_out = _digest_forms(item, engine)
    tmp_item = convert(item, engine)

    if engine=='MolModMT':

        molecules, bonds = get(tmp_item, molecules=True, bonded_atoms=True)

        if selection not in [None, 'all']:
            atom_indices = _select(self.topology, selection, syntaxis)
            working_molecules = []
            for molecule in molecules:
                if len(_np.intersect1d(molecule, atom_indices)):
                    working_molecules.append(molecule)
            molecules=working_molecules

        molecules_array_all, molecules_array_starts = serialize_list_of_lists(molecules,
                                                                              fortran=True,
                                                                              dtype='int64')

        bonds_array_all, bonds_array_starts = serialize_list_of_lists(bonds, fortran=True,
                                                                      dtype='int64')


        aux = self.trajectory
        aux.coordinates=_np.asfortranarray(aux.coordinates, dtype='float64')
        aux.box=_np.asfortranarray(aux.box, dtype='float64')
        aux.invbox=_np.asfortranarray(aux.invbox, dtype='float64')

        _libbox.unwrap(aux.coordinates, molecules_array_all,
                       molecules_array_starts, bonds_array_all, bonds_array_starts,
                       aux.box, aux.invbox, aux.orthogonal,
                       aux.n_frames, aux.n_atoms,
                       molecules_array_all.shape[0], molecules_array_starts.shape[0],
                       bonds_array_all.shape[0], bonds_array_starts.shape[0])

        aux.coordinates=_np.ascontiguousarray(aux.coordinates)
        aux.box=_np.ascontiguousarray(aux.box)
        aux.invbox=_np.ascontiguousarray(aux.invbox)

        return convert(tmp_item, form_out)

    else:

        raise NotImplementedError

def wrap_molecules(self):
    #self.coors=asfortran_np.array(self.coors)
    #libbox.wrap_all_inplace(self.coors,self.box,self.invbox,self.orthogonal,self.coors.shape[0])
    #self.coors=ascontiguous_np.array(self.coors)
    raise NotImplementedError

