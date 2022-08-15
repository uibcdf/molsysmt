from molsysmt._private.digestion import digest
from .water import is_water
from .ion import is_ion
from .cosolute import is_cosolute
from .small_molecule import is_small_molecule
from .aminoacid import is_aminoacid
from .terminal_capping import is_terminal_capping
from .nucleotide import is_nucleotide
from .lipid import is_lipid
from .saccharide import is_saccharide

@digest()
def get_group_type_from_group_name(group_name):

    output = None

    if is_water(group_name):
        output = 'water'
    elif is_ion(group_name):
        output = 'ion'
    elif is_cosolute(group_name):
        output = 'cosolute'
    elif is_small_molecule(group_name):
        output = 'small molecule'
    elif is_aminoacid(group_name):
        output = 'aminoacid'
    elif is_terminal_capping(group_name):
        output = 'terminal capping'
    elif is_nucleotide(group_name):
        output = 'nucleotide'
    elif is_lipid(group_name):
        output = 'lipid'
    elif is_saccharide(group_name):
        output = 'saccharide'

    return output

