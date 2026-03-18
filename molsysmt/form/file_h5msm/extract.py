from molsysmt._private.smonitor import NotImplementedMethodError
from molsysmt._private.arg_digestion import arg_digest
from molsysmt._private.variables import is_all
import numpy as np

@arg_digest(form='file:h5msm')
def extract(item, atom_indices='all', structure_indices='all', output_filename=None, copy_if_all=True,
            skip_digestion=False):

    if output_filename is None:
        output_filename = item

    if is_all(atom_indices) and is_all(structure_indices):

        if copy_if_all or (output_filename != item):

            from shutil import copy as copy_file
            copy_file(item, output_filename)

        return output_filename

    from .to_molsysmt_H5MSMFileHandler import to_molsysmt_H5MSMFileHandler
    from molsysmt.native import H5MSMFileHandler

    input_file_handler = to_molsysmt_H5MSMFileHandler(item, skip_digestion=True)
    input_file = input_file_handler.file

    int_precision = input_file.attrs['int_precision']
    float_precision = input_file.attrs['float_precision']
    length_unit = input_file.attrs['length_unit']
    time_unit = input_file.attrs['time_unit']
    energy_unit = input_file.attrs['energy_unit']
    temperature_unit = input_file.attrs['temperature_unit']
    charge_unit = input_file.attrs['charge_unit']
    mass_unit = input_file.attrs['mass_unit']

    if int_precision == 'single':
        int_type = np.int32
    else:
        int_type = np.int64

    output_file_handler = H5MSMFileHandler(output_filename, io_mode='w',
            int_precision=int_precision, float_precision=float_precision,
            length_unit=length_unit, time_unit=time_unit, energy_unit=energy_unit,
            temperature_unit=temperature_unit, charge_unit=charge_unit,
            mass_unit=mass_unit)
    output_file = output_file_handler.file

    topo_in = input_file['topology']
    topo_out = output_file['topology']

    # -----------------------------------------------------------------------
    # Topology section
    # -----------------------------------------------------------------------

    if is_all(atom_indices):

        # --- atoms ---
        n_atoms = topo_in.attrs['n_atoms']
        topo_out.attrs['n_atoms'] = n_atoms
        if n_atoms:
            for field in ('atom_id', 'atom_name', 'atom_type', 'group_index', 'component_index', 'chain_index'):
                topo_out['atoms'][field].resize((n_atoms,))
                topo_out['atoms'][field][:] = topo_in['atoms'][field][:]

        # --- groups ---
        n_groups = topo_in.attrs['n_groups']
        topo_out.attrs['n_groups'] = n_groups
        if n_groups:
            for field in ('group_id', 'group_name', 'group_type', 'molecule_index'):
                topo_out['groups'][field].resize((n_groups,))
                topo_out['groups'][field][:] = topo_in['groups'][field][:]

        # --- molecules ---
        n_molecules = topo_in.attrs['n_molecules']
        topo_out.attrs['n_molecules'] = n_molecules
        if n_molecules:
            for field in ('molecule_id', 'molecule_name', 'molecule_type', 'entity_index'):
                topo_out['molecules'][field].resize((n_molecules,))
                topo_out['molecules'][field][:] = topo_in['molecules'][field][:]

        # --- entities ---
        n_entities = topo_in.attrs['n_entities']
        topo_out.attrs['n_entities'] = n_entities
        if n_entities:
            for field in ('entity_id', 'entity_name', 'entity_type'):
                topo_out['entities'][field].resize((n_entities,))
                topo_out['entities'][field][:] = topo_in['entities'][field][:]

        # --- components ---
        n_components = topo_in.attrs['n_components']
        topo_out.attrs['n_components'] = n_components
        if n_components:
            for field in ('component_id', 'component_name', 'component_type'):
                topo_out['components'][field].resize((n_components,))
                topo_out['components'][field][:] = topo_in['components'][field][:]

        # --- chains ---
        n_chains = topo_in.attrs['n_chains']
        topo_out.attrs['n_chains'] = n_chains
        if n_chains:
            for field in ('chain_id', 'chain_name', 'chain_type'):
                topo_out['chains'][field].resize((n_chains,))
                topo_out['chains'][field][:] = topo_in['chains'][field][:]

        # --- bonds ---
        n_bonds = topo_in.attrs['n_bonds']
        topo_out.attrs['n_bonds'] = n_bonds
        if n_bonds:
            for field in ('atom1_index', 'atom2_index', 'order', 'type'):
                topo_out['bonds'][field].resize((n_bonds,))
                topo_out['bonds'][field][:] = topo_in['bonds'][field][:]

    else:

        # --- atoms ---
        n_atoms = len(atom_indices)
        topo_out.attrs['n_atoms'] = n_atoms

        topo_out['atoms']['atom_id'].resize((n_atoms,))
        topo_out['atoms']['atom_name'].resize((n_atoms,))
        topo_out['atoms']['atom_type'].resize((n_atoms,))
        topo_out['atoms']['atom_id'][:] = topo_in['atoms']['atom_id'][atom_indices]
        topo_out['atoms']['atom_name'][:] = topo_in['atoms']['atom_name'][atom_indices]
        topo_out['atoms']['atom_type'][:] = topo_in['atoms']['atom_type'][atom_indices]

        group_indices, new_group_index = np.unique(
            topo_in['atoms']['group_index'][atom_indices], return_inverse=True)
        topo_out['atoms']['group_index'].resize((n_atoms,))
        topo_out['atoms']['group_index'][:] = new_group_index.astype(int_type)

        component_indices, new_component_index = np.unique(
            topo_in['atoms']['component_index'][atom_indices], return_inverse=True)
        topo_out['atoms']['component_index'].resize((n_atoms,))
        topo_out['atoms']['component_index'][:] = new_component_index.astype(int_type)

        chain_indices, new_chain_index = np.unique(
            topo_in['atoms']['chain_index'][atom_indices], return_inverse=True)
        topo_out['atoms']['chain_index'].resize((n_atoms,))
        topo_out['atoms']['chain_index'][:] = new_chain_index.astype(int_type)

        # --- groups ---
        n_groups = len(group_indices)
        topo_out.attrs['n_groups'] = n_groups
        if n_groups:
            topo_out['groups']['group_id'].resize((n_groups,))
            topo_out['groups']['group_name'].resize((n_groups,))
            topo_out['groups']['group_type'].resize((n_groups,))
            topo_out['groups']['group_id'][:] = topo_in['groups']['group_id'][group_indices]
            topo_out['groups']['group_name'][:] = topo_in['groups']['group_name'][group_indices]
            topo_out['groups']['group_type'][:] = topo_in['groups']['group_type'][group_indices]

            molecule_indices, new_molecule_index = np.unique(
                topo_in['groups']['molecule_index'][group_indices], return_inverse=True)
            topo_out['groups']['molecule_index'].resize((n_groups,))
            topo_out['groups']['molecule_index'][:] = new_molecule_index.astype(int_type)
        else:
            molecule_indices = np.array([], dtype=int_type)

        # --- molecules ---
        n_molecules = len(molecule_indices)
        topo_out.attrs['n_molecules'] = n_molecules
        if n_molecules:
            topo_out['molecules']['molecule_id'].resize((n_molecules,))
            topo_out['molecules']['molecule_name'].resize((n_molecules,))
            topo_out['molecules']['molecule_type'].resize((n_molecules,))
            topo_out['molecules']['molecule_id'][:] = topo_in['molecules']['molecule_id'][molecule_indices]
            topo_out['molecules']['molecule_name'][:] = topo_in['molecules']['molecule_name'][molecule_indices]
            topo_out['molecules']['molecule_type'][:] = topo_in['molecules']['molecule_type'][molecule_indices]

            entity_indices, new_entity_index = np.unique(
                topo_in['molecules']['entity_index'][molecule_indices], return_inverse=True)
            topo_out['molecules']['entity_index'].resize((n_molecules,))
            topo_out['molecules']['entity_index'][:] = new_entity_index.astype(int_type)
        else:
            entity_indices = np.array([], dtype=int_type)

        # --- entities ---
        n_entities = len(entity_indices)
        topo_out.attrs['n_entities'] = n_entities
        if n_entities:
            for field in ('entity_id', 'entity_name', 'entity_type'):
                topo_out['entities'][field].resize((n_entities,))
                topo_out['entities'][field][:] = topo_in['entities'][field][entity_indices]

        # --- components ---
        n_components = len(component_indices)
        topo_out.attrs['n_components'] = n_components
        if n_components:
            for field in ('component_id', 'component_name', 'component_type'):
                topo_out['components'][field].resize((n_components,))
                topo_out['components'][field][:] = topo_in['components'][field][component_indices]

        # --- chains ---
        n_chains = len(chain_indices)
        topo_out.attrs['n_chains'] = n_chains
        if n_chains:
            for field in ('chain_id', 'chain_name', 'chain_type'):
                topo_out['chains'][field].resize((n_chains,))
                topo_out['chains'][field][:] = topo_in['chains'][field][chain_indices]

        # --- bonds ---
        mask1 = np.isin(topo_in['bonds']['atom1_index'][:], atom_indices)
        mask2 = np.isin(topo_in['bonds']['atom2_index'][:], atom_indices)
        mask = mask1 & mask2

        n_bonds = int(np.sum(mask))
        topo_out.attrs['n_bonds'] = n_bonds

        if n_bonds:
            topo_out['bonds']['atom1_index'].resize((n_bonds,))
            topo_out['bonds']['atom2_index'].resize((n_bonds,))
            topo_out['bonds']['atom1_index'][:] = np.searchsorted(
                atom_indices, topo_in['bonds']['atom1_index'][mask].astype(np.int64), side='left')
            topo_out['bonds']['atom2_index'][:] = np.searchsorted(
                atom_indices, topo_in['bonds']['atom2_index'][mask].astype(np.int64), side='left')

            n_bonds_order = int(np.sum(mask & (topo_in['bonds']['order'].asstr()[:] != ''))) if n_bonds else 0
            if n_bonds_order:
                topo_out['bonds']['order'].resize((n_bonds,))
                topo_out['bonds']['order'][:] = topo_in['bonds']['order'][mask]

            n_bonds_type = int(np.sum(mask & (topo_in['bonds']['type'].asstr()[:] != ''))) if n_bonds else 0
            if n_bonds_type:
                topo_out['bonds']['type'].resize((n_bonds,))
                topo_out['bonds']['type'][:] = topo_in['bonds']['type'][mask]

    # -----------------------------------------------------------------------
    # Structures section
    # -----------------------------------------------------------------------

    structs_in = input_file['structures']
    structs_out = output_file['structures']

    if is_all(structure_indices):

        for attr in ('n_structures', 'n_structures_written', 'constant_time_step', 'time_step',
                     'constant_id_step', 'id_step', 'constant_box', 'pbc',
                     'n_degrees_of_freedom', 'temperature_from_kinetic_energy'):
            structs_out.attrs[attr] = structs_in.attrs[attr]

        for field in ('id', 'time'):
            ns = structs_in[field].shape[0]
            if ns:
                structs_out[field].resize((ns,))
                structs_out[field][:] = structs_in[field][:]

        ns = structs_in['box'].shape[0]
        if ns:
            structs_out['box'].resize((ns, 3, 3))
            structs_out['box'][:, :, :] = structs_in['box'][:, :, :]

        for field in ('kinetic_energy', 'potential_energy', 'temperature'):
            ns = structs_in[field].shape[0]
            if ns:
                structs_out[field].resize((ns,))
                structs_out[field][:] = structs_in[field][:]

        if is_all(atom_indices):
            n_at = structs_in.attrs['n_atoms']
            structs_out.attrs['n_atoms'] = n_at
            ns = structs_in['coordinates'].shape[0]
            if ns:
                structs_out['coordinates'].resize((ns, n_at, 3))
                structs_out['coordinates'][:, :, :] = structs_in['coordinates'][:, :, :]
            ns = structs_in['velocities'].shape[0]
            if ns:
                structs_out['velocities'].resize((ns, n_at, 3))
                structs_out['velocities'][:, :, :] = structs_in['velocities'][:, :, :]
        else:
            n_at = len(atom_indices)
            structs_out.attrs['n_atoms'] = n_at
            ns = structs_in['coordinates'].shape[0]
            if ns:
                structs_out['coordinates'].resize((ns, n_at, 3))
                structs_out['coordinates'][:, :, :] = structs_in['coordinates'][:, atom_indices, :]
            ns = structs_in['velocities'].shape[0]
            if ns:
                structs_out['velocities'].resize((ns, n_at, 3))
                structs_out['velocities'][:, :, :] = structs_in['velocities'][:, atom_indices, :]

    else:

        n_structures = len(structure_indices)
        intervals = structure_indices[1:] - structure_indices[:-1]
        equispaced = len(intervals) > 0 and np.all(intervals == intervals[0])
        interval = int(intervals[0]) if equispaced and len(intervals) > 0 else 0
        del intervals

        structs_out.attrs['n_structures'] = n_structures
        structs_out.attrs['n_structures_written'] = n_structures

        if structs_in.attrs['constant_time_step'] and equispaced:
            structs_out.attrs['constant_time_step'] = True
            structs_out.attrs['time_step'] = interval * structs_in.attrs['time_step']
        else:
            structs_out.attrs['constant_time_step'] = False
            structs_out.attrs['time_step'] = 0.0

        if structs_in.attrs['constant_id_step'] and equispaced:
            structs_out.attrs['constant_id_step'] = True
            structs_out.attrs['id_step'] = interval * structs_in.attrs['id_step']
        else:
            structs_out.attrs['constant_id_step'] = False
            structs_out.attrs['id_step'] = 0

        for attr in ('constant_box', 'pbc', 'n_degrees_of_freedom', 'temperature_from_kinetic_energy'):
            structs_out.attrs[attr] = structs_in.attrs[attr]

        # structure id
        if structs_in['id'].shape[0]:
            if structs_in.attrs['constant_id_step']:
                if equispaced:
                    structs_out['id'].resize((1,))
                    structs_out['id'][0] = structs_in['id'][0] + structure_indices[0] * structs_in.attrs['id_step']
                else:
                    structs_out['id'].resize((n_structures,))
                    structs_out['id'][:] = structs_in['id'][0] + structure_indices * structs_in.attrs['id_step']
            else:
                structs_out['id'].resize((n_structures,))
                structs_out['id'][:] = structs_in['id'][structure_indices]

        # time
        if structs_in['time'].shape[0]:
            if structs_in.attrs['constant_time_step']:
                if equispaced:
                    structs_out['time'].resize((1,))
                    structs_out['time'][0] = structs_in['time'][0] + structure_indices[0] * structs_in.attrs['time_step']
                else:
                    structs_out['time'].resize((n_structures,))
                    structs_out['time'][:] = structs_in['time'][0] + structure_indices * structs_in.attrs['time_step']
            else:
                structs_out['time'].resize((n_structures,))
                structs_out['time'][:] = structs_in['time'][structure_indices]

        # box
        if structs_in['box'].shape[0]:
            structs_out['box'].resize((n_structures, 3, 3))
            structs_out['box'][:, :, :] = structs_in['box'][structure_indices, :, :]

        # scalar energetics / temperature
        for field in ('kinetic_energy', 'potential_energy', 'temperature'):
            if structs_in[field].shape[0]:
                structs_out[field].resize((n_structures,))
                structs_out[field][:] = structs_in[field][structure_indices]

        if is_all(atom_indices):
            n_at = structs_in.attrs['n_atoms']
            structs_out.attrs['n_atoms'] = n_at
            if structs_in['coordinates'].shape[0]:
                structs_out['coordinates'].resize((n_structures, n_at, 3))
                structs_out['coordinates'][:, :, :] = structs_in['coordinates'][structure_indices, :, :]
            if structs_in['velocities'].shape[0]:
                structs_out['velocities'].resize((n_structures, n_at, 3))
                structs_out['velocities'][:, :, :] = structs_in['velocities'][structure_indices, :, :]
        else:
            n_at = len(atom_indices)
            structs_out.attrs['n_atoms'] = n_at
            if structs_in['coordinates'].shape[0]:
                structs_out['coordinates'].resize((n_structures, n_at, 3))
                for count, ii in enumerate(structure_indices):
                    structs_out['coordinates'][count, :, :] = structs_in['coordinates'][ii, atom_indices, :]
            if structs_in['velocities'].shape[0]:
                structs_out['velocities'].resize((n_structures, n_at, 3))
                for count, ii in enumerate(structure_indices):
                    structs_out['velocities'][count, :, :] = structs_in['velocities'][ii, atom_indices, :]

    input_file_handler.close()
    output_file_handler.close()

    return output_filename
