from os.path import basename as _basename
from os import remove as _remove
from MDAnalysis.coordinates.CRD import CRDReader as _mdanalysis_coordinates_CRDReader

form_name=_basename(__file__).split('.')[0].replace('api_','').replace('_','.')

is_form={
    _mdanalysis_coordinates_CRDReader : form_name,
    'mdanalysis.coordinates.CRDReader' : form_name
}

info=["",""]
with_topology=False
with_trajectory=True
with_parameters=False

def select_with_MDTraj(item, selection):

    raise NotImplementedError

def select_with_MDAnalysis(item, selection):

    raise NotImplementedError

def select_with_MolSysMT(item, selection):

    raise NotImplementedError

def extract(item, atom_indices='all', frame_indices='all'):

    if (atom_indices is 'all') and (frame_indices is 'all'):
        return item
    else:
        raise NotImplementedError

def copy(item):

    raise NotImplementedError

###### Get

## system

def get_form_from_system(item, indices='all', frame_indices='all'):

    return form_name

