from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.Structures', to_form='molsysmt.Structures')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):

    to_item.append(id = item.id,
                   time = item.time,
                   coordinates = item.coordinates,
                   velocities = item.velocities,
                   box = item.box,
                   temperature = item.temperature,
                   potential_energy = item.potential_energy,
                   kinetic_energy = item.kinetic_energy,
                   skip_digestion=True)

    pass

