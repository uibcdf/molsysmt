def to_molsysmt_MolSys(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_molsysmt_MolSys as file_psf_to_molsysmt_MolSys
    from molsysmt import convert, has_attribute

    if has_attribute(molecular_system, 'structural'):

        molsysmt_structures = convert(molecular_system, selection=atom_indices, structure_indices=structure_indices,
            to_form='molsysmt.Structures')

        coordinates = molsysmt_structures.coordinates
        time = molsysmt_structures.time
        box = molsysmt_structures.box
        structure_id = molsysmt_structures.structure_id

        tmp_item = file_psf_to_molsysmt_MolSys(item, atom_indices=atom_indices, coordinates=coordinates,
            time=time, box=box, structure_id=structure_id)
    else:

        tmp_item = file_psf_to_molsysmt_MolSys(item, atom_indices=atom_indices)

    return tmp_item

def to_molsysmt_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_molsysmt_Topology as file_psf_to_molsysmt_Topology

    tmp_item = file_psf_to_molsysmt_Topology(item, atom_indices=atom_indices)

    return tmp_item

def to_openmm_CharmmPsfFile(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_openmm_CharmmPsfFile as file_psf_to_openmm_CharmmPsfFile

    tmp_item = file_psf_to_openmm_CharmmPsfFile(item, atom_indices=atom_indices)

    return tmp_item

def to_openmm_Topology(item, molecular_system, atom_indices='all', structure_indices='all'):

    from molsysmt.form.file_psf import to_openmm_Topology as file_psf_to_openmm_Topology

    tmp_item = file_psf_to_openmm_Topology(item, atom_indices=atom_indices)

    return tmp_item


