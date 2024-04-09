from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt.element.atom import get_atom_type_from_atom_name
import numpy as np

@digest(form='file:psf')
def to_molsysmt_Topology(item, atom_indices='all', skip_digestion=False):

    from .to_openmm_CharmmPsfFile import to_openmm_CharmmPsfFile
    from ..openmm_CharmmPsfFile import to_molsysmt_Topology as openmm_CharmmPsfFile_to_molsysmt_Topology

    tmp_item = to_openmm_CharmmPsfFile(item, skip_digestion=True)
    tmp_item = openmm_CharmmPsfFile_to_molsysmt_Topology(tmp_item, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

