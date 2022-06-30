# Configuration file for MolSysMT

# Configure pyunitwizard
import pyunitwizard as puw

puw.configure.load_library(['pint', 'openmm.unit'])
puw.configure.set_default_form('pint')
puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'amu', 'e',
                                 'kJ/mol', 'kJ/(mol*nm**2)', 'N', 'degrees'])


# Set this variable false to disable argument checking
argument_checking = True
