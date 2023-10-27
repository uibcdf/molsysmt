def is_form(item):

    from openmm.app.simulation import Simulation

    return isinstance(item, Simulation)

