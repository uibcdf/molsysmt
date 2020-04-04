from .exceptions import *

_parser={
    'molsysmt' : 'MolSysMT',
    'amber' : 'Amber',
    'mdanalysis' : 'MDAnalysis',
    'mdtraj' : 'MDTraj',
    'parmed' : 'ParmEd'
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

