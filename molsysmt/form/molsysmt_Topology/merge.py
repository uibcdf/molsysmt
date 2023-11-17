from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np

@digest(form='molsysmt.TopologyNEW')
def merge(items, atom_indices='all'):

    raise NotImplementedError

