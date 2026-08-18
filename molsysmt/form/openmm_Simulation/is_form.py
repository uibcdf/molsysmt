def is_form(item):
    """
    Checking whether an item is an instance of form openmm.Simulation.

    Parameters
    ----------
    item : object
        Item to check.

    Returns
    -------
    bool
        True if item conforms to form openmm.Simulation, False otherwise.
    """

    from openmm.app.simulation import Simulation

    return isinstance(item, Simulation)

