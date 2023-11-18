from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
from molsysmt.element.atom import get_atom_type_from_atom_name
from molsysmt.element.group import get_group_type_from_group_name
import numpy as np

@digest(form='file:psf')
def to_molsysmt_TopologyOld(item, atom_indices='all'):

    from .to_openmm_CharmmPsfFile import to_openmm_CharmmPsfFile
    from ..openmm_CharmmPsfFile import to_molsysmt_TopologyOld as openmm_CharmmPsfFile_to_molsysmt_TopologyOld

    tmp_item = to_openmm_CharmmPsfFile(item)
    tmp_item = openmm_CharmmPsfFile_to_molsysmt_TopologyOld(tmp_item, atom_indices=atom_indices)

    return tmp_item

