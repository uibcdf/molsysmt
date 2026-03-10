from molsysmt._private.arg_digestion import arg_digest

def file_prmtop_and_file_inpcrd_to_molsysmt_MolSys(molecular_system, atom_indices='all', structure_indices='all',
                                                  skip_digestion=False):
    """Build a MolSys from a prmtop topology and inpcrd coordinates."""

    from molsysmt.basic import get_form
    from molsysmt.form.file_prmtop.to_molsysmt_Topology import to_molsysmt_Topology as file_prmtop_to_molsysmt_Topology
    from molsysmt.form.file_inpcrd.to_molsysmt_Structures import to_molsysmt_Structures as file_inpcrd_to_molsysmt_Structures
    from molsysmt.native import MolSys

    forms = get_form(molecular_system)

    item_prmtop = None
    item_inpcrd = None

    for form, item in zip(forms, molecular_system):
        if form=='file:prmtop':
            item_prmtop = item
        else:
            item_inpcrd = item

    output_item = MolSys()

    output_item.topology = file_prmtop_to_molsysmt_Topology(item_prmtop, atom_indices=atom_indices,
                                                            skip_digestion=True)
    output_item.structures = file_inpcrd_to_molsysmt_Structures(item_inpcrd, atom_indices=atom_indices,
                                                                structure_indices=structure_indices,
                                                                skip_digestion=True)

    return output_item

def file_psf_and_file_dcd_to_molsysmt_MolSys(molecular_system, atom_indices='all', structure_indices='all',
                                             skip_digestion=False):
    """Build a MolSys from a PSF topology and DCD trajectory."""

    from molsysmt.basic import get_form
    from molsysmt.form.file_psf.to_molsysmt_Topology import to_molsysmt_Topology as file_psf_to_molsysmt_Topology
    from molsysmt.form.file_dcd.to_molsysmt_Structures import to_molsysmt_Structures as file_dcd_to_molsysmt_Structures
    from molsysmt.native import MolSys

    forms = get_form(molecular_system)

    item_psf = None
    item_dcd = None

    for form, item in zip(forms, molecular_system):
        if form=='file:psf':
            item_psf = item
        else:
            item_dcd = item

    output_item = MolSys()

    output_item.topology = file_psf_to_molsysmt_Topology(item_psf, atom_indices=atom_indices,
                                                         skip_digestion=True)
    output_item.structures = file_dcd_to_molsysmt_Structures(item_dcd, atom_indices=atom_indices,
                                                             structure_indices=structure_indices,
                                                             skip_digestion=True)

    return output_item

def file_gro_and_file_xtc_to_molsysmt_MolSys(molecular_system, atom_indices='all', structure_indices='all',
                                             skip_digestion=False):
    """Build a MolSys from a GRO topology and XTC trajectory."""

    from molsysmt.basic import get_form
    from molsysmt.form.file_gro.to_molsysmt_Topology import to_molsysmt_Topology as file_gro_to_molsysmt_Topology
    from molsysmt.form.file_xtc.to_molsysmt_Structures import to_molsysmt_Structures as file_xtc_to_molsysmt_Structures
    from molsysmt.native import MolSys

    forms = get_form(molecular_system)

    item_gro = None
    item_xtc = None

    for form, item in zip(forms, molecular_system):
        if form=='file:gro':
            item_gro = item
        else:
            item_xtc = item

    output_item = MolSys()

    output_item.topology = file_gro_to_molsysmt_Topology(item_gro, atom_indices=atom_indices,
                                                         skip_digestion=True)
    output_item.structures = file_xtc_to_molsysmt_Structures(item_xtc, atom_indices=atom_indices,
                                                             structure_indices=structure_indices,
                                                             skip_digestion=True)

    return output_item


def molsysmt_Topology_and_molsysmt_Structures_to_molsysmt_MolSys(molecular_system, atom_indices='all', structure_indices='all',
                                                                  skip_digestion=False):
    """Build a MolSys from native Topology and Structures objects."""

    from molsysmt.basic import get_form
    from molsysmt.native import MolSys

    forms = get_form(molecular_system)

    item_topology = None
    item_structures = None

    for form, item in zip(forms, molecular_system):
        if form == 'molsysmt.Topology':
            item_topology = item
        elif form == 'molsysmt.Structures':
            item_structures = item

    output_item = MolSys()

    output_item.topology = item_topology.extract(atom_indices=atom_indices, copy_if_all=True, skip_digestion=True)
    output_item.structures = item_structures.extract(atom_indices=atom_indices,
                                                     structure_indices=structure_indices,
                                                     copy_if_all=True,
                                                     skip_digestion=True)

    return output_item
