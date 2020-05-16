from .exceptions import *

_parser={
    'molsysmt' : 'MolSysMT',
    'amber' : 'Amber',
    'mdanalysis' : 'MDAnalysis',
    'mdtraj' : 'MDTraj',
    'parmed' : 'ParmEd',
    'nglview' : 'NGLview'
}

def digest_syntaxis(syntaxis):

    try:
        syntaxis = _parser[syntaxis.lower()]
        return syntaxis
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolSysMT')


def digest(selection, syntaxis="MolSysMT"):

    syntaxis = digest_syntaxis(syntaxis)

    if syntaxis=='MolSysMT':

        selection=selection.replace('backbone','(atom.name==["CA", "N", "C", "O"])')

    #elif syntaxis=="MDTraj":

    return selection, syntaxis

def indices_to_syntaxis(item, indices, target='atom', to_syntaxis=None):

    output_string = ''

    if to_syntaxis=='NGLview':

        if target=='atom':
            output_string = '@'+','.join([str(ii) for ii in indices])
        elif target=='group':
            from molsysmt import get
            group_ids = get(item, target='group', indices=indices, group_id=True)
            output_string = ' '.join([str(ii) for ii in group_ids])
        elif target=='chain':
            from molsysmt import get
            chain_names = get(item, target='chain', indices=indices, chain_name=True)
            output_string = ' '.join([':'+ii for ii in chain_names])
        else:
            raise NotImplementedError

    else:

        raise NotImplementedError

    return output_string

