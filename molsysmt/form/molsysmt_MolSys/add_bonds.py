from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='molsysmt.MolSys')
def add_bonds(item, bonded_atom_pairs, skip_digestion=False):

    item.topology.add_bonds(bonded_atom_pairs, skip_digestion=True)

