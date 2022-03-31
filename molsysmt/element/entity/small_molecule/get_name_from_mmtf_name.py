from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

mmtf_translator = {

    '3-(2-BENZOTHIAZOLYLTHIO)-1-PROPANESULFONIC ACID' : '3-(2-benzothiazolylthio)-1-propanesulfonic acid',
    '3-{3,5-DIMETHYL-4-[3-(3-METHYL-ISOXAZOL-5-YL)-PROPOXY]-PHENYL}-5-TRIFLUOROMETHYL-[1,2,4]OXADIAZOLE' : '3-{3,5-dimethyl-4-[3-(3-methyl-isoxazol-5-yl)-propoxy]-phenyl}-5-trifluoromethyl-[1,2,4]oxadiazole',
    'octyl beta-D-glucopyranoside' : 'octyl beta-d-glucopyranoside',
    'MYRISTIC ACID': 'myristic acid',
    'DEXAMETHASONE' : 'dexamethasone',
    'ESTRADIOL' : 'estradiol',
    '2-HYDROXYETHYL DISULFIDE' : '2-hydroxyethyl disulfide',
    'BENZENE' : 'benzene',
    'NADPH DIHYDRO-NICOTINAMIDE-ADENINE-DINUCLEOTIDE PHOSPHATE': 'nadph dihydro-nicotinamide-adenine-dinucleotide phosphate',

    }

def get_name_from_mmtf_name(name):

    return mmtf_translator[name]
