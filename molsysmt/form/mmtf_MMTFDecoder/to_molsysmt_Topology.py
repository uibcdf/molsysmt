from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest(form='mmtf.MMTFDecoder')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_molsysmt_MolSys import to_molsysmt_MolSys

    tmp_item = to_molsysmt_MolSys(item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item.topology

