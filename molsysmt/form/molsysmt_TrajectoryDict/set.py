from molsysmt import pyunitwizard as _puw
from molsysmt._private.variables import is_all as _is_all

def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    length_unit = _puw.get_unit(item['coordinates'])
    value = _puw.convert(value, to_unit=length_unit)

    if _is_all(indices):
        if _is_all(structure_indices):
            item['coordinates']=value
        else:
            item['coordinates'][structure_indices,:,:]=value
    else:
        if _is_all(structure_indices):
            item['coordinates'][:,indices,:]=value
        else:
            item['coordinates'][np.ix_(indices,structure_indices)]=value

    pass


