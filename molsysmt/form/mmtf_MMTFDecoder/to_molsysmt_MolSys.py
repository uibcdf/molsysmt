from molsysmt._private.digestion import digest

@digest(form='mmtf.MMTFDecoder')
def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', bioassembly_name=None):

    from molsysmt.native.molsys import MolSys
    from .to_molsysmt_Topology import to_molsysmt_Topology
    from .to_molsysmt_Structures import to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices)
    tmp_item.structures = to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices)

    if bioassembly_name is not None:

        from .get import get_bioassemblies_from_system
        from molsysmt.build import make_bioassembly

        bioassemblies = get_bioassemblies_from_system(item)
        tmp_item = make_bioassembly(tmp_item, bioassembly=bioassemblies[bioassembly_name])

    return tmp_item
