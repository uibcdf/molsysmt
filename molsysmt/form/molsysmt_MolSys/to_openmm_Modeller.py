from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *
from .is_molsysmt_MolSys import is_molsysmt_MolSys

def to_openmm_Modeller(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        try:
            is_molsysmt_MolSys(item)
        except:
            raise WrongFormError('molsysmt.MolSys')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    try:
        from openmm.app import Modeller
    except:
        raise LibraryNotFound(openmm)

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom
    from molsysmt import puw

    tmp_topology = to_openmm_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_positions = get_coordinates_from_atom(item, indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_positions = puw.convert(tmp_positions, to_form='openmm.unit')

    tmp_item = Modeller(tmp_topology, tmp_positions[0])

    return tmp_item

