from molsysmt._private.digestion import arg_digest
from molsysmt.dependencies import requires

@arg_digest(form='mmtf.MMTFDecoder')
@requires('mmtf')
def to_mmtf_MMTFDecoder(item, atom_indices='all', structure_indices='all', copy_if_all=True, skip_digestion=False):

    from .extract import extract

    return extract(item, atom_indices=atom_indices, structure_indices=structure_indices, copy_if_all=copy_if_all, skip_digestion=True)

