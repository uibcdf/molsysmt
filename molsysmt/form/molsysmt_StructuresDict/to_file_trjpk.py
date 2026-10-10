from molsysmt import pyunitwizard as puw
from molsysmt._private.argdigest import arg_digest
from molsysmt._private.variables import is_all


@arg_digest(form="molsysmt.StructuresDict")
def to_file_trjpk(
    item,
    atom_indices="all",
    structure_indices="all",
    output_filename=None,
    skip_digestion=False,
):
    """
    Converting from molsysmt.StructuresDict to file:trjpk.


    Parameters
    ----------
    item : molecular system
        Argument item.
    atom_indices : int, list, tuple, or numpy.ndarray, default='all'
        Atom indices (0-based) to include.
    structure_indices : int, list, tuple, or numpy.ndarray, default='all'
        Structure indices (0-based) to include or process.
    output_filename : str or pathlib.Path, default=None
        Output file path for serialization.
    skip_digestion : bool, default=False
        Whether to skip MolSysMT's internal argument digestion mechanism.

    Returns
    -------
    file:trjpk
        Resulting object in file:trjpk form.


    Notes
    -----
    Coordinates and box vectors are serialized in nm, time in ps. Both selected
    axes retain their order and repetitions, including empty axes. Missing
    optional fields are written as None. Arrays are converted one at a time.

    .. versionadded:: 1.0.0
    """

    import pickle

    from .get_structural_attributes import get_n_structures_from_system

    coordinates = item.get("coordinates")
    n_atoms = (
        (coordinates.shape[1] if coordinates is not None else 0)
        if is_all(atom_indices)
        else len(atom_indices)
    )
    n_structures = get_n_structures_from_system(
        item, structure_indices=structure_indices, skip_digestion=True
    )

    # Serialize one field at a time: avoid retaining converted copies of every array.
    with open(output_filename, "wb") as stream:
        pickle.dump(n_atoms, stream)
        pickle.dump(n_structures, stream)
        for name, unit in (
            ("coordinates", "nm"),
            ("box", "nm"),
            ("time", "ps"),
            ("structure_id", None),
        ):
            value = item.get(name)
            if value is not None:
                if not is_all(structure_indices):
                    value = value[structure_indices]
                if name == "coordinates" and not is_all(atom_indices):
                    value = value[:, atom_indices, :]
                if unit is not None:
                    value = puw.get_value(value, to_unit=unit)
            pickle.dump(value, stream)
            del value
    return output_filename
