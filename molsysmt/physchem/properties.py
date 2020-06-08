def get_masses(item, target ='atom', selection = 'all'):

    from mendeleev import element
    from molsysmt import get
    from simtk import unit

    atom_types = get(item, target = 'atom', selection = selection, type = True)

    output = []

    for ii in atom_types:
        var_aux = element(ii).atomic_weight
        output.append(var_aux*unit.amu)

    return output

def get_radii(item, target = 'atom', selection = 'all', radius_type = 'vdw'):

    from mendeleev import element
    from molsysmt import get
    from simtk import unit

    atom_types = get(item, target = 'atom', selection = selection, type = True)

    output = []

    for ii in atom_types:
        var_aux = element(ii).vdw_radius
        output.append(var_aux*unit.picometers)

    return output
