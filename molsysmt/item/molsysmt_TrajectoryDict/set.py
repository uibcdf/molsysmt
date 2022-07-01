from molsysmt import puw as _puw

def set_coordinates_to_atom(item, indices='all', structure_indices='all', value=None):

    length_unit = _puw.get_unit(item['coordinates'])
    value = _puw.convert(value, to_unit=length_unit)

    if indices is 'all':
        if structure_indices is 'all':
            item['coordinates']=value
        else:
            item['coordinates'][structure_indices,:,:]=value
    else:
        if structure_indices is 'all':
            item['coordinates'][:,indices,:]=value
        else:
            item['coordinates'][np.ix_(indices,structure_indices)]=value

    pass


