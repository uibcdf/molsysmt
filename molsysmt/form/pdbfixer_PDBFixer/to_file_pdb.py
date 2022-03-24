from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import WrongFormError, WrongAtomIndicesError
from molsysmt._private.atom_indices import digest_atom_indices

def to_file_pdb(item, atom_indices='all', output_filename=None, check=True):

    if check:

        try:
            is_pdbfixer_PDBFixer(item)
        except:
            raise WrongFormError('pdbfixer.PDBFixer')

        try:
            atom_indices = digest_atom_indices(atom_indices)
        except:
            raise WrongAtomIndicesError()

    from . import to_openmm_Topology
    from . import get_coordinates_from_atom, get_box_from_atom
    from ..openmm_Topology import to_file_pdb as openmm_Topology_to_file_pdb

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices, check=False)
    coordinates = get_coordinates_from_atom(tmp_item, atom_indices=atom_indices, check=False)
    box = get_box_from_atom(tmp_item, check=False)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, box=box,
                                           output_filename=output_filename, check=False)

    return tmp_item


