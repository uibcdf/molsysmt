from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.Topology')
def add_bonds(item, bonded_atom_pairs, skip_digestion=False):

    item.add_bonds(bonded_atom_pairs, skip_digestion=True)

