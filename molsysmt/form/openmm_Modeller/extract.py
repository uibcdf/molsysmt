from .is_openmm_Modeller import is_openmm_Modeller
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError, WrongStructureIndicesError
from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.atom_indices import digest_atom_indices
from molsysmt._private.structure_indices import digest_structure_indices

def extract(item, atom_indices='all', structure_indices='all', copy_if_all=True, check=True):

    if check:

        try:
            is_openmm_Modeller(item)
        except:
            raise WrongFormError('openmm.Modeller')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()


    from openmm.app import Modeller

    if (atom_indices is 'all') and (structure_indices is 'all'):


        tmp_item = Modeller(item.topology, item.positions)

    else:

        from . import get_coordinates_from_atom
        from ..openmm_Topology import extract as extract_openmm_Topology

        tmp_topology = extract_openmm_Topology(item.topology, atom_indices=atom_indices)
        tmp_positions = get_coordinates_from_atom(item, indices=atom_indices)
        tmp_item = Modeller(tmp_topology, tmp_positions)

    return tmp_item

