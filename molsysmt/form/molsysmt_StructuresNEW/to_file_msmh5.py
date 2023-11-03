from molsysmt._private.digestion import digest
from molsysmt import pyunitwizard as puw
import numpy as np

@digest(form='molsysmt.StructuresNEW')
def to_file_msmh5(item, atom_indices='all', structure_indices='all', output_filename=None,
        compression='gzip', compression_opts=4, int_precision='single', float_precision='single'):

    from molsysmt.native import MSMH5FileHandler

    handler = MSMH5FileHandler(output_filename, io_mode='w', compression=compression,
            compression_opts=compression_opts, int_precision=int_precision,
            float_precision=float_precision, closed=False)

    _add_structures_to_msmh5(item, handler, atom_indices=atom_indices,
            structure_indices=structure_indices)

    handler.close()

    return output_filename

def _add_structures_to_msmh5(item, file, atom_indices='all', structure_indices='all'):

    from h5py._hl.files import File as h5py_File
    from molsysmt.native import MSMH5FileHandler

    file_is_msmh5 = False
    needs_to_be_closed = False

    if isinstance(file, h5py_File):

        if 'type' in file.attrs:
            file_is_msmh5 = (file.attrs['type']=='msmh5')

    elif isinstance(file, MSMH5FileHandler):

            file = file.file
            file_is_msmh5 = True

    else:

        from molsysmt.form.file_msmh5.is_form import is_form as is_file_msmh5_form

        file_is_msmh5 = is_file_msmh5_form(file)

        if file_is_msmh5:
            file = h5py.File(file, "w")
            needs_to_be_closed = True

    if not file_is_msmh5:
        raise ValueError

    int_precision = file.attrs['int_precision']
    float_precision = file.attrs['float_precision']

    if int_precision=='single':
        int_type=np.int32
    elif int_precision=='double':
        int_type=np.int64

    if float_precision=='single':
        float_type=np.float32
    elif float_precision=='double':
        float_type=np.float64

    structures_ds = file['structures']

    n_atoms = item.n_atoms
    n_structures = item.n_structures

    structures_ds.attrs['n_atoms'] = item.n_atoms
    structures_ds.attrs['n_structures'] = item.n_structures

    length_unit = puw.get_standard_units(dimensionality={'[L]':1})
    time_unit = puw.get_standard_units(dimensionality={'[T]':1})
    energy_unit = puw.get_standard_units(dimensionality={'[L]':2, '[M]':1, '[T]':-2,
        '[mol]': -1})
    temperature_unit = puw.get_standard_units(dimensionality={'[K]':1})

    structures_ds.attrs['length_unit']=str(length_unit)
    structures_ds.attrs['time_unit']=str(time_unit)
    structures_ds.attrs['energy_unit']=str(energy_unit)

    if item.coordinates is not None:
        structures_ds['coordinates'].resize((n_structures,n_atoms,3))
        if puw.check(item.coordinates, unit=length_unit):
            aux = puw.get_value(item.coordinates).astype(float_precision)
        else:
            aux = puw.get_value(item.coordinates, to_unit=length_unit).astype(float_precision)
        structures_ds['coordinates'][:,:,:] = aux

    if item.velocities is not None:
        structures_ds['velocities'].resize((n_structures,n_atoms,3))
        if puw.check(item.velocities, unit=length_unit/length_time):
            aux = puw.get_value(item.velocities).astype(float_precision)
        else:
            aux = puw.get_value(item.velocities, to_unit=length_unit/length_time).astype(float_precision)
        structures_ds['velocities'][:,:,:] = aux

    if item.box is not None:
        structures_ds['box'].resize((n_structures,3,3))
        if puw.check(item.box, unit=length_unit):
            aux = puw.get_value(item.box).astype(float_precision)
        else:
            aux = puw.get_value(item.box, to_unit=length_unit).astype(float_precision)
        structures_ds['box'][:,:,:] = aux

    if item.kinetic_energy is not None:
        structures_ds['kinetic_energy'].resize((n_structures))
        if puw.check(item.kinetic_energy, unit=energy_unit):
            aux = puw.get_value(item.kinetic_energy).astype(float_precision)
        else:
            aux = puw.get_value(item.kinetic_energy, to_unit=length_unit).astype(float_precision)
        structures_ds['kinetic_energy'][:] = aux

    if item.potential_energy is not None:
        structures_ds['potential_energy'].resize((n_structures))
        if puw.check(item.potential_energy, unit=energy_unit):
            aux = puw.get_value(item.potential_energy).astype(float_precision)
        else:
            aux = puw.get_value(item.potential_energy, to_unit=length_unit).astype(float_precision)
        structures_ds['potential_energy'][:] = aux

    if item.temperature is not None:
        structures_ds['temperature'].resize((n_structures))
        if puw.check(item.temperature, unit=temperature_unit):
            aux = puw.get_value(item.temperature).astype(float_precision)
        else:
            aux = puw.get_value(item.temperature, to_unit=length_unit).astype(float_precision)
        structures_ds['temperature'][:] = aux

    if needs_to_be_closed:
        file.close()

    pass

