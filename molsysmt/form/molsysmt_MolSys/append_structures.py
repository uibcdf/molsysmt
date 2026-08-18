from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.argdigest import arg_digest
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
    """
    Appending coordinate structures to an item of form molsysmt.MolSys.

    Parameters
    ----------
    to_item : molsysmt.MolSys
        Target item to modify or add elements to.
    item : molsysmt.MolSys
        Source item in molsysmt.MolSys form.
    structure_id : object
        Structure identifiers.
    time : numpy.ndarray or quantity
        Simulation time coordinates in picoseconds.
    coordinates : numpy.ndarray or quantity
        Cartesian coordinate array in nanometers.
    velocities : object
        Argument velocities.
    box : numpy.ndarray or quantity
        Simulation box vectors in nanometers.
    temperature : object
        Argument temperature.
    potential_energy : object
        Argument potential_energy.
    kinetic_energy : object
        Argument kinetic_energy.
    structure_chemical_state_index : object
        Argument structure_chemical_state_index.
    b_factor : object
        Argument b_factor.
    alternate_location : object
        Argument alternate_location.
    occupancy : object
        Argument occupancy.
    atom_indices : str, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : str, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include.
    attribute_policy : object
        Argument attribute_policy.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    molsysmt.MolSys
        Resulting object in molsysmt.MolSys form.

    .. versionadded:: 1.0.0
    """

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
