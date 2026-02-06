from molsysmt.exceptions import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest

@arg_digest(form='molsysmt.Structures', to_form='molsysmt.Structures')
def append_structures(to_item, item=None, id=None, time=None, coordinates=None, velocities=None,
        box=None, temperature=None, potential_energy=None, kinetic_energy=None, skip_digestion=False):

    item.append(id=id, time=time, coordinates=coordinates,
            velocities=velocities, box=box, temperature=temperature,
            potential_energy=potential_energy, kinetic_energy=kinetic_energy,
            skip_digestion=True)

    pass

