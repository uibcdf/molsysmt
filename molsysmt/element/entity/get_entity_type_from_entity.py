from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
import numpy as np

def get_entity_type_from_entity(molecular_system, indices='all', check=True):

    if check:

        digest_single_molecular_system(molecular_system)
        indices = digest_indices(indices)

    raise NotImplementedError

