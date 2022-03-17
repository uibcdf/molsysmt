from molsysmt._private_tools.exceptions import *
from molsysmt._private_tools.digestion import *
from molsysmt.tools.mmtf_MMTFDecoder.is_mmtf_MMTFDecoder import is_mmtf_MMTFDecoder

def to_molsysmt_MolSys(item, atom_indices='all', structure_indices='all', check=True):

    if check:

        if not is_mmtf_MMTFDecoder(item):
            raise WrongFormError('mmtf.MMTFDecoder')

        try:
            atom_indices = digest_indices(atom_indices)
        except:
            raise WrongIndicesError()

        try:
            structure_indices = digest_structure_indices(structure_indices)
        except:
            raise WrongStructureIndicesError()

    from molsysmt.native.molsys import MolSys
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Topology as mmtf_MMTFDecoder_to_molsysmt_Topology
    from molsysmt.tools.mmtf_MMTFDecoder import to_molsysmt_Structures as mmtf_MMTFDecoder_to_molsysmt_Structures

    tmp_item = MolSys()
    tmp_item.topology = mmtf_MMTFDecoder_to_molsysmt_Topology(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)
    tmp_item.structures = mmtf_MMTFDecoder_to_molsysmt_Structures(item, atom_indices=atom_indices, structure_indices=structure_indices, check=False)

    return tmp_item

