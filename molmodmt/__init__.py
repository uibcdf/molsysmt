
from . import utils

from .native.molmod import MolMod
from .multitool import select, extract, merge, info, get_form, get, set, load,\
                       convert, duplicate, write, view, reformat
from .info_converters import info_forms, info_load, info_convert, info_select, info_viewers
from .rmsd import rmsd, least_rmsd_fit
from .distances import distance, distance_atoms_pairs, min_distance, contact_map, neighbors_lists
from .centers import geometrical_center, center_of_mass, center, recenter
from .sequence import sequence_alignment, sequence_identity, structure_alignment
from .radius_of_gyration import radius_of_gyration
from .fix import fix_chains, fix_pdb_structure
from .model_loops import add_loop
from .remove_atoms import remove, remove_solvent, remove_hydrogens
from .potential_energy import energy_minimization
from .solvate_box import solvate
from .protonation import add_missing_hydrogens
from .mutations import mutate
from .topology import is_water, is_ion, is_aminoacid, is_nucleotide, residue_name_to_molecule_type
from .chem_and_phys_properties import get_charge, get_net_charge, get_mass, get_net_mass,\
                               get_degrees_of_freedom
from .pbc import wrap_molecules_to_pbc_cell, unwrap_molecules_from_pbc_cell, minimum_image_convention

# With the following list sphinx can document de methods in the api section without adding the
# module files names explicitly:

__all_multitool__ = ['select', 'extract', 'merge', 'info', 'get_form', 'get', 'set', 'load',
                    'convert', 'duplicate', 'write', 'view', 'reformat']
__all_info_converters__ = ['info_forms', 'info_load', 'info_convert', 'info_select', 'info_viewers']
__all_rmsd__ = ['rmsd', 'least_rmsd_fit']
__all_distances__ = ['distance', 'distance_atoms_pairs', 'min_distance', 'contact_map',
                     'neighbors_lists']
__all_centers__ = ['geometrical_center', 'center_of_mass', 'center', 'recenter']
__all_sequence__ = ['sequence_alignment', 'sequence_identity', 'structure_alignment']
__all_radius_of_gyration__ = ['radius_of_gyration']
__all_fix__ = ['fix_chains', 'fix_pdb_structure']
__all_model_loops__ = ['add_loop']
__all_remove_atoms__ = ['remove', 'remove_solvent', 'remove_hydrogens']
__all_potential_energy__ = ['energy_minimization']
__all_solvate_box__ = ['solvate']
__all_protonation__ = ['add_missing_hydrogens']
__all_mutations__ = ['mutate']
__all_topology__ = ['is_water', 'is_ion', 'is_aminoacid', 'is_nucleotide',
                    'residue_name_to_molecule_type']
__all_chem_and_phys_properties__ = ['get_charge', 'get_net_charge', 'get_mass', 'get_net_mass',
                                    'get_degrees_of_freedom']
__all_pbc__ = ['wrap_molecules', 'unwrap_molecules', 'minimum_image_convention']

__all__ = __all_multitool__ + __all_info_converters__ + __all_rmsd__ + __all_distances__ +\
        __all_centers__ + __all_sequence__ + __all_radius_of_gyration__ + __all_fix__ +\
        __all_model_loops__ + __all_remove_atoms__ + __all_potential_energy__ +\
        __all_solvate_box__ + __all_protonation__ + __all_mutations__ + __all_topology__ +\
        __all_topology__ + __all_chem_and_phys_properties__ + __all_pbc__

