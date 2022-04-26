from ..exceptions import *

engines = [
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

engines_from_lowercase={ ii.lower() : ii for ii in engines }

def digest_engine(engine):

    try:
        return engines_from_lowercase[engine.lower()]
    except:
        raise BadCallError()

