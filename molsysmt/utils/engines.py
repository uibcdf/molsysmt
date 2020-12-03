from .exceptions import *

_engines={
    'amber' : 'Amber',
    'pdbfixer' : 'PDBFixer',
    'openmm' : 'OpenMM',
    'mdtraj' : 'MDTraj',
    'leap' : 'LEaP',
    'modeller' : 'Modeller',
    'molsysmt' : 'MolSysMT',
    'openpocket' : 'OpenPocket',
    'nglview' : 'NGLView'
}

def digest(engine):

    try:
        return _engines[engine.lower()]
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolSysMT')

