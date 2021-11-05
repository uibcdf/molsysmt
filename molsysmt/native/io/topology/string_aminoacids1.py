def to_string_aminoacids1 (item, molecular_system=None, atom_indices='all', frame_indices='all'):

    from molsysmt.forms.api_string_aminoacids3 import to_string_aminoacids1 as string_aminoacids3_to_string_aminoacids1
    from .string_aminoacids3 import to_string_aminoacids3 as molsysmt_Topology_to_string_aminoacids3

    tmp_item, tmp_molecular_system = molsysmt_Topology_to_string_aminoacids3(item,
            molecular_system=molecular_system, atom_indices=atom_indices, frame_indices=frame_indices)
    tmp_item, tmp_molecular_system = string_aminoacids3_to_string_aminoacids1(tmp_item,
            molecular_system=tmp_molecular_system)

    return tmp_item, tmp_molecular_system

