from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all


@digest(form='molsysmt.MolSys', to_form='molsysmt.MolSys')
def append_structures(to_item, item=None, structure_id=None, time=None, coordinates=None, velocities=None,
                      box=None, temperature=None, potential_energy=None, kinetic_energy=None,
                      atom_indices='all', structure_indices='all', skip_digestion=False):

    if item is not None:
        to_item.structures.append_structures(item, atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)
    else:
        to_item.structures.append(structure_id=structure_id, time=time, coordinates=coordinates,
                                  velocities=velocities, box=box, temperature=temperature,
                                  potential_energy=potential_energy, kinetic_energy=kinetic_energy,
                                  atom_indices=atom_indices, structure_indices=structure_indices,
                                  skip_digestion=True)

    pass

