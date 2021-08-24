"""
MolSysMT
This must be a short description of the project
"""

# Handle versioneer
from ._version import get_versions
versions = get_versions()
__version__ = versions['version']
__git_revision__ = versions['full-revisionid']
del get_versions, versions

__documentation_web__ = 'https://www.uibcdf.org/MolSysMT'
__github_web__ = 'https://github.com/uibcdf/MolSysMT'
__github_issues_web__ = __github_web__ + '/issues'

from ._pyunitwizard import puw as puw

#from . import tools

from . import demo_systems

from .native.molsys import MolSys
from .basic import select, extract, merge, add, concatenate_frames, append_frames, info, get, set, \
                       convert, copy, view, remove, get_form, contains, is_composed_of
from .info_basics import info_forms, info_convert, info_select, info_viewers

from .additional_remove import remove_solvent, remove_hydrogens
from .peptides import build_peptide
from .geometrical_transformations import translate
from .centers import get_geometric_center, get_center_of_mass, get_center, center
from .distances import distance, minimum_distance, maximum_distance, contact_map, neighbors
from .graphs import bondgraph
from .covalent import covalent_chains, covalent_blocks, covalent_dihedral_quartets
from .dihedral_angles import get_dihedral_angles, set_dihedral_angles, shift_dihedral_angles, ramachandran_angles
from .protonation import add_missing_hydrogens, has_hydrogens
from .terminals_capping import add_terminal_capping
from . import physico_chemical_properties as physchem
from .solvate_box import solvate, is_solvated
from .potential_energy import energy_minimization, potential_energy
from .sasa import sasa
from .rmsd import rmsd, least_rmsd, least_rmsd_fit
from . import hbonds
from .pbc import wrap_to_pbc, wrap_to_mic, unwrap

from .sequence import sequence_alignment, sequence_identity, structure_alignment
#from .radius_of_gyration import radius_of_gyration
#from .fix import fix_chains, fix
#from .model_loops import add_loop
#from .mutations import mutate
#from . import elements as elements
#from .pbc import minimum_image_convention,\
#        box_shape_from_box_angles, box_shape_from_box_vectors, box_lengths_from_box_vectors, box_angles_from_box_vectors,\
#        box_vectors_from_box_lengths_and_angles, box_volume_from_box_vectors
#from .pockets import alpha_spheres
#from . import physchem
#from . import nglview


# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all__ = []
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


