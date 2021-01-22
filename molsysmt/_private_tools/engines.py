from .exceptions import BadCallError

list_engines = [
    'Amber',
    'PDBFixer',
    'OpenMM',
    'MDTraj',
    'LEaP',
    'Modeller',
    'MolSysMT',
    'OpenPocket',
    'NGLView',
]

_aux={ ii.lower : ii for ii in list_engines }

def digest_engine(engine):

    try:
        return _aux[engine.lower()]
    except:
        raise BadCallError('Wrong way of invoking this method. Either the engine is not implemented, either is mispelled.\n\
                           Check the online documentation  for more information: http://www.uibcdf.org/MolSysMT')

