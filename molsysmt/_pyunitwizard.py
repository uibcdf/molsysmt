# Configure PyUnitWizard

import pyunitwizard as puw

puw.configure.set_default_form('pint')
puw.configure.set_default_parser('pint')
puw.configure.set_standard_units(['nm', 'ps', 'K', 'mole', 'amu', 'e',
                                 'kJ/mol', 'kJ/(mol*nm)', 'kJ/(mol*nm**2)', 'radians'])
# puw.configure.add_constant(name, value, unit)

# Registering MolSysMT canonical fast-tracks
puw.register_fast_track("nanometers", puw.unit("nm"))
puw.register_fast_track("picoseconds", puw.unit("ps"))
puw.register_fast_track("kelvin", puw.unit("K"))
