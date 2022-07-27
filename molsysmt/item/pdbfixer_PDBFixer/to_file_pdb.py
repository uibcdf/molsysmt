from .is_pdbfixer_PDBFixer import is_pdbfixer_PDBFixer
from molsysmt._private.exceptions import *
from molsysmt._private.digestion import *

def to_file_pdb(item, atom_indices='all', output_filename=None):

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

    tmp_item = to_openmm_Topology(item, atom_indices=atom_indices)
    coordinates = get_coordinates_from_atom(tmp_item, atom_indices=atom_indices)
    box = get_box_from_atom(tmp_item)
    tmp_item = openmm_Topology_to_file_pdb(tmp_item, coordinates=coordinates, box=box,
                                           output_filename=output_filename)

    return tmp_item


