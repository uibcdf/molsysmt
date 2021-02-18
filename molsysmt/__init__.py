from .version import __version__
from ._pyunitwizard import puw as _puw
from ._private_tools import units as _u

from . import tools

from . import demo_systems

from .native.molsys import MolSys
from .multitool import select, extract, merge, concatenate, add, append, info, get, set, \
                       convert, copy, write, view, remove, get_form
from .info_multitool import info_forms, info_convert, info_select, info_viewers
from .geometrical_transformations import translate
from .rmsd import rmsd, least_rmsd, least_rmsd_fit, angular_rmsd
from .distances import distance, minimum_distance, maximum_distance, contact_map, neighbors_lists
from .centers import geometric_center, center_of_mass, center, recenter
from .sequence import sequence_alignment, sequence_identity, structure_alignment
from .radius_of_gyration import radius_of_gyration
from .fix import fix_chains, fix
from .model_loops import add_loop
from .remove_atoms import remove_solvent, remove_hydrogens
from .potential_energy import energy_minimization, potential_energy
from .peptides import build_peptide
from .solvate_box import solvate, is_solvated
from .protonation import add_missing_hydrogens
from .terminals_capping import add_terminal_capping
from .mutations import mutate
from . import elements as elements
from .chem_and_phys_properties import get_mass, get_net_mass, get_degrees_of_freedom
from .pbc import wrap_molecules_to_pbc_cell, unwrap_molecules_from_pbc_cell, minimum_image_convention,\
        box_shape_from_box_angles, box_shape_from_box_vectors, box_lengths_from_box_vectors, box_angles_from_box_vectors,\
        box_vectors_from_box_lengths_and_angles, box_volume_from_box_vectors
from .pockets import alpha_spheres
from .sasa import sasa
from .covalent import covalent_chains, covalent_blocks, covalent_dihedral_quartets
from .dihedral_angles import get_dihedral_angles, set_dihedral_angles, shift_dihedral_angles, ramachandran_angles
from .graphs import bondgraph
from . import physchem
from . import nglview


# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all__ = ['convert']
#__all__ = [
#    'convert', 'info', 'select', 'get', 'set', 'convert', 'copy', 'write', 'view', 'get_form',
#    'extract', 'remove',
#    'rmsd', 'least_rmsd', 'least_rmsd_fit',
#    'distance', 'maximum_distance', 'minimum_distance', 'contact_map', 'neighbors_lists',
#    'geometric_center', 'center_of_mass', 'center', 'recenter',
#    'radius_of_gyration',
#    'remove_solvent', 'remove_hydrogens',
#    'build_peptide',
#    'wrap_molecules_to_pbc_cell', 'unwrap_molecules_from_pbc_cell',
#    'minimum_image_convention', 'box_shape_from_box_angles', 'box_shape_from_box_vectors',
#    'box_lengths_from_box_vectors', 'box_angles_from_box_vectors', 'box_vectors_from_box_lengths_and_angles'
#          ]


