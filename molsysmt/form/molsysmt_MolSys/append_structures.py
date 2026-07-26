from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import pandas as pd
import numpy as np


@arg_digest(form='molsysmt.MolSys', to_form='molsysmt.MolSys')
def append_structures(to_item, item=None, structure_id=None, time=None, coordinates=None, velocities=None,
                      box=None, temperature=None, potential_energy=None, kinetic_energy=None,
                      structure_chemical_state_index=None,
                      b_factor=None, alternate_location=None, occupancy=None,
                      atom_indices='all', structure_indices='all',
                      attribute_policy='intersection', skip_digestion=False):

    if item is not None:
        to_item.append_structures(
            item,
            atom_indices=atom_indices,
            structure_indices=structure_indices,
            attribute_policy=attribute_policy,
            skip_digestion=True,
        )
    else:
        old_n_structures = to_item.structures.n_structures
        old_state_indices = to_item._get_structure_chemical_state_indices(
            resolved=True
        )
        to_item.structures.append(structure_id=structure_id, time=time, coordinates=coordinates,
                                  velocities=velocities, box=box, temperature=temperature,
                                  potential_energy=potential_energy, kinetic_energy=kinetic_energy,
                                  b_factor=b_factor, alternate_location=alternate_location,
                                  occupancy=occupancy,
                                  atom_indices=atom_indices, structure_indices=structure_indices,
                                  attribute_policy=attribute_policy,
                                  skip_digestion=True)
        n_new_structures = to_item.structures.n_structures - old_n_structures
        if n_new_structures and (
            len(to_item.topology._chemical_states) > 1
            or to_item._structure_chemical_state_indices is not None
            or structure_chemical_state_index is not None
        ):
            if structure_chemical_state_index is None:
                if len(to_item.topology._chemical_states) == 1:
                    incoming = [0] * n_new_structures
                else:
                    incoming = [pd.NA] * n_new_structures
            elif structure_chemical_state_index is pd.NA or np.isscalar(
                structure_chemical_state_index
            ):
                incoming = [structure_chemical_state_index] * n_new_structures
            else:
                incoming = list(structure_chemical_state_index)
            combined = pd.array(
                list(old_state_indices) + incoming, dtype='Int64'
            )
            to_item._structure_chemical_state_indices = None
            to_item._set_structure_chemical_state_indices(combined)

    pass
