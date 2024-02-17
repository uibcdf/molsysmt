from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures')
def append_structures(item, id=None, time=None, coordinates=None, velocities=None,
        box=None, temperature=None, potential_energy=None, kinetic_energy=None, skip_digestion=False):

    item.append(id=id, time=time, coordinates=coordinates,
            velocities=velocities, box=box, temperature=temperature,
            potential_energy=potential_energy, kinetic_energy=kinetic_energy,
            skip_digestion=True)

    pass

