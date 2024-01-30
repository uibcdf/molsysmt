from molsysmt._private.exceptions import NotImplementedMethodError
from molsysmt._private.digestion import digest
from molsysmt._private.variables import is_all
import numpy as np

@digest(form='file:h5msm')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
            skip_digestion=False):

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename!=item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)
            tmp_item = output_filename

        else:

            tmp_item = item
    else:

        from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
        from molsysmt.native import H5MSMFileHandler

        input_file_handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
        input_file = input_file_handler.file

        int_precision = input_file_handler.file.attrs['int_precision']
        float_precision = input_file_handler.file.attrs['float_precision']
        length_unit = input_file_handler.file.attrs['length_unit']
        time_unit = input_file_handler.file.attrs['time_unit']
        energy_unit = input_file_handler.file.attrs['energy_unit']
        temperature_unit = input_file_handler.file.attrs['temperature_unit']
        charge_unit = input_file_handler.file.attrs['charge_unit']
        mass_unit = input_file_handler.file.attrs['mass_unit']

        output_file_handler = H5MSMFileHandler(output_filename, io_mode='w',
                int_precision=int_precision, float_precision=float_precision,
                length_unit=length_unit, time_unit=time_unit, energy_unit=energy_unit,
                temperature_unit=temperature_unit, charge_unit=charge_unit,
                mass_unit=mass_unit)
        output_file = output_file_handler.file

        # Topology

        if is_all(atom_indices):

            n_atoms = input_file['atoms'].shape[0]
            output_file['topology'].attrs['n_atoms'] = n_atoms

            output_file['topology']['atoms']['id'].resize((n_atoms,))
            output_file['topology']['atoms']['name'].resize((n_atoms,))
            output_file['topology']['atoms']['type'].resize((n_atoms,))
            output_file['topology']['atoms']['group_index'].resize((n_atoms,))
            output_file['topology']['atoms']['chain_index'].resize((n_atoms,))

            output_file['topology']['atoms']['id'][:] = input_file['topology']['atoms']['id'][:]
            output_file['topology']['atoms']['name'][:] = input_file['topology']['atoms']['name'][:]
            output_file['topology']['atoms']['type'][:] = input_file['topology']['atoms']['type'][:]
            output_file['topology']['atoms']['group_index'][:] = input_file['topology']['atoms']['group_index'][:]
            output_file['topology']['atoms']['chain_index'][:] = input_file['topology']['atoms']['chain_index'][:]

            n_groups = input_file['groups'].shape[0]
            output_file['topology'].attrs['n_groups'] = n_groups

            output_file['topology']['groups']['id'].resize((n_groups,))
            output_file['topology']['groups']['name'].resize((n_groups,))
            output_file['topology']['groups']['type'].resize((n_groups,))
            output_file['topology']['groups']['component_index'].resize((n_groups,))

            output_file['topology']['groups']['id'][:] = input_file['topology']['groups']['id'][:]
            output_file['topology']['groups']['name'][:] = input_file['topology']['groups']['name'][:]
            output_file['topology']['groups']['type'][:] = input_file['topology']['groups']['type'][:]
            output_file['topology']['groups']['component_index'][:] = input_file['topology']['groups']['component_index'][:]

            n_components = input_file['components'].shape[0]
            output_file['topology'].attrs['n_components'] = n_components

            output_file['topology']['components']['id'].resize((n_components,))
            output_file['topology']['components']['name'].resize((n_components,))
            output_file['topology']['components']['type'].resize((n_components,))
            output_file['topology']['components']['molecule_index'].resize((n_components,))

            output_file['topology']['components']['id'][:] = input_file['topology']['components']['id'][:]
            output_file['topology']['components']['name'][:] = input_file['topology']['components']['name'][:]
            output_file['topology']['components']['type'][:] = input_file['topology']['components']['type'][:]
            output_file['topology']['components']['molecule_index'][:] = input_file['topology']['components']['molecule_index'][:]

            n_molecules = input_file['molecules'].shape[0]
            output_file['topology'].attrs['n_molecules'] = n_molecules

            output_file['topology']['molecules']['id'].resize((n_molecules,))
            output_file['topology']['molecules']['name'].resize((n_molecules,))
            output_file['topology']['molecules']['type'].resize((n_molecules,))
            output_file['topology']['molecules']['entity_index'].resize((n_molecules,))

            output_file['topology']['molecules']['id'][:] = input_file['topology']['molecules']['id'][:]
            output_file['topology']['molecules']['name'][:] = input_file['topology']['molecules']['name'][:]
            output_file['topology']['molecules']['type'][:] = input_file['topology']['molecules']['type'][:]
            output_file['topology']['molecules']['entity_index'][:] = input_file['topology']['molecules']['entity_index'][:]

            n_entities = input_file['entities'].shape[0]
            output_file['topology'].attrs['n_entities'] = n_entities

            output_file['topology']['entities']['id'].resize((n_entities,))
            output_file['topology']['entities']['name'].resize((n_entities,))
            output_file['topology']['entities']['type'].resize((n_entities,))

            output_file['topology']['entities']['id'][:] = input_file['topology']['entities']['id'][:]
            output_file['topology']['entities']['name'][:] = input_file['topology']['entities']['name'][:]
            output_file['topology']['entities']['type'][:] = input_file['topology']['entities']['type'][:]

            n_chains = input_file['chains'].shape[0]
            output_file['topology'].attrs['n_chains'] = n_chains

            output_file['topology']['chains']['id'].resize((n_chains,))
            output_file['topology']['chains']['name'].resize((n_chains,))
            output_file['topology']['chains']['type'].resize((n_chains,))

            output_file['topology']['chains']['id'][:] = input_file['topology']['chains']['id'][:]
            output_file['topology']['chains']['name'][:] = input_file['topology']['chains']['name'][:]
            output_file['topology']['chains']['type'][:] = input_file['topology']['chains']['type'][:]

            n_bonds = input_file['bonds'].shape[0]
            output_file['topology'].attrs['n_bonds'] = n_bonds

            output_file['topology']['bonds']['atom1_index'].resize((n_bonds,))
            output_file['topology']['bonds']['atom2_index'].resize((n_bonds,))
            output_file['topology']['bonds']['order'].resize((n_bonds,))
            output_file['topology']['bonds']['type'].resize((n_bonds,))

            output_file['topology']['bonds']['atom1_index'][:] = input_file['topology']['bonds']['atom1_index'][:]
            output_file['topology']['bonds']['atom2_index'][:] = input_file['topology']['bonds']['atom2_index'][:]
            output_file['topology']['bonds']['order'][:] = input_file['topology']['bonds']['order'][:]
            output_file['topology']['bonds']['type'][:] = input_file['topology']['bonds']['type'][:]

        else:

            n_atoms = len(atom_indices)
            output_file['topology'].attrs['n_atoms'] = n_atoms

            output_file['topology']['atoms']['id'].resize((n_atoms,))
            output_file['topology']['atoms']['name'].resize((n_atoms,))
            output_file['topology']['atoms']['type'].resize((n_atoms,))
            output_file['topology']['atoms']['group_index'].resize((n_atoms,))
            output_file['topology']['atoms']['chain_index'].resize((n_atoms,))

            output_file['topology']['atoms']['id'][:] = input_file['topology']['atoms']['id'][atom_indices]
            output_file['topology']['atoms']['name'][:] = input_file['topology']['atoms']['name'][atom_indices]
            output_file['topology']['atoms']['type'][:] = input_file['topology']['atoms']['type'][atom_indices]

            group_indices, aux = np.unique(input_file['topology']['atoms']['group_index'][atom_indices],
                    return_inverse=True)

            output_file['topology']['atoms']['group_index'][:] = aux

            chain_indices, aux = np.unique(input_file['topology']['atoms']['chain_index'][atom_indices],
                    return_inverse=True)

            output_file['topology']['atoms']['chain_index'][:] = aux

            n_groups = len(group_indices)
            output_file['topology'].attrs['n_groups'] = n_groups

            output_file['topology']['groups']['id'].resize((n_groups,))
            output_file['topology']['groups']['name'].resize((n_groups,))
            output_file['topology']['groups']['type'].resize((n_groups,))
            output_file['topology']['groups']['component_index'].resize((n_groups,))

            output_file['topology']['groups']['id'][:] = input_file['topology']['groups']['id'][group_indices]
            output_file['topology']['groups']['name'][:] = input_file['topology']['groups']['name'][group_indices]
            output_file['topology']['groups']['type'][:] = input_file['topology']['groups']['type'][group_indices]

            component_indices, aux = np.unique(input_file['topology']['groups']['component_index'][group_indices],
                    return_inverse=True)

            output_file['topology']['groups']['component_index'][:] = aux

            n_components = len(component_indices)
            output_file['topology'].attrs['n_components'] = n_components

            output_file['topology']['components']['id'].resize((n_components,))
            output_file['topology']['components']['name'].resize((n_components,))
            output_file['topology']['components']['type'].resize((n_components,))
            output_file['topology']['components']['molecule_index'].resize((n_components,))

            output_file['topology']['components']['id'][:] = input_file['topology']['components']['id'][component_indices]
            output_file['topology']['components']['name'][:] = input_file['topology']['components']['name'][component_indices]
            output_file['topology']['components']['type'][:] = input_file['topology']['components']['type'][component_indices]

            molecule_indices, aux = np.unique(input_file['topology']['components']['molecule_index'][component_indices],
                    return_inverse=True)

            output_file['topology']['components']['molecule_index'][:] = aux

            n_molecules = len(molecule_indices)
            output_file['topology'].attrs['n_molecules'] = n_molecules

            output_file['topology']['molecules']['id'].resize((n_molecules,))
            output_file['topology']['molecules']['name'].resize((n_molecules,))
            output_file['topology']['molecules']['type'].resize((n_molecules,))
            output_file['topology']['molecules']['entity_index'].resize((n_molecules,))

            output_file['topology']['molecules']['id'][:] = input_file['topology']['molecules']['id'][component_indices]
            output_file['topology']['molecules']['name'][:] = input_file['topology']['molecules']['name'][component_indices]
            output_file['topology']['molecules']['type'][:] = input_file['topology']['molecules']['type'][component_indices]

            entity_indices, aux = np.unique(input_file['topology']['molecules']['entity_index'][molecule_indices],
                    return_inverse=True)

            output_file['topology']['molecules']['entity_index'][:] = aux

            n_entities = len(entity_indices)
            output_file['topology'].attrs['n_entities'] = n_entities

            output_file['topology']['entities']['id'].resize((n_entities,))
            output_file['topology']['entities']['name'].resize((n_entities,))
            output_file['topology']['entities']['type'].resize((n_entities,))

            output_file['topology']['entities']['id'][:] = input_file['topology']['entities']['id'][entity_indices]
            output_file['topology']['entities']['name'][:] = input_file['topology']['entities']['name'][entity_indices]
            output_file['topology']['entities']['type'][:] = input_file['topology']['entities']['type'][entity_indices]

            n_chains = len(chain_indices)
            output_file['topology'].attrs['n_chains'] = n_chains

            output_file['topology']['chains']['id'].resize((n_chains,))
            output_file['topology']['chains']['name'].resize((n_chains,))
            output_file['topology']['chains']['type'].resize((n_chains,))

            output_file['topology']['chains']['id'][:] = input_file['topology']['chains']['id'][chain_indices]
            output_file['topology']['chains']['name'][:] = input_file['topology']['chains']['name'][chain_indices]
            output_file['topology']['chains']['type'][:] = input_file['topology']['chains']['type'][chain_indices]

            mask1 = np.in1d(input_file['topology']['bonds']['atom1_index'][:], atom_indices)
            mask2 = np.in1d(input_file['topology']['bonds']['atom2_index'][:], atom_indices)
            mask = mask1*mask2

            n_bonds = np.sum(mask)
            output_file['topology'].attrs['n_bonds'] = n_bonds

            output_file['topology']['bonds']['atom1_index'].resize((n_bonds,))
            output_file['topology']['bonds']['atom2_index'].resize((n_bonds,))
            output_file['topology']['bonds']['order'].resize((n_bonds,))
            output_file['topology']['bonds']['type'].resize((n_bonds,))

            output_file['topology']['bonds']['atom1_index'][:] = np.searchsorted(atom_indices,
                    input_file['topology']['bonds']['atom1_index'][mask].astype('int64'),
                    side='left')
            output_file['topology']['bonds']['atom2_index'][:] = np.searchsorted(atom_indices,
                    input_file['topology']['bonds']['atom2_index'][mask].astype('int64'),
                    side='left')
            output_file['topology']['bonds']['order'][:] = input_file['topology']['bonds']['order'][mask]
            output_file['topology']['bonds']['type'][:] = input_file['topology']['bonds']['type'][mask]

        # Structure

        if is_all(structure_indices):

            output_file['structures'].attrs['n_structures'] = input_file['structures'].attrs['n_structures']
            output_file['structures'].attrs['n_structures_written'] = input_file['structures'].attrs['n_structures_written']
            output_file['structures'].attrs['constant_time_step'] = input_file['structures'].attrs['constant_time_step']
            output_file['structures'].attrs['time_step'] = input_file['structures'].attrs['time_step']
            output_file['structures'].attrs['constant_id_step'] = input_file['structures'].attrs['constant_id_step']
            output_file['structures'].attrs['id_step'] = input_file['structures'].attrs['id_step']
            output_file['structures'].attrs['constant_box'] = input_file['structures'].attrs['constant_box']
            output_file['structures'].attrs['pbc'] = input_file['structures'].attrs['pbc']
            output_file['structures'].attrs['n_degrees_of_freedom'] = input_file['structures'].attrs['n_degrees_of_freedom']
            output_file['structures'].attrs['temperature_from_kinetic_energy'] = input_file['structures'].attrs['temperature_from_kinetic_energy']

            aux_n_structures = input_file['structures']['id'].shape[0]
            if aux_n_structures:
                output_file['structures']['id'].resize((aux_n_structures,))
                output_file['structures']['id'][:] = input_file['structures']['id'][:]

            aux_n_structures = input_file['structures']['time'].shape[0]
            if aux_n_structures:
                output_file['structures']['time'].resize((aux_n_structures,))
                output_file['structures']['time'][:] = input_file['structures']['time'][:]

            aux_n_structures = input_file['structures']['box'].shape[0]
            if aux_n_structures:
                output_file['structures']['box'].resize((aux_n_structures,3,3))
                output_file['structures']['box'][:,:,:] = input_file['structures']['box'][:,:,:]

            aux_n_structures = input_file['structures']['kinetic_energy'].shape[0]
            if aux_n_structures:
                output_file['structures']['kinetic_energy'].resize((aux_n_structures,))
                output_file['structures']['kinetic_energy'][:] = input_file['structures']['kinetic_energy'][:]

            aux_n_structures = input_file['structures']['potential_energy'].shape[0]
            if aux_n_structures:
                output_file['structures']['potential_energy'].resize((aux_n_structures,))
                output_file['structures']['potential_energy'][:] = input_file['structures']['potential_energy'][:]

            aux_n_structures = input_file['structures']['temperature'].shape[0]
            if aux_n_structures:
                output_file['structures']['temperature'].resize((aux_n_structures,))
                output_file['structures']['temperature'][:] = input_file['structures']['temperature'][:]

            if is_all(atom_indices):

                output_file['structures'].attrs['n_atoms'] = input_file['structures'].attrs['n_atoms']

                aux_n_structures, aux_n_atoms = input_file['structures']['coordinates'].shape[0:2]
                if aux_n_structures:
                    output_file['structures']['coordinates'].resize((aux_n_structures,aux_n_atoms,3))
                    output_file['structures']['coordinates'][:,:,:] = input_file['structures']['coordinates'][:,:,:]

                aux_n_structures, aux_n_atoms = input_file['structures']['velocities'].shape[0:2]
                if aux_n_structures:
                    output_file['structures']['velocities'].resize((aux_n_structures,aux_n_atoms,3))
                    output_file['structures']['velocities'][:,:,:] = input_file['structures']['velocities'][:,:,:]

            else:

                aux_n_atoms = len(atom_indices)
                output_file['structures'].attrs['n_atoms'] = aux_n_atoms

                aux_n_structures = input_file['structures']['coordinates'].shape[0]
                if aux_n_structures:
                    output_file['structures']['coordinates'].resize((aux_n_structures,aux_n_atoms,3))
                    output_file['structures']['coordinates'][:,:,:] = input_file['structures']['coordinates'][:,atom_indices,:]

                aux_n_structures = input_file['structures']['velocities'].shape[0]
                if aux_n_structures:
                    output_file['structures']['velocities'].resize((aux_n_structures,aux_n_atoms,3))
                    output_file['structures']['velocities'][:,:,:] = input_file['structures']['velocities'][:,atom_indices,:]

        else:

            n_structures = len(structure_indices)
            intervals = structure_indices[1:]-structure_indices[:-1]
            equispaced = np.all(intervals==intervals[0])
            interval = 0
            if equispaced:
                interval = intervals[0]
            del(intervals)

            output_file['structures'].attrs['n_structures'] = n_structures
            output_file['structures'].attrs['n_structures_written'] = n_structures
            if input_file['structures'].attrs['constant_time_step'] and equispaced:
                output_file['structures'].attrs['constant_time_step'] = True
                output_file['structures'].attrs['time_step'] = interval*input_file['structures'].attrs['time_step']
            else:
                output_file['structures'].attrs['constant_time_step'] = False
                output_file['structures'].attrs['time_step'] = 0.0
            if input_file['structures'].attrs['constant_id_step'] and equispaced:
                output_file['structures'].attrs['constant_id_step'] = True
                output_file['structures'].attrs['id_step'] = interval*input_file['structures'].attrs['id_step']
            else:
                output_file['structures'].attrs['constant_id_step'] = False
                output_file['structures'].attrs['id_step'] = 0
            output_file['structures'].attrs['constant_box'] = input_file['structures'].attrs['constant_box']
            output_file['structures'].attrs['pbc'] = input_file['structures'].attrs['pbc']
            output_file['structures'].attrs['n_degrees_of_freedom'] = input_file['structures'].attrs['n_degrees_of_freedom']
            output_file['structures'].attrs['temperature_from_kinetic_energy'] = input_file['structures'].attrs['temperature_from_kinetic_energy']

            aux_n_structures = input_file['structures']['id'].shape[0]
            if aux_n_structures:
                if input_file['structures'].attrs['constant_id_step']:
                    if equispaced:
                        output_file['structures']['id'].resize((1,))
                        output_file['structures']['id'][0] = input_file['structures']['id'][0]+structure_indices[0]*input_file['structures'].attrs['id_step']
                    else:
                        output_file['structures']['id'].resize((n_structures,))
                        output_file['structures']['id'][:] = input_file['structures']['id'][0]+structure_indices*input_file['structures'].attrs['id_step']
                else:
                    output_file['structures']['id'].resize((n_structures,))
                    output_file['structures']['id'][:] = input_file['structures']['id'][structure_indices]

            aux_n_structures = input_file['structures']['time'].shape[0]
            if aux_n_structures:
                if input_file['structures'].attrs['constant_time_step']:
                    if equispaced:
                        output_file['structures']['time'].resize((1,))
                        output_file['structures']['time'][0] = input_file['structures']['time'][0]+structure_indices[0]*input_file['structures'].attrs['time_step']
                    else:
                        output_file['structures']['time'].resize((n_structures,))
                        output_file['structures']['time'][:] = input_file['structures']['time'][0]+structure_indices*input_file['structures'].attrs['time_step']
                else:
                    output_file['structures']['time'].resize((n_structures,))
                    output_file['structures']['time'][:] = input_file['structures']['time'][structure_indices]

            aux_n_structures = input_file['structures']['box'].shape[0]
            if aux_n_structures:
                output_file['structures']['box'].resize((aux_n_structures,3,3))
                output_file['structures']['box'][:,:,:] = input_file['structures']['box'][structure_indices,:,:]

            aux_n_structures = input_file['structures']['kinetic_energy'].shape[0]
            if aux_n_structures:
                output_file['structures']['kinetic_energy'].resize((n_structures,))
                output_file['structures']['kinetic_energy'][:] = input_file['structures']['kinetic_energy'][structure_indices]

            aux_n_structures = input_file['structures']['potential_energy'].shape[0]
            if aux_n_structures:
                output_file['structures']['potential_energy'].resize((n_structures,))
                output_file['structures']['potential_energy'][:] = input_file['structures']['potential_energy'][structure_indices]

            aux_n_structures = input_file['structures']['temperature'].shape[0]
            if aux_n_structures:
                output_file['structures']['temperature'].resize((n_structures,))
                output_file['structures']['temperature'][:] = input_file['structures']['temperature'][structure_indices]

            if is_all(atom_indices):

                output_file['structures'].attrs['n_atoms'] = input_file['structures'].attrs['n_atoms']
                aux_n_structures, aux_n_atoms = input_file['structures']['coordinates'].shape[0:2]
                if aux_n_structures:
                    output_file['structures']['coordinates'].resize((n_structures,aux_n_atoms,3))
                    output_file['structures']['coordinates'][:,:,:] = input_file['structures']['coordinates'][structure_indices,:,:]

                aux_n_structures, aux_n_atoms = input_file['structures']['velocities'].shape[0:2]
                if aux_n_structures:
                    output_file['structures']['velocities'].resize((n_structures,aux_n_atoms,3))
                    output_file['structures']['velocities'][:,:,:] = input_file['structures']['velocities'][structure_indices,:,:]

            else:

                n_atoms = len(atom_indices)
                output_file['structures'].attrs['n_atoms'] = n_atoms

                aux_n_structures = input_file['structures']['coordinates'].shape[0]
                if aux_n_structures:
                    output_file['structures']['coordinates'].resize((n_structures,n_atoms,3))
                    for count, ii in enumerate(structure_indices):
                        output_file['structures']['coordinates'][count,:,:] = input_file['structures']['coordinates'][ii,atom_indices,:]

                aux_n_structures = input_file['structures']['velocities'].shape[0]
                if aux_n_structures:
                    output_file['structures']['velocities'].resize((n_structures,n_atoms,3))
                    for count, ii in enumerate(structure_indices):
                        output_file['structures']['velocities'][count,:,:] = input_file['structures']['velocities'][ii,atom_indices,:]

        input_file_handler.close()
        output_file_handler.close()

    return output_filename

