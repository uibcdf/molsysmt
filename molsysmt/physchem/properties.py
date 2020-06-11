def get_masses(item, target ='atom', selection = 'all'):
    
    from .atoms.weight import weight as atomic_weight 
    from molsysmt import get
    from simtk import unit

    atom_types = get(item, target = 'atom', selection = selection, type = True)

    output = []

    for ii in atom_types:
        var_aux = atomic_weight[ii]
        output.append(var_aux*unit.amu)

    return output

def get_radii(item, target = 'atom', selection = 'all', radius_type = 'vdw'):

    from .atoms.vdw_radius import vdw as vdw_radius 
    from molsysmt import get
    from simtk import unit

    atom_types = get(item, target = 'atom', selection = selection, type = True)

    output = []

    for ii in atom_types:
        var_aux = vdw_radius[ii]
        output.append(var_aux*unit.picometers)

    return output

def get_polarity(item, target = 'group', selection = 'all', polarity_type = 'grantham'):

    from molsysmt import get
    from simtk import unit

    residue_types = get(item, target = 'residue', selection = selection, name = True)

    output = []

    if polarity_type == 'grantham':

        from .residues.polarity import grantham as polarity

    elif polarity_type == 'zimmerman':

        from .residues.polarity import zimmerman as polarity

    for ii in residue_types:
        var_aux = polarity[ii]
        output.append(var_aux)


    return output

def get_transmembrane_tendency(item, target = 'group', selection = 'all',
                               transmembrane_tendency_type = 'zhao'):

    from molsysmt import get
    from simtk import unit

    residue_types = get(item, target = 'residue', selection = selection, name = True)

    output = []

    if transmembrane_tendency_type == 'zhao':

        from .residues.transmembrane_tendency import zhao as transmembrane_tendency

    elif transmembrane_tendency_type == 'senes':

        from .residues.transmembrane_tendency import senes as transmembrane_tendency

    for ii in residue_types:
        var_aux = transmembrane_tendency[ii]
        output.append(var_aux)

    return output


