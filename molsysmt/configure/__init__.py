# Configuration file for MolSysMT

from .logging_setup import setup_logging

# Set this variable true while testing
_testing = False

# Set this variable true while debugging
_debugging = False

# Default attribute values

default_attribute = {

        'box':None,
        'structure_id':None,
        'box':None,
        'coordinates':None,
        'time':None,

        'forcefield':'AMBER14',
        'implicit_solvent':None,
        'water_model':'TIP3P',
        'non_bonded_method':'no cutoff',
        'constraints':'hbonds',
        'dispersion_correction':False,
        'switch_distance':None,
        'ewald_error_tolerance':0.0005,
        'integrator':'Langevin',
        'temperature':'0.0 kelvin',
        'friction':'1.0/picoseconds',
        'time_step':'2.0 femtoseconds',
        'platform':'CUDA',
        }

# Selection sortcuts
selection_shortcuts={
        'MolSysMT': {
            'backbone':'(molecule_type==["protein", "peptide"] and atom_name==["CA", "N", "C", "O"])',
            'heavy atoms not solvent':'(atom_name!=["H"]) and (molecule_type!=["water", "ion"])',
            'heavy atoms':'(atom_name!=["H"])',
            'not solvent':'(molecule_type==["water", "ion"])',
            'solvent':'(molecule_type==["water", "ion"])',
            'hydrogens':'(atom_type=="H")',
            'hydrogen':'(atom_type=="H")',
            }
        }

# Units

def set_default_quantities_form(form='pint'):

    from molsysmt import pyunitwizard as puw
    puw.configure.set_default_form(form)

def set_default_quantities_parser(form='pint'):

    from molsysmt import pyunitwizard as puw
    puw.configure.set_default_parser(form)

def set_default_standard_units(standards=['nm', 'ps', 'K', 'mole', 'amu', 'e',
    'kJ/mol', 'kJ/(mol*nm**2)', 'N', 'degrees']):

    from molsysmt import pyunitwizard as puw
    puw.configure.set_standard_units(standards)

# Sphinx

# Is sphinx working?
#from os import environ
#_sphinx_is_working = ('SPHINXWORKING' in environ)
#del(environ)
#
## NGLview
#_view_from_htmlfiles=False
#if _sphinx_is_working:
#    _view_from_htmlfiles=True

# Optimization
large_list_length = 10000

# Visibility
show_all_capabilities = True

# Heavy trajectory processing
import os as _os
max_ram_usage = int(0.5 * _os.sysconf('SC_PAGE_SIZE') * _os.sysconf('SC_PHYS_PAGES'))  # 50% of total RAM in bytes
heavy_mode = 'auto'         # 'auto' | 'force' | 'off'
chunk_size = 100            # default number of frames per chunk
emit_heavy_telemetry = True
memory_pressure_threshold = 0.80  # warn when RSS exceeds this fraction of max_ram_usage
del _os

# Topology
min_length_protein = 50

# GPU acceleration
use_gpu = False          # True | False | 'auto'
gpu_threshold = 3_000_000  # payload (n_structures * n_atoms * 3) above which 'auto' uses GPU


