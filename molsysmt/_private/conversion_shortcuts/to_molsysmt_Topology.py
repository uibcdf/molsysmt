def molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_Topology(molecular_system, atom_indices='all',
                                                                   structure_indices='all', skip_digestion=False):

    from molsysmt.basic import get_form
    from molsysmt.form.molsysmt_Topology import extract as extract_topology

    forms = get_form(molecular_system)

    topology = None

    for form, item in zip(forms, molecular_system):
        if form=='molsysmt.Topology':
            topology = item
            break

    tmp_item = extract_topology(topology, atom_indices=atom_indices, copy_if_all=True, skip_digestion=True)

    return tmp_item

def file_prmtop_and_file_inpcrd_to_molsysmt_Topology(molecular_system, atom_indices='all',
                                                     structure_indices='all', skip_digestion=False):

    from molsysmt.basic import get_form
    from molsysmt.form.file_prmtop import to_molsysmt_Topology as file_prmtop_to_molsysmt_Topology

    forms = get_form(molecular_system)

    item_prmtop = None

    for form, item in zip(forms, molecular_system):
        if form=='file:prmtop':
            item_prmtop = item
            break

    tmp_item = file_prmtop_to_molsysmt_Topology(item_prmtop, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

def file_psf_and_file_dcd_to_molsysmt_Topology(molecular_system, atom_indices='all', structure_indices='all',
                                               skip_digestion=False):

    from molsysmt.basic import get_form
    from molsysmt.form.file_psf import to_molsysmt_Topology as file_psf_to_molsysmt_Topology
    from molsysmt.native import MolSys

    forms = get_form(molecular_system)

    item_psf = None

    for form, item in zip(forms, molecular_system):
        if form=='file:psf':
            item_psf = item
            break

    tmp_item = file_psf_to_molsysmt_Topology(item_psf, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

def file_psf_and_file_crd_to_molsysmt_Topology(molecular_system, atom_indices='all', structure_indices='all', 
                                               skip_digestion=False):

    from molsysmt.basic import get_form
    from molsysmt.form.file_psf import to_molsysmt_Topology as file_psf_to_molsysmt_Topology

    forms = get_form(molecular_system)

    item_psf = None

    for form, item in zip(forms, molecular_system):
        if form=='file:psf':
            item_psf = item
            break

    tmp_item = file_psf_to_molsysmt_Topology(item_psf, atom_indices=atom_indices, skip_digestion=True)

    return tmp_item

def file_gro_and_file_xtc_to_molsysmt_Topology(molecular_system, atom_indices='all', structure_indices='all',
                                               skip_digestion=False):

    from molsysmt.basic import get_form
    from molsysmt.form.file_gro import to_molsysmt_Topology as file_gro_to_molsysmt_Topology

    forms = get_form(molecular_system)

    item_gro = None

    for form, item in zip(forms, molecular_system):
        if form=='file:gro':
            item_gro = item
            break


    tmp_item = file_gro_to_molsysmt_Topology(item_gro, atom_indices=atom_indices, get_missing_bonds=True,
                                             skip_digestion=True)

    return output_item

