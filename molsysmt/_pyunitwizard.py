# Configure PyUnitWizard
#
# The MolSysSuite libraries share one PyUnitWizard kernel inside a process, so
# whichever of them configured it last used to win -- and with lazy imports
# "last" can be a notebook cell run much later, silently undoing what the user
# chose. They therefore all declare the *same* policy, and each one applies it
# only when no policy is active yet.
#
# The shared policy is MolSysMT's. Changing it is a suite-wide decision, not a
# per-library one: see `pyunitwizard/devguide/pending_proposals/
# molsyssuite_unit_configuration_authority.md`.

import pyunitwizard as puw

STANDARD_UNITS = [
    'nm',              # length: nanometer
    'ps',              # time: picosecond
    'K',               # temperature: kelvin
    'mole',            # amount of substance
    'dalton',          # mass
    'e',               # charge: elementary charge
    'kJ/mol',          # energy
    'kJ/(mol*nm)',     # force
    'kJ/(mol*nm**2)',  # force constant
    'radians',         # angle
]

# Only when nobody has decided yet. An active policy belongs to whoever set it:
# another suite library, or the user.
if not puw.configure.has_active_policy():
    puw.configure.set_default_form('pint')
    puw.configure.set_default_parser('pint')
    puw.configure.set_standard_units(STANDARD_UNITS, provenance='molsysmt')

# Fast tracks are named converters, not policy: `to_nanometers` means
# nanometers whatever the active standard units are. Registering them is
# idempotent across the suite, so it is unconditional.
puw.register_fast_track('nanometers', puw.unit('nm'))
puw.register_fast_track('picoseconds', puw.unit('ps'))
puw.register_fast_track('kelvin', puw.unit('K'))
