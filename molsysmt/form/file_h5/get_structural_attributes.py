from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
from molsysmt import pyunitwizard as puw
from depdigest import dep_digest
import types

form = 'file:h5'


@dep_digest('mdtraj')
def _read_frames(item):
    """Reading all frame fields from an MDTraj HDF5 file."""

    import mdtraj as md

    with md.open(item) as tmp_item:
        return tmp_item.read()


def _slice_structures(value, structure_indices):
    """Selecting structures from an optional frame field."""

    if value is None:
        return None
    if is_all(structure_indices):
        return value
    return value[structure_indices]


@arg_digest(form=form)
def get_coordinates_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    frames = _read_frames(item)
    output = _slice_structures(frames.coordinates, structure_indices)
    if not is_all(indices):
        output = output[:, indices, :]
    return output * puw.unit('nanometer')


@arg_digest(form=form)
def get_velocities_from_atom(item, indices='all', structure_indices='all', skip_digestion=False):
    frames = _read_frames(item)
    output = _slice_structures(frames.velocities, structure_indices)
    if output is not None and not is_all(indices):
        output = output[:, indices, :]
    if output is None:
        return None
    return output * puw.unit('nanometer/picosecond')


@arg_digest(form=form)
def get_box_from_system(item, structure_indices='all', skip_digestion=False):
    frames = _read_frames(item)
    lengths = _slice_structures(frames.cell_lengths, structure_indices)
    angles = _slice_structures(frames.cell_angles, structure_indices)
    if lengths is None or angles is None:
        return None

    from molsysmt.pbc import get_box_from_lengths_and_angles

    return get_box_from_lengths_and_angles(
        lengths * puw.unit('nanometer'),
        angles * puw.unit('degree'),
        skip_digestion=True,
    )


@arg_digest(form=form)
def get_time_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_frames(item).time, structure_indices)
    if output is None:
        return None
    return output * puw.unit('picosecond')


@arg_digest(form=form)
def get_temperature_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_frames(item).temperature, structure_indices)
    if output is None:
        return None
    return output * puw.unit('kelvin')


@arg_digest(form=form)
def get_potential_energy_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_frames(item).potentialEnergy, structure_indices)
    if output is None:
        return None
    return output * puw.unit('kilojoule/mole')


@arg_digest(form=form)
def get_kinetic_energy_from_system(item, structure_indices='all', skip_digestion=False):
    output = _slice_structures(_read_frames(item).kineticEnergy, structure_indices)
    if output is None:
        return None
    return output * puw.unit('kilojoule/mole')


@arg_digest(form=form)
def get_total_energy_from_system(item, structure_indices='all', skip_digestion=False):
    potential = get_potential_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    kinetic = get_kinetic_energy_from_system(
        item,
        structure_indices=structure_indices,
        skip_digestion=True,
    )
    if potential is None or kinetic is None:
        return None
    return potential + kinetic


@arg_digest(form=form)
def get_structure_id_from_system(item, structure_indices='all', skip_digestion=False):
    return None

@arg_digest(form=form)
@dep_digest('mdtraj')
def get_n_structures_from_system(item, structure_indices='all', skip_digestion=False):
    import mdtraj as md
    with md.open(item) as tmp_item:
        # mdtraj HDF5TrajectoryFile uses __len__ for n_frames
        try:
            output = len(tmp_item)
        except Exception:
            coords = tmp_item.read(n_frames=1).coordinates
            output = coords.shape[1]
    if not is_all(structure_indices):
        output = len(structure_indices)
    return output

# List of functions to be imported
__all__ = [name for name, obj in globals().items() if isinstance(obj, types.FunctionType) and name.startswith('get_')]
