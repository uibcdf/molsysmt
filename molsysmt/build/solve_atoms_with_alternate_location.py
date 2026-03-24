from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.smonitor import ArgumentError, InternalAlgorithmError, ArgumentChoiceError
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
import numpy as np

@arg_digest()
def solve_atoms_with_alternate_location(molecular_system, selection='all',
        structure_indices='all', location_id='occupancy', syntax='MolSysMT'):
    """
    Resolve atoms with alternate location records by selecting one conformer per atom.

    Crystallographic structures often contain atoms with multiple alternate location
    records (e.g. 'A' and 'B'), each associated with a different set of coordinates,
    B-factors, occupancies, and atom IDs. This function selects a single conformer
    for each such atom and updates the molecular system in-place with the chosen
    coordinates, B-factors, and atom IDs.

    Parameters
    ----------
    molecular_system : molecular system
        Molecular system in any of :ref:`the supported forms <Introduction_Forms>`.
        Must carry alternate-location metadata accessible via
        ``get(molecular_system, alternate_location=True)``.

    selection : str, list, tuple, or numpy.ndarray, default 'all'
        Atom selection restricting which atoms are considered for alternate-location
        resolution.

    structure_indices : int, list of int, or 'all', default 'all'
        Structure frame index or indices over which to apply the resolution. If
        ``'all'``, all frames are processed.

    location_id : str, list of str, or numpy.ndarray, default 'occupancy'
        Strategy or explicit location identifiers used to choose among alternate
        conformers:

        - ``'occupancy'``: Select the conformer with the highest occupancy for each
          atom. When two conformers share an occupancy of exactly 0.5 the location
          'A' is chosen.
        - A single-character string (e.g. ``'A'``): Apply the same location ID to
          all atoms in the selection.
        - A list or array of single-character strings: Provide one location ID per
          atom in the selection.

    syntax : str, default 'MolSysMT'
        Syntax used to interpret the ``selection`` string.

    Returns
    -------
    None
        The molecular system is modified in-place; no value is returned.

    Raises
    ------
    InternalAlgorithmError
        Raised if the number of resolved location IDs does not match the number of
        selected atoms.

    Notes
    -----
    If the molecular system has B-factor data, the B-factors of the chosen conformer
    are written back alongside the coordinates and atom IDs.

    When all structure frames share the same set of atoms with alternate locations,
    a single vectorised ``set`` call is used; otherwise the update is applied
    frame-by-frame.

    .. versionadded:: 1.0.0
    """

    from molsysmt import get, set, select

    alt_loc_dict = get(molecular_system, alternate_location=True)

    system_with_b_factors = (get(molecular_system, b_factors=True) is not None)

    if is_all(structure_indices):

        n_structures = get(molecular_system, n_structures=True)
        structure_indices = np.arange(n_structures)

    atom_indices = select(molecular_system, selection=selection, syntax=syntax)
    n_atoms = len(atom_indices)

    if isinstance(location_id, str):

        if location_id=='occupancy':

            new_location_id=[]
            new_atom_indices=[]

            for structure_index in structure_indices:
                for tmp_atom_index, tmp_alt_loc_value in alt_loc_dict[structure_index].items():
                    arg = np.argmax(tmp_alt_loc_value['occupancy'])

                for tmp_atom_index, tmp_alt_loc_value in alt_loc_dict[structure_index].items():
                    key_int = int(tmp_atom_index)
                    if key_int in atom_indices:
                        new_atom_indices.append(key_int)
                        arg = np.argmax(tmp_alt_loc_value['occupancy'])
                        if np.isclose(tmp_alt_loc_value['occupancy'][arg],0.5):
                            new_location_id.append('A')
                        else:
                            new_location_id.append(tmp_alt_loc_value['location_id'][arg])

            location_id = new_location_id
            atom_indices = new_atom_indices

        elif len(location_id)==1:
            location_id = [location_id for ii in range(n_atoms)]

    if isinstance(location_id,(list, tuple, np.ndarray)):
        if len(location_id)!=n_atoms:
            raise InternalAlgorithmError("Unexpected empty state", caller="molsysmt.build.solve_atoms_with_alternate_location.py")

        aux_atom_indices=[]
        aux_b_factor=[]
        aux_atom_id=[]
        aux_coordinates=[]
        for structure_index in structure_indices:
            aux2_atom_indices=[]
            aux2_b_factor=[]
            aux2_atom_id=[]
            aux2_coordinates=[]
            for tmp_atom_index, tmp_alt_loc_value in alt_loc_dict[structure_index].items():
                key_int = int(tmp_atom_index)
                if key_int in atom_indices:
                    aux_arg = np.argwhere(np.array(atom_indices)==key_int)[0][0]
                    arg = np.where(tmp_alt_loc_value['location_id']==location_id[aux_arg])[0][0]
                    aux2_atom_indices.append(key_int)
                    aux2_b_factor.append(tmp_alt_loc_value['b_factor'][arg])
                    aux2_atom_id.append(tmp_alt_loc_value['atom_id'][arg])
                    aux2_coordinates.append(tmp_alt_loc_value['coordinates'][arg])
            aux_atom_indices.append(aux2_atom_indices)
            aux_b_factor.append(puw.utils.sequences.concatenate(aux2_b_factor))
            aux_atom_id.append(aux2_atom_id)
            aux_coordinates.append(puw.utils.sequences.concatenate(aux2_coordinates))

        aux_coordinates = puw.utils.sequences.concatenate(aux_coordinates)
        aux_b_factor = puw.utils.sequences.concatenate(aux_b_factor)

        equal_atom_indices_all_structures=False

        for tmp_atom_indices in aux_atom_indices:
            equal_atom_indices_all_structures = np.all(tmp_atom_indices==aux_atom_indices[0])
            if not equal_atom_indices_all_structures:
                break

        if equal_atom_indices_all_structures:
            mask=aux_atom_indices[0]
            atts_to_set = {
                'atom_id':aux_atom_id[0],
                'coordinates':aux_coordinates}
            if system_with_b_factors:
                atts_to_set['b_factor']=aux_b_factor
            set(molecular_system, selection=mask, structure_indices=structure_indices,
                **atts_to_set)
        else:
            for ii, structure_index in enumerate(structure_indices):
                mask=aux_atom_indices[ii]
                atts_to_set = {
                    'atom_id':aux_atom_id[ii],
                    'coordinates':aux_coordinates[ii]}
                if system_with_b_factors:
                    atts_to_set['b_factor']=aux_b_factor[ii]
                set(molecular_system, selection=mask, structure_indices=structure_index,
                    **atts_to_set)

    pass
