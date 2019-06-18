from .exceptions import *

_engines={
    'pdbfixer' : 'PDBFixer',
    'openmm' : 'OpenMM',
    'mdtraj' : 'MDTraj',
    'leap' : 'LEaP',
    'molmodmt' : 'MolModMT'
}

def digest(engine):

    try:
        return _engines[engine.lower()]
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolModMT')

