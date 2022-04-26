from .water import is_water
from .ion import is_ion
from .cosolute import is_cosolute
from .small_molecule import is_small_molecule
from .aminoacid import is_aminoacid
from .terminal_capping import is_terminal_capping
from .nucleotide import is_nucleotide
from .lipid import is_lipid

def get_group_type_from_group_name(name):

    output = None

    if is_water(name):
        output = 'water'
    elif is_ion(name):
        output = 'ion'
    elif is_cosolute(name):
        output = 'cosolute'
    elif is_small_molecule(name):
        output = 'small molecule'
    elif is_aminoacid(name):
        output = 'aminoacid'
    elif is_terminal_capping(name):
        output = 'terminal capping'
    elif is_nucleotide(name):
        output = 'nucleotide'
    elif is_lipid(name):
        output = 'lipid'

    return output

