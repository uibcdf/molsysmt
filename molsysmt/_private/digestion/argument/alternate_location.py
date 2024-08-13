import numpy as np
from ...exceptions import ArgumentError

functions_where_boolean = (
    'molsysmt.basic.get.get',
    'molsysmt.basic.compare.compare',
    'molsysmt.basic.iterator.__init__',
    '.iterators.__init__'
    )

def digest_alternate_location(alternate_location, caller=None):

    from .location_id import digest_location_id
    from .occupancy import digest_occupancy
    from .b_factor import digest_b_factor
    from .atom_id import digest_atom_id
    from .coordinates import digest_coordinates

    if caller is not None:

        if caller.endswith(functions_where_boolean):
            if isinstance(alternate_location, bool):
                return alternate_location
            else:
                raise ArgumentError('alternate_location', value=alternate_location, caller=caller, message=None)


    if alternate_location is None:
        return None

    if isinstance(alternate_location, dict):
        alternate_location = [alternate_location]

    if isinstance(alternate_location, (tuple, list)):
        right_format=True
        for aux_alternate_location in alternate_location:
            for aux_atom_index, aux_dict in aux_alternate_location.items():
                if not isinstance(aux_atom_index, (int, np.int64)):
                    right_format=False
                    break
                try:
                    aux_dict['location_id']=digest_location_id(aux_dict['location_id'])
                    n_atoms = aux_dict['location_id'].shape[0]
                    aux_dict['occupancy']=digest_occupancy(aux_dict['occupancy'])[0]
                    aux_dict['b_factor']=digest_b_factor(aux_dict['b_factor'])[0]
                    aux_dict['atom_id']=digest_atom_id(aux_dict['atom_id'])
                    aux_dict['coordinates']=digest_coordinates(aux_dict['coordinates'])[0]
                    if aux_dict['occupancy'] is not None:
                        if aux_dict['occupancy'].shape[0]!=n_atoms:
                            right_format=False
                            break
                    if aux_dict['b_factor'] is not None:
                        if aux_dict['b_factor'].shape[0]!=n_atoms:
                            right_format=False
                            break
                    if aux_dict['atom_id'] is not None:
                        if len(aux_dict['atom_id'])!=n_atoms:
                            right_format=False
                            break
                    if aux_dict['coordinates'] is not None:
                        if aux_dict['coordinates'].shape[0]!=n_atoms:
                            right_format=False
                            break
                except:
                    right_format=False
                    break
        if right_format:
            return alternate_location

    raise ArgumentError('alternate_location', value=alternate_location, caller=caller, message=None)

