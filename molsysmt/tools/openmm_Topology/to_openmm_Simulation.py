from molsysmt.tools.pdbfixer_PDBFixer.is_openmm_Topology import is_openmm_Topology
from molsysmt._private_tools.exceptions import WrongFormError, WrongAtomIndicesError, WrongCoordinatesError
from molsysmt._private_tools.atom_indices import digest_atom_indices, digest_coordinates

def to_openmm_Simulation(item, atom_indices='all', check=True):

    if check:

        try:
            is_openmm_Topology(item)
        except:
            raise WrongFormError('openmm.Topology')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

        try:
            coordinates = digest_coordinates(coordinates)
        except:
            raise WrongCoordinatesError()

    from molsysmt.tools.openmm_Topology import to_openmm_System as openmm_Topology_to_openmm_System
    from molsysmt.tools.openmm_System import to_openmm_Simulation as openmm_System_to_openmm_Simulation

    tmp_item = openmm_Topology_to_openmm_System(item, atom_indices=atom_indices, check=False)
    tmp_item = openmm_System_to_openmm_Simulation(tmp_item, check=False)

    return tmp_item


