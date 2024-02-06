from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest

@digest(form='molsysmt.StructuresOld', to_form='molsysmt.StructuresOld')
def add(to_item, item, atom_indices='all', structure_indices='all', skip_digestion=False):

    to_item.append_structures(structure_id = item.structure_id,
                              time = item.time,
                              coordinates = item.coordinates,
                              velocities = item.velocities,
                              box = box,
                              temperature = temperature,
                              potential_energy = potential_energy,
                              kinetic_energy = kinetic_energy,
                              skip_digestion=True)

    pass

